from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from config import Config
from database.models import db, User, AnalysisResult, EncryptedData, AuditLog
from modules.analyzer import EncryptionAnalyzer
from modules.key_manager import KeyManager
from modules.report_generator import ReportGenerator
from modules.memory_encryptor import MemoryEncryptor
import os
import sys
import base64
from datetime import datetime
import json
from io import BytesIO

# Set UTF-8 encoding for console output on Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize modules
analyzer = EncryptionAnalyzer(Config)
key_manager = KeyManager(Config.KEY_VAULT_PATH, Config.AUDIT_LOG_PATH)
report_generator = ReportGenerator()

# Initialize memory encryptor (will be initialized after app context)
memory_encryptor = None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== Authentication Routes ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            
            # Log audit
            audit = AuditLog(
                user_id=user.id,
                action='LOGIN',
                details=f'User {username} logged in',
                ip_address=request.remote_addr
            )
            db.session.add(audit)
            db.session.commit()
            
            flash('Muvaffaqiyatli kirdingiz!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Noto\'g\'ri foydalanuvchi nomi yoki parol!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('Barcha maydonlarni to\'ldiring!', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Parollar mos kelmadi!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Parol kamida 6 ta belgidan iborat bo\'lishi kerak!', 'error')
            return render_template('register.html')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Bu foydalanuvchi nomi band!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Bu email allaqachon ro\'yxatdan o\'tgan!', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Log audit
        audit = AuditLog(
            user_id=user.id,
            action='REGISTER',
            details=f'New user registered: {username}',
            ip_address=request.remote_addr
        )
        db.session.add(audit)
        db.session.commit()
        
        flash('Ro\'yxatdan o\'tdingiz! Endi tizimga kirishingiz mumkin.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    # Log audit
    audit = AuditLog(
        user_id=current_user.id,
        action='LOGOUT',
        details=f'User {current_user.username} logged out',
        ip_address=request.remote_addr
    )
    db.session.add(audit)
    db.session.commit()
    
    logout_user()
    flash('Tizimdan chiqdingiz!', 'info')
    return redirect(url_for('login'))

# ==================== Main Routes ====================

@app.route('/')
@login_required
def index():
    """Dashboard page"""
    # Get recent analysis results
    recent_results = AnalysisResult.query.filter_by(user_id=current_user.id)\
        .order_by(AnalysisResult.created_at.desc()).limit(5).all()
    
    # Get statistics
    total_analyses = AnalysisResult.query.filter_by(user_id=current_user.id).count()
    
    return render_template('index.html', 
                         recent_results=recent_results,
                         total_analyses=total_analyses)

@app.route('/analyze', methods=['GET', 'POST'])
@login_required
def analyze():
    """Analysis page"""
    if request.method == 'POST':
        try:
            # Get input data
            input_type = request.form.get('input_type', 'text')
            
            if input_type == 'text':
                plaintext = request.form.get('plaintext', '')
                if not plaintext:
                    return jsonify({'error': 'Matn kiritilmagan!'}), 400
            else:
                # File upload
                if 'file' not in request.files:
                    return jsonify({'error': 'Fayl tanlanmagan!'}), 400
                
                file = request.files['file']
                if file.filename == '':
                    return jsonify({'error': 'Fayl tanlanmagan!'}), 400
                
                plaintext = file.read()
            
            # Run analysis on all algorithms
            results = analyzer.compare_algorithms(plaintext)
            
            # Save results to database
            for result in results:
                analysis_result = AnalysisResult(
                    user_id=current_user.id,
                    algorithm=result['algorithm'],
                    encryption_time_ms=result['encryption_time_ms'],
                    decryption_time_ms=result['decryption_time_ms'],
                    total_time_ms=result['total_time_ms'],
                    avg_cpu_percent=result['avg_cpu_percent'],
                    avg_memory_mb=result['avg_memory_mb'],
                    entropy=result['entropy'],
                    key_size=result['key_size'],
                    security_level=result['security_level'],
                    t_performance=result['T_performance'],
                    e_security=result['E_security'],
                    k_key_management=result['K_key_management'],
                    i_integrity=result['I_integrity'],
                    s_overall_score=result['S_overall_score'],
                    plaintext_size=result['plaintext_size'],
                    ciphertext_size=result['ciphertext_size'],
                    integrity_check=result['integrity_check']
                )
                db.session.add(analysis_result)
            
            db.session.commit()
            
            # Log audit
            audit = AuditLog(
                user_id=current_user.id,
                action='ANALYSIS',
                details=f'Analyzed {len(results)} algorithms',
                ip_address=request.remote_addr
            )
            db.session.add(audit)
            db.session.commit()
            
            # Store results in session for report generation
            session['last_analysis'] = results
            
            return jsonify({
                'success': True,
                'results': results,
                'best_algorithm': analyzer.get_best_algorithm(results)
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('analyze.html')

@app.route('/encrypt', methods=['POST'])
@login_required
def encrypt_data():
    """Encrypt data with selected algorithm"""
    try:
        algorithm = request.form.get('algorithm')
        plaintext = request.form.get('plaintext', '')
        
        if not algorithm or not plaintext:
            return jsonify({'error': 'Algoritm yoki matn kiritilmagan!'}), 400
        
        # Create key
        key_id = key_manager.create_key(algorithm, current_user.username)
        key, iv_or_nonce, _ = key_manager.get_key(key_id)
        
        # Analyze and encrypt
        result, _, _ = analyzer.analyze_algorithm(algorithm, plaintext, key, iv_or_nonce)
        
        # Store encrypted data
        encrypted_data = EncryptedData(
            user_id=current_user.id,
            algorithm=algorithm,
            key_id=key_id,
            content_type='text'
        )
        encrypted_data.set_encrypted_content(plaintext)
        db.session.add(encrypted_data)
        db.session.commit()
        
        # Log audit
        audit = AuditLog(
            user_id=current_user.id,
            action='ENCRYPT',
            details=f'Encrypted data with {algorithm}',
            ip_address=request.remote_addr
        )
        db.session.add(audit)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'encrypted_id': encrypted_data.id,
            'key_id': key_id,
            'metrics': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/decrypt/<int:encrypted_id>', methods=['POST'])
@login_required
def decrypt_data(encrypted_id):
    """Decrypt data"""
    try:
        encrypted_data = EncryptedData.query.get_or_404(encrypted_id)
        
        # Check ownership
        if encrypted_data.user_id != current_user.id:
            return jsonify({'error': 'Ruxsat yo\'q!'}), 403
        
        # Get key
        key, iv_or_nonce, algorithm = key_manager.get_key(encrypted_data.key_id)
        
        # Decrypt
        plaintext = encrypted_data.get_decrypted_content()
        
        # Log audit
        audit = AuditLog(
            user_id=current_user.id,
            action='DECRYPT',
            details=f'Decrypted data with {algorithm}',
            ip_address=request.remote_addr
        )
        db.session.add(audit)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'plaintext': plaintext.decode('utf-8'),
            'algorithm': algorithm
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/encrypted')
@login_required
def encrypted():
    """Encrypted data page"""
    encrypted_data = EncryptedData.query.filter_by(user_id=current_user.id)\
        .order_by(EncryptedData.created_at.desc()).all()
    
    return render_template('encrypted.html', encrypted_data=encrypted_data)

@app.route('/delete_encrypted/<int:encrypted_id>', methods=['DELETE'])
@login_required
def delete_encrypted(encrypted_id):
    """Delete encrypted data"""
    try:
        encrypted_data = EncryptedData.query.get_or_404(encrypted_id)
        
        # Check ownership
        if encrypted_data.user_id != current_user.id:
            return jsonify({'error': 'Ruxsat yo\'q!'}), 403
        
        # Delete
        db.session.delete(encrypted_data)
        db.session.commit()
        
        # Log audit
        audit = AuditLog(
            user_id=current_user.id,
            action='DELETE_ENCRYPTED',
            details=f'Deleted encrypted data ID: {encrypted_id}',
            ip_address=request.remote_addr
        )
        db.session.add(audit)
        db.session.commit()
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/report')
@login_required
def report():
    """Report page"""
    # Get last analysis from session or database
    results = session.get('last_analysis')
    
    if not results:
        # Get latest analysis from database
        latest_results = AnalysisResult.query.filter_by(user_id=current_user.id)\
            .order_by(AnalysisResult.created_at.desc()).limit(4).all()
        
        if latest_results:
            results = [
                {
                    'algorithm': r.algorithm,
                    'encryption_time_ms': r.encryption_time_ms,
                    'decryption_time_ms': r.decryption_time_ms,
                    'total_time_ms': r.total_time_ms,
                    'avg_cpu_percent': r.avg_cpu_percent,
                    'avg_memory_mb': r.avg_memory_mb,
                    'entropy': r.entropy,
                    'key_size': r.key_size,
                    'security_level': r.security_level,
                    'T_performance': r.t_performance,
                    'E_security': r.e_security,
                    'K_key_management': r.k_key_management,
                    'I_integrity': r.i_integrity,
                    'S_overall_score': r.s_overall_score,
                    'plaintext_size': r.plaintext_size,
                    'ciphertext_size': r.ciphertext_size,
                    'integrity_check': r.integrity_check
                }
                for r in latest_results
            ]
    
    return render_template('report.html', results=results)

@app.route('/export/pdf')
@login_required
def export_pdf():
    """Export report as PDF"""
    try:
        results = session.get('last_analysis')
        
        if not results:
            flash('Tahlil natijalari topilmadi!', 'error')
            return redirect(url_for('report'))
        
        # Generate PDF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'encryption_report_{timestamp}.pdf'
        output_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        report_generator.generate_pdf_report(results, output_path)
        
        # Log audit
        audit = AuditLog(
            user_id=current_user.id,
            action='EXPORT_PDF',
            details=f'Exported report as PDF',
            ip_address=request.remote_addr
        )
        db.session.add(audit)
        db.session.commit()
        
        return send_file(output_path, as_attachment=True, download_name=filename)
    
    except Exception as e:
        flash(f'Xatolik: {str(e)}', 'error')
        return redirect(url_for('report'))

@app.route('/history')
@login_required
def history():
    """Analysis history page"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    pagination = AnalysisResult.query.filter_by(user_id=current_user.id)\
        .order_by(AnalysisResult.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('history.html', pagination=pagination)

@app.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for statistics"""
    # Algorithm usage statistics
    algorithm_stats = db.session.query(
        AnalysisResult.algorithm,
        db.func.count(AnalysisResult.id).label('count'),
        db.func.avg(AnalysisResult.s_overall_score).label('avg_score')
    ).filter_by(user_id=current_user.id)\
     .group_by(AnalysisResult.algorithm).all()
    
    stats = {
        'algorithms': [
            {
                'name': stat.algorithm,
                'count': stat.count,
                'avg_score': round(stat.avg_score, 4) if stat.avg_score else 0
            }
            for stat in algorithm_stats
        ]
    }
    
    return jsonify(stats)

# ==================== In-Memory Encryption Routes ====================

@app.route('/secure-encrypt', methods=['GET', 'POST'])
@login_required
def secure_encrypt():
    """Secure file encryption with temporary storage"""
    if request.method == 'POST':
        try:
            # Check if MASTER_KEY is configured
            if not Config.MASTER_KEY:
                return jsonify({'error': 'MASTER_KEY not configured in .env file!'}), 500
            
            # Get algorithm selection
            algorithm = request.form.get('algorithm', 'AES')
            
            # Get file from request
            if 'file' not in request.files:
                return jsonify({'error': 'Fayl tanlanmagan!'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'Fayl tanlanmagan!'}), 400
            
            # Get original filename
            original_filename = secure_filename(file.filename)
            
            # Read file into BytesIO
            file_stream = BytesIO(file.read())
            
            # Initialize encryptor
            global memory_encryptor
            if memory_encryptor is None:
                memory_encryptor = MemoryEncryptor(Config.MASTER_KEY)
            
            # Encrypt based on algorithm
            if algorithm == 'AES':
                encrypted_data_stream, encrypted_key_stream = memory_encryptor.encrypt_file_aes(file_stream)
            elif algorithm == 'Fernet':
                encrypted_data_stream, encrypted_key_stream = memory_encryptor.encrypt_file_fernet(file_stream)
            elif algorithm == 'ChaCha20':
                encrypted_data_stream, encrypted_key_stream = memory_encryptor.encrypt_file_chacha20(file_stream)
            else:
                return jsonify({'error': 'Noto\'g\'ri algoritm!'}), 400
            
            # Create user-specific temp folder
            user_temp_folder = os.path.join(Config.TEMP_ENCRYPTED_FOLDER, str(current_user.id))
            os.makedirs(user_temp_folder, exist_ok=True)
            
            # Generate unique session ID for this encryption
            import uuid
            session_id = str(uuid.uuid4())
            
            # Create session folder
            session_folder = os.path.join(user_temp_folder, session_id)
            os.makedirs(session_folder, exist_ok=True)
            
            # Save encrypted files to temp folder
            enc_filename = f"{original_filename}.enc"
            key_filename = f"{original_filename}.key"
            
            enc_path = os.path.join(session_folder, enc_filename)
            key_path = os.path.join(session_folder, key_filename)
            
            with open(enc_path, 'wb') as f:
                f.write(encrypted_data_stream.getvalue())
            
            with open(key_path, 'wb') as f:
                f.write(encrypted_key_stream.getvalue())
            
            # Store session info
            session['encryption_session_id'] = session_id
            session['original_filename'] = original_filename
            session['encryption_algorithm'] = algorithm
            
            # Log audit
            audit = AuditLog(
                user_id=current_user.id,
                action='SECURE_ENCRYPT',
                details=f'Encrypted file {original_filename} with {algorithm} (in-memory)',
                ip_address=request.remote_addr
            )
            db.session.add(audit)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Fayl muvaffaqiyatli shifrlandi!',
                'algorithm': algorithm,
                'filename': original_filename
            })
        
        except Exception as e:
            return jsonify({'error': f'Xatolik: {str(e)}'}), 500
    
    return render_template('secure_encrypt.html')

@app.route('/download-encrypted-data')
@login_required
def download_encrypted_data():
    """Download encrypted data file and delete after"""
    try:
        session_id = session.get('encryption_session_id')
        original_filename = session.get('original_filename', 'file')
        
        if not session_id:
            flash('Shifrlangan ma\'lumot topilmadi!', 'error')
            return redirect(url_for('secure_encrypt'))
        
        # Get file path
        user_temp_folder = os.path.join(Config.TEMP_ENCRYPTED_FOLDER, str(current_user.id))
        session_folder = os.path.join(user_temp_folder, session_id)
        enc_path = os.path.join(session_folder, f"{original_filename}.enc")
        
        if not os.path.exists(enc_path):
            flash('Fayl topilmadi!', 'error')
            return redirect(url_for('secure_encrypt'))
        
        # Read file to memory
        with open(enc_path, 'rb') as f:
            file_data = f.read()
        
        # Mark that data file was downloaded
        session['enc_downloaded'] = True
        
        # Check if both files downloaded, then delete folder
        if session.get('key_downloaded'):
            import shutil
            try:
                shutil.rmtree(session_folder)
                # Clear session
                session.pop('encryption_session_id', None)
                session.pop('original_filename', None)
                session.pop('enc_downloaded', None)
                session.pop('key_downloaded', None)
            except Exception as del_error:
                print(f"[ERROR] Failed to delete folder: {del_error}")
        
        # Send file from memory
        return send_file(
            BytesIO(file_data),
            as_attachment=True,
            download_name=f"{original_filename}.enc",
            mimetype='application/octet-stream'
        )
    
    except Exception as e:
        flash(f'Xatolik: {str(e)}', 'error')
        return redirect(url_for('secure_encrypt'))

@app.route('/download-encrypted-key')
@login_required
def download_encrypted_key():
    """Download encrypted key file and delete after"""
    try:
        session_id = session.get('encryption_session_id')
        original_filename = session.get('original_filename', 'file')
        
        if not session_id:
            flash('Shifrlangan kalit topilmadi!', 'error')
            return redirect(url_for('secure_encrypt'))
        
        # Get file path
        user_temp_folder = os.path.join(Config.TEMP_ENCRYPTED_FOLDER, str(current_user.id))
        session_folder = os.path.join(user_temp_folder, session_id)
        key_path = os.path.join(session_folder, f"{original_filename}.key")
        
        if not os.path.exists(key_path):
            flash('Fayl topilmadi!', 'error')
            return redirect(url_for('secure_encrypt'))
        
        # Read file to memory
        with open(key_path, 'rb') as f:
            file_data = f.read()
        
        # Mark that key file was downloaded
        session['key_downloaded'] = True
        
        # Check if both files downloaded, then delete folder
        if session.get('enc_downloaded'):
            import shutil
            try:
                shutil.rmtree(session_folder)
                # Clear session
                session.pop('encryption_session_id', None)
                session.pop('original_filename', None)
                session.pop('enc_downloaded', None)
                session.pop('key_downloaded', None)
            except Exception as del_error:
                print(f"[ERROR] Failed to delete folder: {del_error}")
        
        # Send file from memory
        return send_file(
            BytesIO(file_data),
            as_attachment=True,
            download_name=f"{original_filename}.key",
            mimetype='application/octet-stream'
        )
    
    except Exception as e:
        flash(f'Xatolik: {str(e)}', 'error')
        return redirect(url_for('secure_encrypt'))

@app.route('/secure-decrypt', methods=['GET', 'POST'])
@login_required
def secure_decrypt():
    """Secure in-memory file decryption page"""
    if request.method == 'POST':
        try:
            # Check if MASTER_KEY is configured
            if not Config.MASTER_KEY:
                return jsonify({'error': 'MASTER_KEY not configured in .env file!'}), 500
            
            # Get algorithm selection
            algorithm = request.form.get('algorithm', 'AES')
            
            # Get encrypted data file
            if 'encrypted_file' not in request.files:
                return jsonify({'error': 'Shifrlangan fayl tanlanmagan!'}), 400
            
            encrypted_file = request.files['encrypted_file']
            if encrypted_file.filename == '':
                return jsonify({'error': 'Shifrlangan fayl tanlanmagan!'}), 400
            
            # Get encrypted key file
            if 'key_file' not in request.files:
                return jsonify({'error': 'Kalit fayli tanlanmagan!'}), 400
            
            key_file = request.files['key_file']
            if key_file.filename == '':
                return jsonify({'error': 'Kalit fayli tanlanmagan!'}), 400
            
            # Read files into BytesIO
            encrypted_data_stream = BytesIO(encrypted_file.read())
            encrypted_key_stream = BytesIO(key_file.read())
            
            # Initialize encryptor
            global memory_encryptor
            if memory_encryptor is None:
                memory_encryptor = MemoryEncryptor(Config.MASTER_KEY)
            
            # Decrypt based on algorithm
            if algorithm == 'AES':
                decrypted_stream = memory_encryptor.decrypt_file_aes(encrypted_data_stream, encrypted_key_stream)
            elif algorithm == 'Fernet':
                decrypted_stream = memory_encryptor.decrypt_file_fernet(encrypted_data_stream, encrypted_key_stream)
            elif algorithm == 'ChaCha20':
                decrypted_stream = memory_encryptor.decrypt_file_chacha20(encrypted_data_stream, encrypted_key_stream)
            else:
                return jsonify({'error': 'Noto\'g\'ri algoritm!'}), 400
            
            # Get original filename (remove .enc extension)
            original_filename = secure_filename(encrypted_file.filename)
            if original_filename.endswith('.enc'):
                original_filename = original_filename[:-4]
            
            # Create user-specific temp folder
            user_temp_folder = os.path.join(Config.TEMP_ENCRYPTED_FOLDER, str(current_user.id))
            os.makedirs(user_temp_folder, exist_ok=True)
            
            # Generate unique session ID for decryption
            import uuid
            decrypt_session_id = str(uuid.uuid4())
            
            # Create session folder
            decrypt_folder = os.path.join(user_temp_folder, decrypt_session_id)
            os.makedirs(decrypt_folder, exist_ok=True)
            
            # Save decrypted file to temp folder
            decrypted_path = os.path.join(decrypt_folder, original_filename)
            with open(decrypted_path, 'wb') as f:
                f.write(decrypted_stream.getvalue())
            
            # Store session info
            session['decryption_session_id'] = decrypt_session_id
            session['decrypted_filename'] = original_filename
            
            # Log audit
            audit = AuditLog(
                user_id=current_user.id,
                action='SECURE_DECRYPT',
                details=f'Decrypted file with {algorithm} (in-memory)',
                ip_address=request.remote_addr
            )
            db.session.add(audit)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Fayl muvaffaqiyatli deshifrlandi!',
                'algorithm': algorithm
            })
        
        except Exception as e:
            return jsonify({'error': f'Xatolik: {str(e)}'}), 500
    
    return render_template('secure_decrypt.html')

