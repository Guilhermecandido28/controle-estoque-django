document.addEventListener("DOMContentLoaded", function() {
    // Função para carregar dados via AJAX
    function loadChartData() {
                
        fetch('/dashboard/vendasxfp_dia/')            
            .then(response => response.json())
            .then(dataFromServer => {
                // Extrair labels e valores dos dados recebidos
                var labels = Object.keys(dataFromServer);
                var dataValues = Object.values(dataFromServer);                
                // Cores para o gráfico
                var colors = [
                    'rgb(54, 162, 235)',   // Para PIX
                    'rgb(75, 192, 192)',   // Para Dinheiro
                    'rgb(255, 205, 86)',   // Para Cartão
                    'rgb(255, 99, 132)'    // Para Débito
                ];
                

                // Doughnut chart
                new Chart(document.getElementById("chartjs-dashboard-pie"), {
                    type: "pie",        
                    data: {
                        labels: labels,
                        datasets: [{
                            data: dataValues,
                            backgroundColor: colors,
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: !window.MSInputMethodContext,
                        maintainAspectRatio: false,
                        legend: {
                            display: false
                        },
                        cutoutPercentage: 75
                    }
                });
            })
            .catch(error => {
                console.error('Erro ao carregar dados:', error);
            });
    }

    // Carregar os dados ao carregar a página
    loadChartData();
});
