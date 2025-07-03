let temperatureChart = null;

async function loadCurrent() {
    try {
        const response = await fetch('/api/current');
        const data = await response.json();
        
        document.getElementById('current-temp').textContent = 
            data.temperature_c ? `${Math.round(data.temperature_c)}°C` : '--°C';
        document.getElementById('current-humidity').textContent = 
            data.humidity ? `${Math.round(data.humidity)}%` : '--%';
        document.getElementById('target-temp').textContent = 
            data.target_temperature_c ? `${Math.round(data.target_temperature_c)}°C` : '--°C';
        document.getElementById('hvac-status').textContent = 
            data.hvac_state || '--';
    } catch (error) {
        console.error('Error loading current data:', error);
    }
}

async function loadStatistics(hours) {
    try {
        const response = await fetch(`/api/statistics?hours=${hours}`);
        const data = await response.json();
        
        document.getElementById('avg-temp').textContent = 
            data.avg_temperature ? `${data.avg_temperature}°C` : '--°C';
        document.getElementById('min-temp').textContent = 
            data.min_temperature ? `${data.min_temperature}°C` : '--°C';
        document.getElementById('max-temp').textContent = 
            data.max_temperature ? `${data.max_temperature}°C` : '--°C';
        document.getElementById('avg-humidity').textContent = 
            data.avg_humidity ? `${data.avg_humidity}%` : '--%';
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

async function loadData(hours, buttonElement = null) {
    // Update active button
    document.querySelectorAll('.time-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // If called from button click, use the button element
    // Otherwise, find the button with matching hours
    if (buttonElement) {
        buttonElement.classList.add('active');
    } else {
        // Find button with matching hours value
        document.querySelectorAll('.time-btn').forEach(btn => {
            if ((hours === 6 && btn.textContent === '6 Hours') ||
                (hours === 12 && btn.textContent === '12 Hours') ||
                (hours === 24 && btn.textContent === '24 Hours') ||
                (hours === 48 && btn.textContent === '48 Hours') ||
                (hours === 168 && btn.textContent === '1 Week')) {
                btn.classList.add('active');
            }
        });
    }
    
    try {
        const response = await fetch(`/api/temperatures?hours=${hours}`);
        const data = await response.json();
        
        updateChart(data);
        await loadStatistics(hours);
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

function updateChart(data) {
    const ctx = document.getElementById('temperatureChart').getContext('2d');
    
    // Create annotations for HVAC states
    const annotations = [];
    let currentAnnotation = null;
    
    data.forEach((point, index) => {
        const hvacState = point.hvac_state;
        const timestamp = new Date(point.timestamp).toLocaleString();
        
        if (hvacState === 'HEATING' || hvacState === 'COOLING') {
            if (!currentAnnotation || currentAnnotation.type !== hvacState) {
                // Start new annotation
                currentAnnotation = {
                    type: hvacState,
                    startIndex: index,
                    endIndex: index,
                    startLabel: timestamp,
                    endLabel: timestamp
                };
            } else {
                // Extend current annotation
                currentAnnotation.endIndex = index;
                currentAnnotation.endLabel = timestamp;
            }
        } else {
            // End current annotation if exists
            if (currentAnnotation) {
                annotations.push({
                    type: 'box',
                    xMin: currentAnnotation.startIndex,
                    xMax: currentAnnotation.endIndex,
                    backgroundColor: currentAnnotation.type === 'HEATING' 
                        ? 'rgba(255, 99, 71, 0.2)'  // Tomato for heating
                        : 'rgba(135, 206, 235, 0.2)', // Sky blue for cooling
                    borderColor: currentAnnotation.type === 'HEATING'
                        ? 'rgba(255, 99, 71, 0.5)'
                        : 'rgba(135, 206, 235, 0.5)',
                    borderWidth: 1,
                    label: {
                        content: currentAnnotation.type,
                        enabled: false
                    }
                });
                currentAnnotation = null;
            }
        }
    });
    
    // Add final annotation if exists
    if (currentAnnotation) {
        annotations.push({
            type: 'box',
            xMin: currentAnnotation.startIndex,
            xMax: currentAnnotation.endIndex,
            backgroundColor: currentAnnotation.type === 'HEATING' 
                ? 'rgba(255, 99, 71, 0.2)'
                : 'rgba(135, 206, 235, 0.2)',
            borderColor: currentAnnotation.type === 'HEATING'
                ? 'rgba(255, 99, 71, 0.5)'
                : 'rgba(135, 206, 235, 0.5)',
            borderWidth: 1,
            label: {
                content: currentAnnotation.type,
                enabled: false
            }
        });
    }
    
    const chartData = {
        labels: data.map(d => new Date(d.timestamp).toLocaleString()),
        datasets: [
            {
                label: 'Temperature (°C)',
                data: data.map(d => d.temperature_c),
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                tension: 0.4,
                yAxisID: 'y-temp'
            },
            {
                label: 'Target Temperature (°C)',
                data: data.map(d => d.target_temperature_c),
                borderColor: '#e74c3c',
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                borderDash: [5, 5],
                tension: 0.4,
                yAxisID: 'y-temp'
            },
            {
                label: 'Humidity (%)',
                data: data.map(d => d.humidity),
                borderColor: '#2ecc71',
                backgroundColor: 'rgba(46, 204, 113, 0.1)',
                tension: 0.4,
                yAxisID: 'y-humidity'
            }
        ]
    };
    
    const config = {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                annotation: {
                    annotations: annotations
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                'y-temp': {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    }
                },
                'y-humidity': {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Humidity (%)'
                    },
                    grid: {
                        drawOnChartArea: false,
                    }
                }
            }
        }
    };
    
    if (temperatureChart) {
        temperatureChart.destroy();
    }
    
    temperatureChart = new Chart(ctx, config);
}

// Initial load
loadCurrent();
loadData(6);
loadStatistics(6);

// Refresh current data every minute
setInterval(loadCurrent, 60000);

// Refresh chart data every 5 minutes
setInterval(() => {
    const activeBtn = document.querySelector('.time-btn.active');
    const hours = parseInt(activeBtn.textContent) || 24;
    loadData(hours);
}, 300000);