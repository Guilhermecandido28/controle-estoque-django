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
    console.log('Formulário de busca enviado.');

    const search_codigo_barras = document.getElementById('id_codigo_barras').value;
    console.log('Código de barras pesquisado:', search_codigo_barras);

    const quantidade = parseFloat(document.getElementById('quantidade').value);
    console.log('Quantidade:', quantidade);

    const desconto = parseFloat(document.getElementById('desconto').value);
    console.log('Desconto:', desconto);

    let valorDesconto = desconto / 100;
    console.log('Valor do desconto:', valorDesconto);

    fetch(`pesquisar_produto/?search_codigo_barras=${search_codigo_barras}`)
    .then(response => {
        console.log('Resposta recebida do servidor.');
        return response.json();
    })
    .then(data => {
        console.log('Dados recebidos:', data);
        
        const tabela_produtos = document.querySelector('#lista_item tbody');
        const total_geralElement = document.getElementById('total_geral');
        
        const currencyFormatter = new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });

        let totalGeralAcumulado = parseFloat(total_geralElement.getAttribute('data-total') || '0');
        console.log('Total geral acumulado:', totalGeralAcumulado);

        data.results.forEach(item => {
            console.log('Processando item:', item);
            let row = '<tr>';
            row += `<td>${item.codigo_barras}</td>`;
            row += `<td>${item.descricao}</td>`;
            row += `<td>${item.tamanho}</td>`;
            row += `<td>${item.cor}</td>`;
            row += `<td>${quantidade}</td>`;
            row += `<td>${desconto}%</td>`;
            
            const preco = parseFloat(item.preco);
            let valorFinal;
            if (!isNaN(preco) && preco > 0) {
                valorFinal = (preco * quantidade) - (preco * quantidade * valorDesconto);
                row += `<td>${currencyFormatter.format(valorFinal)}</td>`;
                console.log('Valor final calculado:', valorFinal);
            } else {
                valorFinal = 0;
                row += `<td>Preço não disponível</td>`;
                console.log('Preço não disponível para item:', item.codigo_barras);
            }
            row += '</tr>';
            
            tabela_produtos.innerHTML += row;
            console.log('Linha adicionada à tabela:', row);

            totalGeralAcumulado += valorFinal;
        });

        total_geralElement.textContent = currencyFormatter.format(totalGeralAcumulado);
        total_geralElement.setAttribute('data-total', totalGeralAcumulado);
        console.log('Total geral atualizado:', totalGeralAcumulado);

        document.getElementById('id_codigo_barras').value = '';
        console.log('Campo código de barras limpo.');
        
    })
    .catch(error => {
        console.error('Erro ao buscar dados:', error);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    function updateModalTotal() {
        const totalGeral = document.getElementById('total_geral').textContent;
        console.log('Atualizando total no modal:', totalGeral);

        const modalTotalElement = document.querySelector('#forma-pagamento #modal_total_geral');
        if (modalTotalElement) {
            modalTotalElement.textContent = `Total: ${totalGeral}`;
            console.log('Total atualizado no modal:', totalGeral);
        }
    }

    const modal = document.getElementById('forma-pagamento');
    modal.addEventListener('show.bs.modal', function (event) {
        console.log('Modal exibido.');
        updateModalTotal();
    });
});

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('btnSalvarItens').addEventListener('click', function(event) {
        event.preventDefault();
        console.log('Botão salvar itens clicado.');

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
            console.log('Item coletado da tabela:', item);
        });

        const form = document.getElementById('formulario-venda');
        const formData = new FormData(form);
        const formEntries = {};
        formData.forEach((value, key) => {
            formEntries[key] = value;
            console.log('Campo do formulário:', key, value);
        });

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
            console.log('Resposta recebida da view Django.');
            if (!response.ok) {
                throw new Error('Erro na resposta da view.');
            }
            return response.json();
        })
        .then(data => {
            console.log('Dados recebidos após salvar venda:', data);
            
            const messageContainer = document.getElementById('messages');

            if (data.success) {
                const successMessage = document.createElement('div');
                successMessage.className = 'alert alert-success fade show';
                successMessage.textContent = 'Venda finalizada com sucesso!';
                messageContainer.innerHTML = '';
                messageContainer.appendChild(successMessage);
                
                setTimeout(() => {
                    successMessage.classList.remove('show');
                    successMessage.classList.add('fade');
                    setTimeout(() => {
                        messageContainer.innerHTML = '';
                    }, 1000);
                }, 3000);

                document.querySelector('#lista_item tbody').innerHTML = '';
                
                document.querySelector('[name="codigo_barras"]').value = '';
                document.querySelector('[name="quantidade"]').value = '1';
                document.querySelector('[name="desconto"]').value = '0';
                
                const total_geralElement = document.getElementById('total_geral');
                total_geralElement.textContent = 'R$ 0,00';
                total_geralElement.setAttribute('data-total', '0');
                document.getElementById('modal_total_geral').textContent = 'Total: R$ 0,00';
                console.log('Valores do formulário e tabela resetados.');

                setTimeout(function() {
                    window.location.reload();
                }, 3000);

            } else {
                const errorMessage = document.createElement('div');
                errorMessage.className = 'alert alert-danger';
                errorMessage.textContent = data.error || 'Falha ao finalizar a venda. Por favor, verifique os dados e tente novamente.';
                messageContainer.innerHTML = '';
                messageContainer.appendChild(errorMessage);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            const messageContainer = document.getElementById('messages');
            const errorMessage = document.createElement('div');
            errorMessage.className = 'alert alert-danger';
            errorMessage.textContent = 'Erro ao processar a venda. Por favor, tente novamente mais tarde.';
            messageContainer.innerHTML = '';
            messageContainer.appendChild(errorMessage);
        });
    });
});

function limparPreco(precoStr) {
    console.log('Limpar preço recebido:', precoStr);

    precoStr = precoStr.replace('R$', '').replace(' ', '').trim();
    console.log('Preço após remoção de prefixo e espaços:', precoStr);

    if (precoStr.includes(',')) {
        precoStr = precoStr.replace('.', '').replace(',', '.');
    } else {
        precoStr = precoStr.replace('.', '').replace(',', '.');
    }
    console.log('Preço após substituição de vírgulas por pontos:', precoStr);

    return precoStr;
}




