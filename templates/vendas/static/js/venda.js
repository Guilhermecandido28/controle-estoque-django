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


document.getElementById('search_codigo_barras').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const search_codigo_barras = document.getElementById('id_codigo_barras').value;
    const quantidade = parseFloat(document.getElementById('quantidade').value);
    const desconto = parseFloat(document.getElementById('desconto').value);
    
    // Cálculo do valor de desconto
    let valorDesconto = desconto / 100;

    fetch(`pesquisar_produto/?search_codigo_barras=${search_codigo_barras}`)
    .then(response => response.json())
    .then(data => {
        const tabela_produtos = document.querySelector('#lista_item tbody');
        const total_geralElement = document.getElementById('total_geral');
        
        // Configuração para formatação de moeda em reais
        const currencyFormatter = new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });

        // Recupera o total acumulado do atributo do elemento
        let totalGeralAcumulado = parseFloat(total_geralElement.getAttribute('data-total') || '0');

        data.results.forEach(item => {
            let row = '<tr>';
            row += `<td>${item.codigo_barras}</td>`;
            row += `<td>${item.descricao}</td>`;
            row += `<td>${item.tamanho}</td>`;
            row += `<td>${item.cor}</td>`;
            row += `<td>${quantidade}</td>`;
            row += `<td>${desconto}%</td>`;
            
            // Verificação se o campo 'preco' existe e é um número
            const preco = parseFloat(item.preco);
            let valorFinal;
            if (!isNaN(preco) && preco > 0) {
                valorFinal = (preco * quantidade) - (preco * quantidade * valorDesconto);
                row += `<td>${currencyFormatter.format(valorFinal)}</td>`;
            } else {
                valorFinal = 0;
                row += `<td>Preço não disponível</td>`;  // Mensagem de erro caso o preço seja inválido
            }
            row += '</tr>';
            
            tabela_produtos.innerHTML += row;  // Adiciona a nova linha à tabela

            // Atualiza o total acumulado
            totalGeralAcumulado += valorFinal;
        });

        // Atualiza o total na página e armazena o total no atributo do elemento
        total_geralElement.textContent = currencyFormatter.format(totalGeralAcumulado);
        total_geralElement.setAttribute('data-total', totalGeralAcumulado);

        // Limpar os campos do formulário após a inserção
        document.getElementById('id_codigo_barras').value = '';
        
    })
    .catch(error => console.error('erro ao buscar dados:', error));
});

document.addEventListener('DOMContentLoaded', function() {
    // Função para atualizar o valor total no modal
    function updateModalTotal() {
        const totalGeral = document.getElementById('total_geral').textContent;
        const modalTotalElement = document.querySelector('#forma-pagamento #modal_total_geral');
        if (modalTotalElement) {
            modalTotalElement.textContent = `Total: ${totalGeral}`;
        }
    }

    // Adiciona um evento para o modal ser mostrado
    const modal = document.getElementById('forma-pagamento');
    modal.addEventListener('show.bs.modal', function (event) {
        updateModalTotal();
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Função para atualizar o valor total no modal
    function updateModalTotal() {
        const totalGeral = document.getElementById('total_geral').textContent;
        const modalTotalElement = document.querySelector('#forma-pagamento #modal_total_geral');
        if (modalTotalElement) {
            modalTotalElement.textContent = `Total: ${totalGeral}`;
        }
    }

    // Adiciona um evento para o modal ser mostrado
    const modal = document.getElementById('forma-pagamento');
    modal.addEventListener('show.bs.modal', function (event) {
        updateModalTotal();
    });
});

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('btnSalvarItens').addEventListener('click', function(event) {
        event.preventDefault(); // Previne o comportamento padrão do formulário

        // Coleta dados da tabela
        const itens = [];
        document.querySelectorAll('#lista_item tbody tr').forEach(row => {
            const item = {
                codigo_barras: row.children[0].textContent,
                descricao: row.children[1].textContent,
                tamanho: row.children[2].textContent,
                cor: row.children[3].textContent,
                quantidade: row.children[4].textContent,
                desconto: row.children[5].textContent,
                preco: limparPreco(row.children[6].textContent)
            };
            itens.push(item);
        });

        // Coleta dados do formulário
        const form = document.getElementById('formulario-venda');
        const formData = new FormData(form);
        const formEntries = {};
        formData.forEach((value, key) => {
            formEntries[key] = value;
        });

        // Envia dados para a view Django
        fetch("/vendas/salvar_venda/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                itens: itens,
                form: formEntries
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na resposta da view.');
            }
            return response.json();
        })
        .then(data => {
            const messageContainer = document.getElementById('messages');

            if (data.success) {
                // Mensagem de sucesso que some após 3 segundos
                const successMessage = document.createElement('div');
                successMessage.className = 'alert alert-success fade show';
                successMessage.textContent = 'Venda finalizada com sucesso!';
                messageContainer.innerHTML = ''; // Limpa mensagens anteriores
                messageContainer.appendChild(successMessage);
                
                // Esconde a mensagem de sucesso após 3 segundos
                setTimeout(() => {
                    successMessage.classList.remove('show');
                    successMessage.classList.add('fade');
                    setTimeout(() => {
                        messageContainer.innerHTML = ''; // Remove o elemento após a animação de desaparecimento
                    }, 1000); // Tempo para a animação de desaparecimento
                }, 3000); // Mensagem visível por 3 segundos

                // Limpa a tabela
                document.querySelector('#lista_item tbody').innerHTML = '';
                
                // Define valores padrão para os campos do formulário
                document.querySelector('[name="codigo_barras"]').value = '';
                document.querySelector('[name="quantidade"]').value = '1';
                document.querySelector('[name="desconto"]').value = '0';
                
                // Atualiza o total geral e o modal
                const total_geralElement = document.getElementById('total_geral');
                total_geralElement.textContent = 'R$ 0,00'; // Resetando o total geral
                total_geralElement.setAttribute('data-total', '0');
                document.getElementById('modal_total_geral').textContent = 'Total: R$ 0,00';
                setTimeout(function() {
                    window.location.reload();
                }, 3000);

            } else {
                // Mensagem de erro persistente com detalhes do erro
                const errorMessage = document.createElement('div');
                errorMessage.className = 'alert alert-danger';
                errorMessage.textContent = data.error || 'Falha ao finalizar a venda. Por favor, verifique os dados e tente novamente.';
                messageContainer.innerHTML = ''; // Limpa mensagens anteriores
                messageContainer.appendChild(errorMessage);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            const messageContainer = document.getElementById('messages');
            // Mensagem de erro persistente
            const errorMessage = document.createElement('div');
            errorMessage.className = 'alert alert-danger';
            errorMessage.textContent = 'Erro ao processar a venda. Por favor, tente novamente mais tarde.';
            messageContainer.innerHTML = ''; // Limpa mensagens anteriores
            messageContainer.appendChild(errorMessage);
        });
    });
});

function limparPreco(precoStr) {
    // Remove o prefixo 'R$', espaços e substitui vírgulas por pontos para a parte decimal
    precoStr = precoStr.replace('R$', '').replace(' ', '').trim();
    
    // Substitui a vírgula decimal por ponto
    if (precoStr.includes(',')) {
        precoStr = precoStr.replace('.', '').replace(',', '.');
    } else {
        precoStr = precoStr.replace('.', '').replace(',', '.');
    }
    console.log(precoStr)
    return precoStr;
}





