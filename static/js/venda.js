function renderiza_grafico1() {
  const ctx = document.getElementById('dashbord1').getContext('2d');

  
  fetch('movimentacao_dia')
      .then(response => response.json())
      .then(data => {
          const cores = {
              'CARTAO': 'blue',
              'DEBITO': 'green',
              'PIX': 'orange',
              'DINHEIRO': 'red'
          };

          
          const formas_pagamento = {};
          const totais_vendas = {};
          data.forEach(item => {
              formas_pagamento[item.forma_pagamento] = true;
              if (!totais_vendas[item.forma_pagamento]) {
                  totais_vendas[item.forma_pagamento] = 0;
              }
              totais_vendas[item.forma_pagamento] += parseFloat(item.soma_total);
          });

          // Converte os objetos em arrays para serem usados no gráfico
          const labels = Object.keys(formas_pagamento);
          const valores = labels.map(label => totais_vendas[label]);

          // Cria o gráfico
          const myChart = new Chart(ctx, {
              type: 'pie',
              data: {
                  labels: labels,
                  datasets: [{
                      label: 'Vendas',
                      data: valores,
                      backgroundColor: labels.map(label => cores[label]),
                      borderColor: 'black',
                      borderWidth: 1,
                      borderRadius: 15,
                      inflateAmount: 0.2,
                  }]
              },
              options: {
                  plugins: {
                      title: {
                          display: true,
                          text: "Vendas R$ x Forma de Pagamento",
                          color: 'black'
                      },
                      legend: {
                          display: true,
                      }
                  }
              }
          });
      })
      .catch(error => {
          console.error('Ocorreu um erro ao buscar os dados de movimentação do dia:', error);
      });
}


// Função para calcular o preço total para uma linha da tabela
function calcularPrecoTotal(row) {
  // console.log('Início do cálculo do preço total');
  var quantidadeElement = row.querySelector('.quantidade');
  var precoElement = row.querySelector('.preco');
  if (!quantidadeElement || !precoElement) {
      // console.error('Erro: Elementos de quantidade ou preço não encontrados.');
      return 0;
  }
  var quantidade = parseInt(quantidadeElement.textContent);
  var precoUnitario = parseFloat(precoElement.textContent.replace('R$', '').replace(',', '.'));
  // console.log('Quantidade:', quantidade);
  // console.log('Preço unitário:', precoUnitario);
  var precoTotal = precoUnitario;
  // console.log('Preço total:', precoTotal);
  // console.log('Fim do cálculo do preço total');
  return precoTotal.toFixed(2); // Arredonda para 2 casas decimais
}

// Função para atualizar o total geral na tabela
function atualizarTotalGeral() {
//   console.log('Início da atualização do total geral');
  var linhas = document.querySelectorAll('#lista_item tbody tr');
  var totalGeral = 0;
  linhas.forEach(function(row) {
      totalGeral += parseFloat(calcularPrecoTotal(row));
  });
    console.log('Total geral calculado:', totalGeral);
  document.getElementById('total_geral').textContent = 'R$ ' + totalGeral.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
//   console.log('Fim da atualização do total geral');
}


// Chamar a função de atualização do total geral após qualquer modificação na tabela
document.body.addEventListener('htmx:afterSwap', function(event) {
//   console.log('Evento htmx:afterSwap disparado');
//   console.log('Detalhes do evento:', event.detail);
  var trigger = event.detail.elt; // Obter o elemento que disparou o evento
//   console.log('Elemento que disparou o evento:', trigger); // Mensagem de depuração
  if (trigger.id === 'lista_item') {
    // console.log('Chamando atualizarTotalGeral()');
    atualizarTotalGeral();
} else if (trigger.closest('#lista_item')) {
    // console.log('Chamando atualizarTotalGeral() a partir de um descendente');
    atualizarTotalGeral();
}
});



// Função para atualizar o total no modal

function atualizarTotalModal(total) {
  // console.log('Atualizando total no modal:', total);
  var modalContent = document.querySelector('.modal-body');
  if (modalContent) {
      // console.log('Elemento modal-body encontrado');
      // Limpar o conteúdo do elemento total_geral
      var totalElement = modalContent.querySelector('#total_geral');
      if (totalElement) {
          totalElement.innerHTML = '';
      } else {
          // console.log('Erro: Elemento total_geral não encontrado');
          return;
      }

      // Criar um elemento para exibir o total da venda
      var totalText = document.createElement('h5');
      totalText.textContent = 'Total da Venda: R$ ' + total.toLocaleString('pt-BR', { minimumFractionDigits: 2 }); // Convertendo para string
      totalText.classList.add('text-success');
      
      // Adicionar o elemento do total ao elemento total_geral
      totalElement.appendChild(totalText);

      // console.log('Total atualizado no modal:', total.toFixed(2));
  } else {
      // console.log('Erro: Elemento modal-body não encontrado');
  }
}


