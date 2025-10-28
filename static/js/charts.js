// Chart.js Configuration and Utilities

// Default Chart.js configuration
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.color = '#6B7280';

// Check if dark mode is enabled
function isDarkMode() {
    return document.documentElement.classList.contains('dark');
}

// Update chart colors based on theme
function updateChartColors() {
    if (isDarkMode()) {
        Chart.defaults.color = '#9CA3AF';
        Chart.defaults.borderColor = '#374151';
    } else {
        Chart.defaults.color = '#6B7280';
        Chart.defaults.borderColor = '#E5E7EB';
    }
}

// Initialize chart colors
updateChartColors();

// Listen for theme changes
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.attributeName === 'class') {
            updateChartColors();
        }
    });
});

observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
});

// Utility function to format numbers
function formatNumber(num, decimals = 2) {
    return Number(num).toFixed(decimals);
}

// Utility function to get color based on score
function getScoreColor(score) {
    if (score >= 0.7) return '#10B981'; // Green
    if (score >= 0.4) return '#F59E0B'; // Yellow
    return '#EF4444'; // Red
}

// Export chart as image
function exportChartAsImage(chartId, filename = 'chart.png') {
    const canvas = document.getElementById(chartId);
    if (canvas) {
        const url = canvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.download = filename;
        link.href = url;
        link.click();
    }
}

// Responsive chart options
const responsiveOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
        legend: {
            display: true,
            position: 'bottom',
            labels: {
                padding: 15,
                usePointStyle: true,
                font: {
                    size: 12,
                    weight: '500'
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 12,
            cornerRadius: 8,
            titleFont: {
                size: 14,
                weight: 'bold'
            },
            bodyFont: {
                size: 13
            },
            callbacks: {
                label: function(context) {
                    let label = context.dataset.label || '';
                    if (label) {
                        label += ': ';
                    }
                    if (context.parsed.y !== null) {
                        label += formatNumber(context.parsed.y, 4);
                    }
                    return label;
                }
            }
        }
    },
    animation: {
        duration: 1000,
        easing: 'easeInOutQuart'
    }
};

// Algorithm colors
const algorithmColors = {
    'AES': {
        background: 'rgba(59, 130, 246, 0.8)',
        border: 'rgb(59, 130, 246)'
    },
    'DES': {
        background: 'rgba(239, 68, 68, 0.8)',
        border: 'rgb(239, 68, 68)'
    },
    'Blowfish': {
        background: 'rgba(251, 146, 60, 0.8)',
        border: 'rgb(251, 146, 60)'
    },
    'ChaCha20': {
        background: 'rgba(168, 85, 247, 0.8)',
        border: 'rgb(168, 85, 247)'
    }
};

// Get color for algorithm
function getAlgorithmColor(algorithm, type = 'background') {
    return algorithmColors[algorithm]?.[type] || 'rgba(100, 100, 100, 0.8)';
}

console.log('Charts.js loaded successfully');