@app.route('/download-decrypted')
@login_required
def download_decrypted():
    """Download decrypted file and delete after"""
    try:
        decrypt_session_id = session.get('decryption_session_id')
        filename = session.get('decrypted_filename', 'decrypted_file')
        
        if not decrypt_session_id:
            flash('Deshifrlangan ma\'lumot topilmadi!', 'error')
            return redirect(url_for('secure_decrypt'))
        
        # Get file path
        user_temp_folder = os.path.join(Config.TEMP_ENCRYPTED_FOLDER, str(current_user.id))
        decrypt_folder = os.path.join(user_temp_folder, decrypt_session_id)
        decrypted_path = os.path.join(decrypt_folder, filename)
        
        if not os.path.exists(decrypted_path):
            flash('Fayl topilmadi!', 'error')
            return redirect(url_for('secure_decrypt'))
        
        # Read file to memory
        with open(decrypted_path, 'rb') as f:
            file_data = f.read()
        
        # Delete folder immediately
        import shutil
        try:
            shutil.rmtree(decrypt_folder)
            # Clear session
            session.pop('decryption_session_id', None)
            session.pop('decrypted_filename', None)
        except Exception as del_error:
            print(f"[ERROR] Failed to delete folder: {del_error}")
        
        # Send file from memory
        return send_file(
            BytesIO(file_data),
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
    
    except Exception as e:
        flash(f'Xatolik: {str(e)}', 'error')
        return redirect(url_for('secure_decrypt'))

# ==================== Admin Routes ====================

@app.route('/admin/cleanup-temp')
@login_required
def admin_cleanup_temp():
    """Manually cleanup all temporary files (admin only)"""
    if current_user.username != 'admin':
        flash('Faqat admin uchun!', 'error')
        return redirect(url_for('index'))
    
    import shutil
    deleted_count = 0
    
    try:
        if os.path.exists(Config.TEMP_ENCRYPTED_FOLDER):
            for user_folder in os.listdir(Config.TEMP_ENCRYPTED_FOLDER):
                user_path = os.path.join(Config.TEMP_ENCRYPTED_FOLDER, user_folder)
                if not os.path.isdir(user_path):
                    continue
                
                for session_folder in os.listdir(user_path):
                    session_path = os.path.join(user_path, session_folder)
                    if os.path.isdir(session_path):
                        try:
                            shutil.rmtree(session_path)
                            deleted_count += 1
                        except:
                            pass
        
        flash(f'Tozalandi: {deleted_count} ta papka', 'success')
    except Exception as e:
        flash(f'Xatolik: {str(e)}', 'error')
    
    return redirect(url_for('index'))

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# ==================== Initialize Database ====================

with app.app_context():
    db.create_all()
    
    # Create default admin user if not exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

# ==================== Run Application ====================

def cleanup_old_temp_files():
    """Clean up temporary encrypted files older than 1 hour"""
    import time
    import shutil
    
    if not os.path.exists(Config.TEMP_ENCRYPTED_FOLDER):
        return
    
    current_time = time.time()
    one_hour = 3600  # seconds
    deleted_count = 0
    
    try:
        for user_folder in os.listdir(Config.TEMP_ENCRYPTED_FOLDER):
            user_path = os.path.join(Config.TEMP_ENCRYPTED_FOLDER, user_folder)
            if not os.path.isdir(user_path):
                continue
            
            for session_folder in os.listdir(user_path):
                session_path = os.path.join(user_path, session_folder)
                if not os.path.isdir(session_path):
                    continue
                
                # Check folder age
                folder_age = current_time - os.path.getctime(session_path)
                if folder_age > one_hour:
                    try:
                        shutil.rmtree(session_path)
                        deleted_count += 1
                        print(f"[CLEANUP] Deleted old temp folder: {session_folder}")
                    except Exception as del_err:
                        print(f"[CLEANUP] Failed to delete {session_folder}: {del_err}")
        
        if deleted_count > 0:
            print(f"[CLEANUP] Total deleted: {deleted_count} folders")
    except Exception as e:
        print(f"[CLEANUP] Error: {str(e)}")

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.TEMP_ENCRYPTED_FOLDER, exist_ok=True)
    os.makedirs(os.path.dirname(Config.KEY_VAULT_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(Config.AUDIT_LOG_PATH), exist_ok=True)
    
    # Cleanup old temp files
    cleanup_old_temp_files()
    
    print("=" * 60)
    print("Intellektual Audit Modeli - Dasturiy Ta'minot Xavfsizligi")
    print("=" * 60)
    print("[OK] Server ishga tushmoqda...")
    print("[OK] Brauzerda quyidagi manzilga o'ting: http://localhost:6001")
    print("[OK] Standart foydalanuvchi: admin / admin123")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=6001)
