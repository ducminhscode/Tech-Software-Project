function drawMedicineStats(labels, data) {

    const ctx = document.getElementById('medicineChart');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: 'Số lượng',
                data: data,
                borderWidth: 2,
                backgroundColor: ["rgba(255, 87, 51, 0.8)", "rgba(51, 255, 87, 0.8)", "rgba(51, 87, 255, 0.8)", "rgba(255, 51, 161, 0.8)",
                                  "rgba(161, 51, 255, 0.8)", "rgba(51, 255, 245, 0.8)", "rgba(245, 255, 51, 0.8)", "rgba(255, 140, 51, 0.8)",
                                  "rgba(140, 255, 51, 0.8)", "rgba(51, 140, 255, 0.8)", "rgba(255, 51, 140, 0.8)", "rgba(140, 51, 255, 0.8)",
                                  "rgba(51, 255, 140, 0.8)", "rgba(255, 199, 51, 0.8)", "rgba(199, 51, 255, 0.8)", "rgba(51, 199, 255, 0.8)",
                                  "rgba(255, 51, 199, 0.8)", "rgba(255, 111, 51, 0.8)", "rgba(111, 255, 51, 0.8)", "rgba(51, 111, 255, 0.8)",
                                  "rgba(255, 51, 111, 0.8)", "rgba(111, 51, 255, 0.8)", "rgba(51, 255, 111, 0.8)", "rgba(255, 214, 51, 0.8)",
                                  "rgba(214, 51, 255, 0.8)", "rgba(51, 214, 255, 0.8)", "rgba(255, 51, 214, 0.8)", "rgba(255, 165, 51, 0.8)",
                                  "rgba(165, 255, 51, 0.8)", "rgba(51, 165, 255, 0.8)", "rgba(255, 51, 165, 0.8)"],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: 'white',
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        color: 'white'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

function drawRevenueStats(labels, data) {

    const ctx = document.getElementById('revenueChart');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: 'Doanh thu',
                data: data,
                borderWidth: 2,
                backgroundColor: ["rgba(255, 87, 51, 0.8)", "rgba(51, 255, 87, 0.8)", "rgba(51, 87, 255, 0.8)", "rgba(255, 51, 161, 0.8)",
                                  "rgba(161, 51, 255, 0.8)", "rgba(51, 255, 245, 0.8)", "rgba(245, 255, 51, 0.8)", "rgba(255, 140, 51, 0.8)",
                                  "rgba(140, 255, 51, 0.8)", "rgba(51, 140, 255, 0.8)", "rgba(255, 51, 140, 0.8)", "rgba(140, 51, 255, 0.8)",
                                  "rgba(51, 255, 140, 0.8)", "rgba(255, 199, 51, 0.8)", "rgba(199, 51, 255, 0.8)", "rgba(51, 199, 255, 0.8)",
                                  "rgba(255, 51, 199, 0.8)", "rgba(255, 111, 51, 0.8)", "rgba(111, 255, 51, 0.8)", "rgba(51, 111, 255, 0.8)",
                                  "rgba(255, 51, 111, 0.8)", "rgba(111, 51, 255, 0.8)", "rgba(51, 255, 111, 0.8)", "rgba(255, 214, 51, 0.8)",
                                  "rgba(214, 51, 255, 0.8)", "rgba(51, 214, 255, 0.8)", "rgba(255, 51, 214, 0.8)", "rgba(255, 165, 51, 0.8)",
                                  "rgba(165, 255, 51, 0.8)", "rgba(51, 165, 255, 0.8)", "rgba(255, 51, 165, 0.8)"],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: 'white',
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        color: 'white'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

function drawFrequencyStats(labels, data) {

    const ctx = document.getElementById('frequencyChart');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: 'Tỷ lệ',
                data: data,
                borderWidth: 2,
                backgroundColor: ["rgba(255, 87, 51, 0.8)", "rgba(51, 255, 87, 0.8)", "rgba(51, 87, 255, 0.8)", "rgba(255, 51, 161, 0.8)",
                                  "rgba(161, 51, 255, 0.8)", "rgba(51, 255, 245, 0.8)", "rgba(245, 255, 51, 0.8)", "rgba(255, 140, 51, 0.8)",
                                  "rgba(140, 255, 51, 0.8)", "rgba(51, 140, 255, 0.8)", "rgba(255, 51, 140, 0.8)", "rgba(140, 51, 255, 0.8)",
                                  "rgba(51, 255, 140, 0.8)", "rgba(255, 199, 51, 0.8)", "rgba(199, 51, 255, 0.8)", "rgba(51, 199, 255, 0.8)",
                                  "rgba(255, 51, 199, 0.8)", "rgba(255, 111, 51, 0.8)", "rgba(111, 255, 51, 0.8)", "rgba(51, 111, 255, 0.8)",
                                  "rgba(255, 51, 111, 0.8)", "rgba(111, 51, 255, 0.8)", "rgba(51, 255, 111, 0.8)", "rgba(255, 214, 51, 0.8)",
                                  "rgba(214, 51, 255, 0.8)", "rgba(51, 214, 255, 0.8)", "rgba(255, 51, 214, 0.8)", "rgba(255, 165, 51, 0.8)",
                                  "rgba(165, 255, 51, 0.8)", "rgba(51, 165, 255, 0.8)", "rgba(255, 51, 165, 0.8)"],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: 'white',
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        color: 'white'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}