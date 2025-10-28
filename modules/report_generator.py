from datetime import datetime
import os

# Try to import WeasyPrint, use ReportLab as fallback
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        REPORTLAB_AVAILABLE = True
    except ImportError:
        REPORTLAB_AVAILABLE = False

class ReportGenerator:
    def __init__(self):
        self.template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Encryption Analysis Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 40px;
            color: #333;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 3px solid #4F46E5;
            padding-bottom: 20px;
        }
        .header h1 {
            color: #4F46E5;
            margin-bottom: 10px;
        }
        .header p {
            color: #666;
            font-size: 14px;
        }
        .section {
            margin-bottom: 30px;
        }
        .section h2 {
            color: #4F46E5;
            border-bottom: 2px solid #E0E7FF;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #4F46E5;
            color: white;
            font-weight: 600;
        }
        tr:hover {
            background-color: #F5F7FF;
        }
        .metric-card {
            background: #F5F7FF;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .metric-card h3 {
            color: #4F46E5;
            margin-top: 0;
        }
        .best-algorithm {
            background: #10B981;
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
        .footer {
            margin-top: 50px;
            text-align: center;
            color: #666;
            font-size: 12px;
            border-top: 1px solid #ddd;
            padding-top: 20px;
        }
        .score-high {
            color: #10B981;
            font-weight: bold;
        }
        .score-medium {
            color: #F59E0B;
            font-weight: bold;
        }
        .score-low {
            color: #EF4444;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 Intellektual Audit Modeli</h1>
        <h2>Shifrlash Algoritmlari Tahlil Hisoboti</h2>
        <p>Yaratilgan sana: {date}</p>
    </div>
    
    <div class="section">
        <h2>📊 Umumiy Natijalar</h2>
        <div class="best-algorithm">
            Eng Samarali Algoritm: {best_algorithm}
        </div>
    </div>
    
    <div class="section">
        <h2>📈 Algoritmlar Taqqoslash Jadvali</h2>
        <table>
            <thead>
                <tr>
                    <th>Algoritm</th>
                    <th>Umumiy Ball (S)</th>
                    <th>Tezlik (T)</th>
                    <th>Xavfsizlik (E)</th>
                    <th>Kalit Boshqaruv (K)</th>
                    <th>Yaxlitlik (I)</th>
                </tr>
            </thead>
            <tbody>
                {comparison_rows}
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>🔍 Batafsil Tahlil</h2>
        {detailed_metrics}
    </div>
    
    <div class="section">
        <h2>⚡ Ishlash Ko'rsatkichlari</h2>
        <table>
            <thead>
                <tr>
                    <th>Algoritm</th>
                    <th>Shifrlash Vaqti (ms)</th>
                    <th>Deshifrlash Vaqti (ms)</th>
                    <th>CPU (%)</th>
                    <th>RAM (MB)</th>
                </tr>
            </thead>
            <tbody>
                {performance_rows}
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>🔐 Xavfsizlik Ko'rsatkichlari</h2>
        <table>
            <thead>
                <tr>
                    <th>Algoritm</th>
                    <th>Kalit Hajmi (bit)</th>
                    <th>Entropiya</th>
                    <th>Xavfsizlik Darajasi</th>
                    <th>Yaxlitlik Tekshiruvi</th>
                </tr>
            </thead>
            <tbody>
                {security_rows}
            </tbody>
        </table>
    </div>
    
    <div class="footer">
        <p>Bu hisobot Intellektual Audit Modeli tomonidan avtomatik yaratilgan</p>
        <p>© 2024 Dasturiy Ta'minot Xavfsizligi Tahlil Tizimi</p>
    </div>
</body>
</html>
        """
    
    def generate_html_report(self, results, output_path=None):
        """
        Generate HTML report from analysis results
        """
        if not results:
            return None
        
        # Determine best algorithm
        best_algorithm = max(results, key=lambda x: x['S_overall_score'])['algorithm']
        
        # Generate comparison rows
        comparison_rows = ""
        for result in sorted(results, key=lambda x: x['S_overall_score'], reverse=True):
            score_class = self._get_score_class(result['S_overall_score'])
            comparison_rows += f"""
                <tr>
                    <td><strong>{result['algorithm']}</strong></td>
                    <td class="{score_class}">{result['S_overall_score']:.4f}</td>
                    <td>{result['T_performance']:.4f}</td>
                    <td>{result['E_security']:.4f}</td>
                    <td>{result['K_key_management']:.4f}</td>
                    <td>{result['I_integrity']:.4f}</td>
                </tr>
            """
        
        # Generate detailed metrics
        detailed_metrics = ""
        for result in results:
            detailed_metrics += f"""
                <div class="metric-card">
                    <h3>{result['algorithm']}</h3>
                    <p><strong>Umumiy Ball:</strong> {result['S_overall_score']:.4f}</p>
                    <p><strong>Shifrlash Vaqti:</strong> {result['encryption_time_ms']:.4f} ms</p>
                    <p><strong>Deshifrlash Vaqti:</strong> {result['decryption_time_ms']:.4f} ms</p>
                    <p><strong>CPU Yuklanishi:</strong> {result['avg_cpu_percent']:.2f}%</p>
                    <p><strong>RAM Sarfi:</strong> {result['avg_memory_mb']:.4f} MB</p>
                    <p><strong>Entropiya:</strong> {result['entropy']:.4f}</p>
                    <p><strong>Kalit Hajmi:</strong> {result['key_size']} bit</p>
                </div>
            """
        
        # Generate performance rows
        performance_rows = ""
        for result in results:
            performance_rows += f"""
                <tr>
                    <td><strong>{result['algorithm']}</strong></td>
                    <td>{result['encryption_time_ms']:.4f}</td>
                    <td>{result['decryption_time_ms']:.4f}</td>
                    <td>{result['avg_cpu_percent']:.2f}</td>
                    <td>{result['avg_memory_mb']:.4f}</td>
                </tr>
            """
        
        # Generate security rows
        security_rows = ""
        for result in results:
            integrity = "✓ Muvaffaqiyatli" if result['integrity_check'] else "✗ Xato"
            security_rows += f"""
                <tr>
                    <td><strong>{result['algorithm']}</strong></td>
                    <td>{result['key_size']}</td>
                    <td>{result['entropy']:.4f}</td>
                    <td>{result['security_level']}</td>
                    <td>{integrity}</td>
                </tr>
            """
        
        # Fill template
        html_content = self.template.format(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            best_algorithm=best_algorithm,
            comparison_rows=comparison_rows,
            detailed_metrics=detailed_metrics,
            performance_rows=performance_rows,
            security_rows=security_rows
        )
        
        # Save HTML if output path provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        return html_content
    
    def generate_pdf_report(self, results, output_path):
        """
        Generate PDF report from analysis results
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        if WEASYPRINT_AVAILABLE:
            # Use WeasyPrint if available
            html_content = self.generate_html_report(results)
            if html_content:
                HTML(string=html_content).write_pdf(output_path)
                return output_path
        elif REPORTLAB_AVAILABLE:
            # Use ReportLab as fallback
            return self._generate_pdf_with_reportlab(results, output_path)
        else:
            raise ImportError("Neither WeasyPrint nor ReportLab is available for PDF generation")
        
        return None
    
    def _generate_pdf_with_reportlab(self, results, output_path):
        """
        Generate PDF using ReportLab (fallback method)
        """
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#4F46E5'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#4F46E5'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph("🧠 Intellektual Audit Modeli", title_style))
        story.append(Paragraph("Shifrlash Algoritmlari Tahlil Hisoboti", styles['Heading2']))
        story.append(Paragraph(f"Yaratilgan sana: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Best Algorithm
        best_algorithm = max(results, key=lambda x: x['S_overall_score'])['algorithm']
        story.append(Paragraph("📊 Umumiy Natijalar", heading_style))
        best_para = Paragraph(f"<b>Eng Samarali Algoritm: {best_algorithm}</b>", styles['Normal'])
        story.append(best_para)
        story.append(Spacer(1, 20))
        
        # Comparison Table
        story.append(Paragraph("📈 Algoritmlar Taqqoslash Jadvali", heading_style))
        
        table_data = [['Algoritm', 'S', 'T', 'E', 'K', 'I']]
        for result in sorted(results, key=lambda x: x['S_overall_score'], reverse=True):
            table_data.append([
                result['algorithm'],
                f"{result['S_overall_score']:.4f}",
                f"{result['T_performance']:.4f}",
                f"{result['E_security']:.4f}",
                f"{result['K_key_management']:.4f}",
                f"{result['I_integrity']:.4f}"
            ])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Performance Table
        story.append(Paragraph("⚡ Ishlash Ko'rsatkichlari", heading_style))
        
        perf_data = [['Algoritm', 'Shifr (ms)', 'Deshifr (ms)', 'CPU (%)', 'RAM (MB)']]
        for result in results:
            perf_data.append([
                result['algorithm'],
                f"{result['encryption_time_ms']:.4f}",
                f"{result['decryption_time_ms']:.4f}",
                f"{result['avg_cpu_percent']:.2f}",
                f"{result['avg_memory_mb']:.4f}"
            ])
        
        perf_table = Table(perf_data)
        perf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(perf_table)
        story.append(Spacer(1, 20))
        
        # Security Table
        story.append(Paragraph("🔐 Xavfsizlik Ko'rsatkichlari", heading_style))
        
        sec_data = [['Algoritm', 'Kalit (bit)', 'Entropiya', 'Daraja', 'Yaxlitlik']]
        for result in results:
            integrity = "✓" if result['integrity_check'] else "✗"
            sec_data.append([
                result['algorithm'],
                str(result['key_size']),
                f"{result['entropy']:.4f}",
                result['security_level'],
                integrity
            ])
        
        sec_table = Table(sec_data)
        sec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(sec_table)
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("Bu hisobot Intellektual Audit Modeli tomonidan avtomatik yaratilgan", styles['Normal']))
        story.append(Paragraph("© 2024 Dasturiy Ta'minot Xavfsizligi Tahlil Tizimi", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def _get_score_class(self, score):
        """Get CSS class based on score value"""
        if score >= 0.7:
            return "score-high"
        elif score >= 0.4:
            return "score-medium"
        else:
            return "score-low"
