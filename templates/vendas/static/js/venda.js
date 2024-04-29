  function renderiza_grafico1(){
    const ctx = document.getElementById('dashbord1').getContext('2d');
    
    // Defina as cores personalizadas para cada categoria
    const cores = {
        'Crédito': 'blue',
        'Débito': 'green',
        'Pix': 'orange',
        'Dinheiro': 'red'
    };
    
    // Obtenha as chaves(labels) do objeto cores
    const labels = Object.keys(cores);
    
    //Cria o grafico
    const myChart = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          label: 'Vendas',
          data: [499.15, 600, 325.37, 432],
          backgroundColor: labels.map(label => cores[label]), // Mapeie as cores de acordo com as labels
          borderColor: 'black', // cor do contorno das barras
          borderWidth: 1,
          borderRadius: 15,
          inflateAmount: 0.2,          
        }]
      },
      options: {
        plugins: {
            title:{
                display: true,
                text: "Vendas R$ x Categoria",                
                color:'black'            
            },
           legend: {
            display: true,            
           } 
        }
      }        
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

// Função para atualizar o total geral na página
function atualizarTotalGeral() {
  // console.log('Início da atualização do total geral');
  var linhas = document.querySelectorAll('#lista_item tbody tr');
  var totalGeral = 0;
  linhas.forEach(function(row) {
      totalGeral += parseFloat(calcularPrecoTotal(row));
  });
  // console.log('Total geral calculado:', totalGeral);
  document.getElementById('total_geral').textContent = 'R$ ' + totalGeral.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
  // console.log('Fim da atualização do total geral');
}


// Chamar a função de atualização do total geral após qualquer modificação na tabela
document.body.addEventListener('htmx:afterSwap', function(event) {
  // console.log('Evento htmx:afterSwap disparado');
  // console.log('Detalhes do evento:', event.detail);
  var trigger = event.detail.elt; // Obter o elemento que disparou o evento
  // console.log('Elemento que disparou o evento:', trigger); // Mensagem de depuração
  if (trigger.id === 'lista_item') {
      // console.log('Chamando atualizarTotalGeral()');
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



