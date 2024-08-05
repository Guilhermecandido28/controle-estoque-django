window.theme = {
    primary: "#3B7DDD",
    secondary: "#6c757d",
    success: "#1cbb8c",
    info: "#17a2b8",
    warning: "#fcb92c",
    danger: "#dc3545",
    white: "#fff",
    "gray-100": "#f8f9fa",
    "gray-200": "#e9ecef",
    "gray-300": "#dee2e6",
    "gray-400": "#ced4da",
    "gray-500": "#adb5bd",
    "gray-600": "#6c757d",
    "gray-700": "#495057",
    "gray-800": "#343a40",
    "gray-900": "#212529",
    black: "#000"
}

document.addEventListener("DOMContentLoaded", function() {
    function loadChartData() {
        fetch('/dashboard/vendasxdia/')
            .then(response => response.json())
            .then(data => {
                var labels = [];
                var dataValuesSemanaPassada = [];
                var dataValuesSemanaAtual = [];
                var dataValuesSaidas = [];

                // Ajusta os dados para o formato esperado pelo Chart.js
                for (var i = 0; i < 7; i++) {
                    labels.push(getDayLabel(i)); // Função para obter label do dia da semana
                    dataValuesSemanaPassada.push(data.semana_passada[i+1] ? data.semana_passada[i+1] : null); // i+1 porque ExtractWeekDay retorna 1 para domingo, 2 para segunda, etc.
                    dataValuesSemanaAtual.push(data.semana_atual[i+1] ? data.semana_atual[i+1] : null);
                    dataValuesSaidas.push(data.saidas[i+1] ? data.saidas[i+1] : null);
                }

                // Cria o gráfico com os dados carregados
                createChart(labels, dataValuesSemanaPassada, dataValuesSemanaAtual, dataValuesSaidas);
            })
            .catch(error => {
                console.error('Erro ao carregar dados:', error);
            });
    }

    function createChart(labels, dataValuesSemanaPassada, dataValuesSemanaAtual, dataValuesSaidas) {
        // Bar chart
        new Chart(document.getElementById("chartjs-bar"), {
            plugins: [ChartDataLabels],
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Semana Atual",
                    backgroundColor: window.theme.success,
                    borderColor: window.theme.success,
                    hoverBackgroundColor: window.theme.success,
                    hoverBorderColor: window.theme.success,
                    data: dataValuesSemanaAtual,
                    barPercentage: .75,
                    categoryPercentage: .8
                }, {
                    label: "Semana Passada",
                    backgroundColor: "#dee2e6",
                    borderColor: "#dee2e6",
                    hoverBackgroundColor: "#dee2e6",
                    hoverBorderColor: "#dee2e6",
                    data: dataValuesSemanaPassada,
                    barPercentage: .75,
                    categoryPercentage: .8
                }, {
                    label: "Saídas Semana Atual",
                    backgroundColor: window.theme.danger,
                    borderColor: window.theme.danger,
                    hoverBackgroundColor: window.theme.danger,
                    hoverBorderColor: window.theme.danger,
                    data: dataValuesSaidas,
                    barPercentage: .75,
                    categoryPercentage: .8
                }]
            },
            options: {
                plugins: {                    
                    datalabels: {
                        color: 'black',
                        formatter: function(value, context) {
                            if (value !== null) {
                                return 'R$ ' + value.toFixed(2).replace('.', ','); // Formata o valor para R$ XX,XX
                            } else {
                                return ''; // Ou qualquer valor padrão desejado
                            }
                        },
                        anchor: 'center',
                        align: 'center',
                        offset: 0,
                        font: {
                            weight: 'bold'
                        }
                    }
                },                    
                maintainAspectRatio: false,
                legend: {
                    display: false,
                                        
                },

                scales: {
                    yAxes: [{
                        gridLines: {
                            display: false
                        },
                        stacked: false,
                        ticks: {
                            stepSize: 40
                        }
                    }],
                    xAxes: [{
                        stacked: false,
                        gridLines: {
                            color: "transparent"
                        }
                    }]
                }
            }
        });
    }

    // Função para obter o label do dia da semana com base no número do dia (0 para Domingo, 1 para Segunda, etc.)
    function getDayLabel(dayNumber) {
        var dayNames = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
        return dayNames[dayNumber];
    }

    // Carrega os dados ao carregar a página
    loadChartData();
});
