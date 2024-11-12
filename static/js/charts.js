
// Gráfico de barras para denuncias mensuales
const ctxMonthly = document.getElementById('monthlyChart').getContext('2d');
const monthlyChart = new Chart(ctxMonthly, {
    type: 'bar',
    data: {
        labels: labelsMeses,
        datasets: [{
            label: 'Denuncias por Mes',
            data: datosMensuales,
            backgroundColor: 'rgba(255, 140, 0, 0.7)',
            borderColor: 'rgba(255, 140, 0, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top'
            },
            datalabels: {
                anchor: 'end',
                align: 'top',
                formatter: (value) => value,
                color: 'black',
                font: {
                    weight: 'bold'
                }
            }
        }
    }
});

// Gráfico de torta para la distribución de tipos de denuncias
const ctxType = document.getElementById('typeChart').getContext('2d');
const typeChart = new Chart(ctxType, {
    type: 'pie',
    data: {
        labels: labelsTipos,
        datasets: [{
            label: 'Tipos de Denuncias',
            data: datosTipos,
            backgroundColor: ['#ff8c00', '#ffd700', '#ff4500', '#ff6347'],
            hoverBackgroundColor: ['#ff7518', '#e6ac00', '#e63900', '#e55b3c']
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top'
            },
            datalabels: {
                formatter: (value, context) => `${value}`,
                color: 'black',
                font: {
                    weight: 'bold'
                }
            }
        }
    }
});

// Gráfico de dona para la distribución de estados de denuncias
const ctxStatus = document.getElementById('statusChart').getContext('2d');
const statusChart = new Chart(ctxStatus, {
    type: 'doughnut',
    data: {
        labels: labelsEstados,
        datasets: [{
            label: 'Estados de Denuncias',
            data: datosEstados,
            backgroundColor: ['#ff8c00', '#ffd700', '#ff4500'],
            hoverBackgroundColor: ['#ff7518', '#e6ac00', '#e63900']
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top'
            },
            datalabels: {
                formatter: (value, context) => `${value}`,
                color: 'black',
                font: {
                    weight: 'bold'
                }
            }
        }
    }
});

// Gráfico de líneas para la tendencia mensual de denuncias
const ctxLine = document.getElementById('lineChart').getContext('2d');
const lineChart = new Chart(ctxLine, {
    type: 'line',
    data: {
        labels: labelsMeses,  // Etiquetas de los meses
        datasets: [{
            label: 'Tendencia de Denuncias Mensuales',
            data: datosLinea,  // Datos de denuncias por mes
            borderColor: 'rgba(255, 140, 0, 1)',
            backgroundColor: 'rgba(255, 140, 0, 0.2)',
            borderWidth: 2,
            fill: true,
            tension: 0.4  // Hace la línea un poco más curva
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top'
            },
            datalabels: {
                anchor: 'end',
                align: 'top',
                formatter: (value) => value,
                color: 'black',
                font: {
                    weight: 'bold'
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});


