console.log('DETALHES DASHBOARD');

    const dashboardSlug = document.getElementById("dashboard-slug").textContent.trim();
    const submitBtn =  document.getElementById("submit-btn")
    const dataInput = document.getElementById("data-input");
    const user = document.getElementById("user").textContent.trim();
    const dataBox = document.getElementById("data-box");

    const socket = new WebSocket(`ws://${window.location.host}/ws/${dashboardSlug}/`);     //const socket = new WebSocket('ws://'+ window.location.host + '/ws/abc/');
    console.log(socket);

    socket.onmessage = function(e) {
        console.log('Server: ' + e.data);
        const {sender, message} = JSON.parse(e.data);
        console.log(sender);
        console.log(message);
        dataBox.innerHTML+=`<p>${sender}: ${message}</p>` ;
        updateChart();
    };

    submitBtn.addEventListener('click', ()=>{
        const dataValue = dataInput.value;
        socket.send(JSON.stringify({
            'message': dataValue,
            'sender': user,
        }));        

        dataInput.value = '';

    });

    const ctx = document.getElementById('myChart').getContext("2d");
    let chart;

    const fetchChartData = async() => {
        const response = await fetch(window.location.href+'/chart/');
        const data = await response.json();

        return data;
    }


    const drawChart = async() => {
        const data = await fetchChartData();
        const {chartData, chartLabels} = data

        chart = new Chart (ctx, {
        type: 'pie',
        data: {
            labels: chartLabels,
            datasets: [{
                label: '% of contribution',
                data: chartData,
                borderWidth: 1
            }]
        },        
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
       });    
    }

    const updateChart = async()=>{
        if(chart){
            chart.destroy();
        }

        await drawChart();
    }

    drawChart();