// Chamar a função de atualizar o total do modal quando necessário
document.body.addEventListener('htmx:afterSwap', function(event) {
  // console.log('Evento htmx:afterSwap disparado');
  var trigger = event.detail.elt;
  // console.log('Elemento que disparou o evento:', trigger)
  if (trigger.id === 'lista_item') {
      // console.log('Modal de forma de pagamento exibido');
      // Obter o total da venda do contexto ou de onde estiver disponível
      var totalVenda = parseFloat(document.getElementById('total_geral').textContent.replace('R$ ', ''));
      // console.log('Total da venda obtido:', totalVenda.toFixed(2));
      if (!isNaN(totalVenda)) {
          // console.log('Total da venda obtido:', totalVenda.toFixed(2));
          atualizarTotalModal(totalVenda);
      } else {
          // console.log('Erro: Não foi possível obter o total da venda');
      }
  }
});



// função que atualiza o total quando é colocado um desconto
function calcularNovoTotal(desconto) {
  // Obter o total original da venda
  var totalOriginal = parseFloat(document.getElementById('total_geral').textContent.replace('R$ ', ''));
  // Calcular o novo total com base no desconto
  var descontoValor = (totalOriginal * desconto) / 100;
  var novoTotal = totalOriginal - descontoValor;
  // Atualizar o total no modal
  atualizarTotalModal(novoTotal);
}

// Adicionar um evento ao input de desconto para capturar quando o valor for alterado
var inputDesconto = document.getElementById('id_desconto');
if (inputDesconto) {
  inputDesconto.addEventListener('input', function(event) {
      // Obter o valor do desconto inserido pelo usuário
      var desconto = parseFloat(event.target.value);
      if (!isNaN(desconto)) {
          // Calcular o novo total da venda com base no desconto
          calcularNovoTotal(desconto);
      }
  });
}


document.body.addEventListener('htmx:afterSwap', function(event) {
    var trigger = event.detail.elt;
    // console.log('htmx:afterSwap event triggered');  // Debug message

    if (trigger.id === 'trocas') {
        // console.log('Trigger id is trocas');  // Debug message
        var totalTrocaElem = document.getElementById('total_troca');
        if (totalTrocaElem) {
            var totalTroca = parseFloat(totalTrocaElem.textContent.replace('R$ ', '').replace(',', '.'));
            // console.log('Total troca value:', totalTroca);  // Debug message
            if (!isNaN(totalTroca)) {
                setTimeout(calcularTotalTroca, 100);  // Add delay
            } else {
                console.error('Erro: totalTroca is NaN');
            }
        } else {
            console.error('Elemento total_troca não encontrado');
        }
    } else if (trigger.id === 'info_produto_trocado' || trigger.id === 'info_produto_novo') {
        // console.log('Trigger id is info_produto_trocado or info_produto_novo');  // Debug message
        setTimeout(calcularTotalTroca, 100);  // Add delay to ensure elements are in the DOM
    } else {
        console.log('Trigger id is not trocas, info_produto_trocado or info_produto_novo');
    }
});

function calcularTotalTroca() {
    // console.log('calcularTotalTroca called');  // Debug message
    var trocados = document.querySelectorAll('[id^="preco_trocado_"]');
    var novos = document.querySelectorAll('[id^="preco_novo_"]');

    // console.log('Trocados:', trocados);  // Debug message
    // console.log('Novos:', novos);  // Debug message

    var totalTrocado = 0;
    var totalNovo = 0;

    trocados.forEach(function(precoElem) {
        var precoText = precoElem.textContent;
        // console.log('Preço trocado text:', precoText);  // Debug message
        var preco = extrairPreco(precoText);
        // console.log('Preço trocado parsed:', preco);  // Debug message
        if (!isNaN(preco)) {
            totalTrocado += preco;
        }
    });

    novos.forEach(function(precoElem) {
        var precoText = precoElem.textContent;
        // console.log('Preço novo text:', precoText);  // Debug message
        var preco = extrairPreco(precoText);
        // console.log('Preço novo parsed:', preco);  // Debug message
        if (!isNaN(preco)) {
            totalNovo += preco;
        }
    });

    var diferenca = totalNovo - totalTrocado;
    // console.log('Diferença calculada:', diferenca);

    var totalTrocaElem = document.getElementById('total_troca');
    if (totalTrocaElem) {
        totalTrocaElem.textContent = 'R$ ' + diferenca.toFixed(2).replace('.', ',');
        // console.log('Elemento total_troca atualizado:', totalTrocaElem.textContent);
    } else {
        console.error('Elemento total_troca não encontrado no calcularTotalTroca');
    }
}

function extrairPreco(precoText) {
    var match = precoText.match(/R\$ ([\d,.]+)/);
    if (match && match[1]) {
        return parseFloat(match[1].replace('.', '').replace(',', '.'));
    }
    return NaN;
}

function deleteRows() {
    // Limpar o conteúdo da tabela
    var tabelas = document.getElementById("lista_item").getElementsByTagName("tbody");
    for (var i = 0; i < tabelas.length; i++) {
        tabelas[i].innerHTML = "";
    }

    atualizarTotalGeral();
}