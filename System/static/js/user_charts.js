$(document).ready(function() {
    const dates = JSON.parse($("#user-date").html().replace(/'/g, '"'));
    const counts = JSON.parse($("#user-count").html());
    const employer_count = JSON.parse($('#employers').html())
    const worker_count = JSON.parse($('#workers').html())

    const ctx = document.getElementById('registered-users').getContext('2d');
    const userRegistrationChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,  
            datasets: [{
                label: 'Daily User Registrations',
                data: counts,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        }
    });

    const barCTX = document.getElementById("user-types").getContext('2d');
    const workerTypeChart = new Chart(barCTX, {
        type: 'bar',
        data: {
            labels: ['Workers', 'Employers'],
            datasets: [{
                label: '',
                data: [worker_count, employer_count],
                backgroundColor: ['rgba(75, 192, 192, 0.7)', 'rgba(255, 159, 64, 0.7)'],
                borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 159, 64, 1)'],
                borderWidth: 1  
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Worker vs Employers'
                }
            }
        }
    })
})