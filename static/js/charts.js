$(document).ready(function() {
    const dates = JSON.parse($("#user-date").html().replace(/'/g, '"'));
    const counts = JSON.parse($("#user-count").html());
    const jobDates = JSON.parse($("#job-date").html().replace(/'/g, '"'));
    const jobCounts = JSON.parse($("#job-count").html());
    const incomeDates = JSON.parse($("#income-date").html().replace(/'/g, '"'));
    const incomeCounts = JSON.parse($("#income-count").html());

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
    const ctxJobs = document.getElementById('job-created').getContext('2d');
    const jobCreatedChart = new Chart(ctxJobs, {
        type: 'line',
        data: {
            labels: jobDates,
            datasets: [{
                label: 'Daily Jobs Created',
                data: jobCounts,
                borderColor: 'rgba(153, 102, 255, 1)',
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
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

    const ctxIncome = document.getElementById('job-revenue').getContext('2d');
    const incomeGeneratedChart = new Chart(ctxIncome, {
        type: 'line',
        data: {
            labels: incomeDates,
            datasets: [{
                label: 'Daily Income Generated',
                data: incomeCounts,
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
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


})