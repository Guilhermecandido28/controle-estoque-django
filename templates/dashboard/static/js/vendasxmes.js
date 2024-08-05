document.addEventListener("DOMContentLoaded", function() {
    var ctx = document.getElementById("chartjs-dashboard-line").getContext("2d");
    var gradient = ctx.createLinearGradient(255, 255, 255, 0);
    gradient.addColorStop(0, "rgba(215, 227, 244, 1 )");
    gradient.addColorStop(1, "rgba(215, 227, 244, 0)");
    var gradient_saidas = ctx.createLinearGradient(255, 255, 255, 0);
    gradient_saidas.addColorStop(0, "rgba(248, 198, 200, 1)");
    gradient_saidas.addColorStop(1, "rgba(224, 198, 200, 0)");

    // Função para carregar os dados via AJAX
    function loadChartData() {
        fetch('/dashboard/vendasxmes/')
            .then(response => response.json())
            .then(data => {
                var labels = [];
                var dataValues = [];
                var saidasValues = [];

                // Ajusta os dados para o formato esperado pelo Chart.js
                for (var i = 1; i <= 12; i++) {
                    labels.push(getMonthLabel(i)); // Função para obter label do mês
                    dataValues.push(data.entradas[i.toString()] ? data.entradas[i.toString()] : null);
                    saidasValues.push(data.saidas[i.toString()] ? data.saidas[i.toString()] : null);
                }

                // Cria o gráfico com os dados carregados
                createChart(labels, dataValues, saidasValues); // Passe todos os argumentos necessários aqui
            })
            .catch(error => {
                console.error('Erro ao carregar dados:', error);
            });
    }

    // Função para criar o gráfico com os dados
    function createChart(labels, dataValues, saidasValues) { // Adicione o argumento saidasValues
        new Chart(ctx, {
            plugins: [ChartDataLabels],
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Entradas R$",
                    fill: true,
                    backgroundColor: gradient,
                    borderColor: 'rgb(54, 162, 235)',
                    data: dataValues
                }, {
                    label: "Saídas R$",
                    fill: true,
                    backgroundColor: gradient_saidas,
                    borderColor: 'red',
                    data: saidasValues,
                }]
            },
            options: {
                plugins: {
                    filler: {
                        propagate: false
                    },
                    datalabels: {
                        color: 'black',
                        formatter: function(value, context) {
                            return 'R$ ' + value.toFixed(2).replace('.', ','); // Formata o valor para R$ XX,XX
                        },
                        anchor: 'end',
                        align: 'top',
                        offset: 2,
                        font: {
                            weight: 'bold'
                        }
                    }
                },
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                tooltips: {
                    intersect: false
                },
                hover: {
                    intersect: true
                },
                scales: {
                    xAxes: [{
                        reverse: true,
                        gridLines: {
                            color: "rgba(0,0,0,0.0)"
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            stepSize: 1000,
                            callback: function(value, index, values) {
                                return 'R$ ' + value.toFixed(2).replace('.', ','); // Formata o tick do eixo Y
                            }
                        },
                        display: true,
                        borderDash: [3, 3],
                        gridLines: {
                            color: "rgba(0,0,0,0.0)"
                        }
                    }]
                }
            }
        });
    }

    // Função para obter o label do mês com base no número do mês
    function getMonthLabel(monthNumber) {
        var monthNames = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
        return monthNames[monthNumber - 1];
    }

    // Carrega os dados ao carregar a página
    loadChartData();
});
