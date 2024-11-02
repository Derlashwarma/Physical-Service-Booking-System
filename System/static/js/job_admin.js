$(document).ready(function(){
    const jobDates = JSON.parse($("#job-date").html().replace(/'/g, '"'));
    const jobCounts = JSON.parse($("#job-count").html());

    const ctxJobs = document.getElementById('job-created').getContext('2d');
    new Chart(ctxJobs, {
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

    const label = JSON.parse($("#label").html().replace(/'/g, '"'));
    const count = JSON.parse($("#count").html());

    function getRandomColor() {
        const r = Math.floor(Math.random() * 256);
        const g = Math.floor(Math.random() * 256);
        const b = Math.floor(Math.random() * 256);
        return `rgba(${r}, ${g}, ${b}, 0.75)`;
    }

    const colors = count.map(()=>getRandomColor());

    const barCTX = document.getElementById("job-tags").getContext('2d');
    new Chart(barCTX, {
        type: 'bar',
        data: {
            labels: label,
            datasets: [{
                label: '',
                data: count,
                borderWidth: 1,
                backgroundColor: colors,
                borderColor: colors,
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Post Tags'
                }
            }
        }
    })
})