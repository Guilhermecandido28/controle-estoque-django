function renderiza_grafico(){
    const ctx = document.getElementById('dashbord').getContext('2d');
    fetch('dados_grafico')
      .then(response => response.json())
      .then(data => {
        const labels = Object.keys(data);
        const values = Object.values(data);
    
    //Cria o grafico
    const myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Quantidade de Estoque',
          data: values,
          backgroundColor: function(context){
            const value = context.dataset.data[context.dataIndex];
            if (value < 2){
                return 'red';
            } else if (value < 5){
                return 'orange';
            } else{
                return 'green';
            }
          },
          borderColor: 'black', // cor do contorno das barras
          borderWidth: 0.2,
          borderRadius: 15,
          inflateAmount: 0.2
        }]
      },
      options: {
        plugins: {
            title:{
                display: true,
                text: "Quantidade de Produtos Cadastrados em cada Mês",                
                color:'black'            
            },
           legend: {
            display: false,            
           } 
        }
      }        
    });
  })
  .catch(error => console.error('erro ao carregar os dados do gráfico:', error));
  }
  
  
  const btnToast = document.getElementById("btnToast"); //seleciono o botão
  btnToast.addEventListener("click", () => { // no clique do botão
      const descricao = document.getElementById("descricao").value;
      const quantidade = document.getElementById("quantidade").value;      
      const toast = document.getElementById("toast"); // capturo o toast invisivel
      const container = document.getElementById("toastContainer"); // capturo o container
      const novoToast = toast.cloneNode(true); // faço um clone do toast invisivelk
      novoToast.lastElementChild.innerHTML = quantidade + " " + "unidade(s)" + " " + descricao + " " + "adicionado(a)! "; // muda a mensagem interna  com data
      container.appendChild(novoToast); // coloco o novo toast no container
      const bsToast = new bootstrap.Toast(novoToast, {}); // aplico a função toast do bootstrap
      bsToast.show(); // mando mostrar
  });