let eventId;
document.addEventListener('DOMContentLoaded', function() {
    // Obtém o elemento do calendário pelo ID
    var calendarEl = document.getElementById('calendar');

    // Cria uma nova instância do FullCalendar com configurações específicas
    var calendar = new FullCalendar.Calendar(calendarEl, {
        themeSystem: 'bootstrap5',                
        locale: 'pt-br', // Define o idioma do calendário para português brasileiro
        height: '1000px', // Define a altura do calendário
        headerToolbar: { // Configura a barra de ferramentas do cabeçalho
            left: 'prev,next today', // Botões de navegação e o botão "hoje" à esquerda
            center: 'title', // Título do calendário no centro
            right: 'dayGridMonth,timeGridWeek,timeGridDay' // Tipos de visualização à direita
        },
        events: 'eventos/', // URL para buscar os eventos
        eventDidMount: function(info) { // Adiciona a classe 'cursor-pointer' aos eventos para mudar o cursor ao passar o mouse
            info.el.classList.add('cursor-pointer');
        },  
        eventClick: function(info) { // Função chamada ao clicar em um evento

            // Cria uma instância do modal para visualização
            const visualizarModal = new bootstrap.Modal(document.getElementById("visualizarModal"));

               // Atualiza o título da tarefa no modal
            document.getElementById("visualizar_tarefa").innerText = info.event.title; // 

            // Atualiza a data de início no modal
            document.getElementById("visualizar_inicio").innerText = new Date(info.event.start).toLocaleString();

            // Atualiza a data de término no modal e verifica se a data de inicio é igual a do fim
            document.getElementById("visualizar_fim").innerText = info.event.end !== null ? new Date(info.event.end).toLocaleString() : new Date(info.event.start).toLocaleString();


             // Atualiza o responsável no modal
            document.getElementById("visualizar_responsavel").innerText = info.event.extendedProps.funcionario.nome;

            // Atualiza o status no modal
            document.getElementById("visualizar_status").innerText = info.event.extendedProps.status == true ? 'Concluída' : 'Pendente';

            //ENVIAR OS DADOS PARA O FORMULÁRIO EDITAR

            // OBTÉM O FORMULÁRIO
            const editModalElement = document.getElementById("visualizarModal");

            // Obtém o ID do evento clicado
            eventId = info.event.id;

            // OBTÉM OS CAMPOS DO EDITAR
            const campoTarefa = editModalElement.querySelector("#tarefas");
            const campoInicio = editModalElement.querySelector("#inicio");            
            const campoFim = editModalElement.querySelector("#fim");
            const campoStatus = editModalElement.querySelector("#status");
            const campoFuncionario = editModalElement.querySelector("#funcionario");
 

            // ATRIBUI O VALOR PARA OS CAMPOS EDITAR
            campoTarefa.value = info.event.title;            
            campoInicio.value = converterData(info.event.start);            
            campoFim.value = info.event.end !== null ? converterData(info.event.end) : converterData(info.event.start);            
            campoStatus.checked =  info.event.extendedProps.status            
            campoFuncionario.value = info.event.extendedProps.funcionario.nome
            console.log(info.event.extendedProps.funcionario.nome)
            
            
            // Exibe o modal de visualização
            visualizarModal.show(); 
        },


        dateClick: function(info) { // Função chamada ao clicar em uma data no calendário
            // Obtém o elemento do modal pelo ID
            const cadastrarModalElement = document.getElementById("cadastrarModal");
            const cadastrarModal = new bootstrap.Modal(document.getElementById("cadastrarModal")); // Cria uma instância do modal para cadastro
            
            const campoInicio = cadastrarModalElement.querySelector("#inicio");
            const campoFim = cadastrarModalElement.querySelector("#fim");

            
            // Define os valores dos campos
            campoInicio.value = converterData(info.dateStr);
            campoFim.value = converterData(info.dateStr); // Define a data de término no formulário
            cadastrarModal.show(); // Exibe o modal de cadastro
        }
    });        
        
        // Renderiza o calendário na página
        calendar.render();
        
        // Cria um elemento de estilo para adicionar ao cabeçalho do documento
        var style = document.createElement('style');
        style.textContent = '.cursor-pointer { cursor: pointer; }'; // Define o estilo para a classe 'cursor-pointer'
        document.head.appendChild(style); // Adiciona o estilo ao documento
        
        // Obtém o elemento para mensagens
        const msg = document.getElementById("messages")
        
        // Adiciona um ouvinte de evento ao botão de cadastro
        document.getElementById('btnCadEvento').addEventListener('click', async (e) => {
            e.preventDefault(); // Previne o comportamento padrão do formulário
            let form = document.getElementById('formCadEvento'); // Obtém o formulário
            let formData = new FormData(form); // Cria um objeto FormData com os dados do formulário
            
            // Envia os dados do formulário para o servidor
            const dados = await fetch("/tarefas/adicionar_tarefa/", {
                method: 'POST', // Método de requisição
                body: formData, // Dados do formulário
                headers: { // Cabeçalhos da requisição
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken') // Token CSRF para segurança
                }
            });
            
            // Aguarda a resposta do servidor
            const resposta = await dados.json(); 
            
            // Verifica se a requisição foi bem-sucedida
            if (!resposta['success']) {
                msg.innerHTML = `<div class="alert alert-danger" role="alert">${resposta['errors']}</div>`; // Exibe mensagem de erro
            } else {
                msg.innerHTML = `<div class="alert alert-success" role="alert">Tarefa salva com sucesso!</div>`; // Exibe mensagem de sucesso
                form.reset(); // Limpa o formulário           
                
                
                // Cria um novo evento para adicionar ao calendário
                const novoEvento = {
                    id: resposta['id'], // Define o ID do evento, geralmente um identificador único para o evento
                    title: resposta['tarefa'], // Define o título do evento, que será exibido no calendário
                    start: resposta['inicio'], // Define a data de início do evento, quando o evento começa
                    end: resposta['prazo'], // Define a data de término do evento, quando o evento termina
                    color: resposta['color'], // Define a cor do evento, usada para destacar visualmente o evento no calendário
                    extendedProps: { // Propriedades estendidas, usadas para armazenar informações adicionais sobre o evento
                        funcionario: resposta['funcionario'], // Armazena informações sobre o funcionário responsável pelo evento
                        status: resposta['status'] // Armazena o status do evento, como concluído ou pendente
                    }
                };
                
                
                // Adiciona o novo evento ao calendário
                calendar.addEvent(novoEvento);
                removerMsg() // Remove a mensagem após um tempo
                const cadastrarModal = new bootstrap.Modal(document.getElementById("cadastrarModal")); // Obtém o modal de cadastro
                cadastrarModal.hide(); // Esconde o modal de cadastro
            }    
        });
        
        
        // RECEBER O SELETOR OCULTAR FORMULÁRIO EDITAR EVENTO E APRESENTAR OS DETALHES DO EVENTO
        
        
        // Adiciona o ouvinte de evento ao botão de edição
        document.getElementById('btnViewEditEvent').addEventListener('click', function() {
            
            // OCULTA OS DETALHES DO EVENTO
            document.getElementById('visualizarEvento').style.display = 'none';
            document.getElementById('visualizarModalLabel').style.display = 'none';
            
            // APRESENTA O TÍTULO E O FORMULÁRIO DE EDIÇÃO
            document.getElementById('editarEvento').style.display = 'block';
            document.getElementById('editarModalLabel').style.display = 'block';
        });  
        
        // Adiciona o ouvinte de evento ao botão de cancelar
        document.getElementById('btnViewEvento').addEventListener('click', function() {
            
            // Apresenta OS DETALHES DO EVENTO
            document.getElementById('visualizarEvento').style.display = 'block';
            document.getElementById('visualizarModalLabel').style.display = 'block';
            
            // Oculta O TÍTULO E O FORMULÁRIO DE EDIÇÃO
            document.getElementById('editarEvento').style.display = 'none';
            document.getElementById('editarModalLabel').style.display = 'none';
        });
        
        
        // RECEBER O SELETOR DO FORMULÁRIO
        const formEditEvento = document.getElementById('formEditEvento');   
        
        
        
        // AGUARDAR O CLIQUE NO BOTÃO DO USUÁRIO
        
        formEditEvento.addEventListener("submit", async (e) => {
            
            // NÃO PERMIRTIR A ATUALIZAÇÃO DA PÁGINA
            e.preventDefault();
            
            // RECEBER OS DADOS DO FORMULÁRIO
            const dadosForm = new FormData(formEditEvento);

            
            
            
            // CHAMAR A URL RESPONSÁVEL
            const respostaForm = await fetch(`/tarefas/editar_tarefa/${eventId}`, {
                method : 'POST',
                body: dadosForm, // Dados do formulário
                headers: { // Cabeçalhos da requisição
                    'X-CSRFToken': dadosForm.get('csrfmiddlewaretoken') // Token CSRF para segurança
                }
                
            })
            
            // REALIZA A LEITURA DOS DADOS DA URL
            const respostaEdit = await respostaForm.json();

            
            // ACESSA O IF QUANDO NÃO EDITAR COM SUCESSO
            if(!respostaEdit['success']){                
                msg.innerHTML = `<div class="alert alert-danger" role="alert">${respostaEdit['errors']}</div>`; // Exibe mensagem de erro
            }else{
                msg.innerHTML = `<div class="alert alert-success" role="alert">Tarefa salva com sucesso!</div>`;
            }
            
            // RECUPERAR O EVENTO NO FULLCALENDAR PELO ID
            const eventoExiste = calendar.getEventById(respostaEdit['id'])

            // VERIFICA SE ENCONTROU O EVENTO NO FULLCALENDAR PELO ID
            if(eventoExiste){

                
                // ATUALIZA OS ATRIBUTOS DO EVENTO COM OS NOVOS VALORES DO BANCO DE DADOS
                eventoExiste.setProp('title', respostaEdit['tarefa']);

                // Atualiza as propriedades de data padrão
                // Debugging start and end dates before setting them
                
                
                let startDate = new Date(respostaEdit['start']);
                let endDate = new Date(respostaEdit['end']);
                
                

                eventoExiste.setDates(startDate, endDate);                


                eventoExiste.setExtendedProp('status', respostaEdit['status']);
                eventoExiste.setExtendedProp('funcionario', respostaEdit['responsavel']);
                eventoExiste.setProp('color', respostaEdit['color']);

    
            }
            // Apresenta OS DETALHES DO EVENTO
            document.getElementById('visualizarEvento').style.display = 'block';
            document.getElementById('visualizarModalLabel').style.display = 'block';
            
            // Oculta O TÍTULO E O FORMULÁRIO DE EDIÇÃO
            document.getElementById('editarEvento').style.display = 'none';
            document.getElementById('editarModalLabel').style.display = 'none';
            removerMsg()

            
        });
        
        // Função para remover mensagens após um tempo
        function removerMsg(){
            setTimeout(() =>{            
                document.getElementById("messages").innerHTML = ""; // Limpa as mensagens
            }, 3000)
        }
    });
    
    // Função para converter a data para o formato desejado
    function converterData(data) {
        let dataObj;
        try {
            dataObj = new Date(data); // Tenta criar um objeto Date
        } catch (e) {
            dataObj = new Date(data); // Se falhar, assume que a data já está no formato ISO 8601
        }
        
        const ano = dataObj.getFullYear(); // Obtém o ano
        const mes = String(dataObj.getMonth() + 1).padStart(2, '0'); // Obtém o mês
        const dia = String(dataObj.getDate()).padStart(2, '0'); // Obtém o dia
        const hora = String(dataObj.getHours()).padStart(2, '0'); // Obtém a hora
        const minuto = String(dataObj.getMinutes()).padStart(2, '0'); // Obtém o minuto
        
        // Formata a data
        const dataFormatada = `${ano}-${mes}-${dia} ${hora}:${minuto}`; 
        
        return dataFormatada; // Retorna a data formatada
    }
    
    
    
    
    
    
    
    
    
    
    
    
    
    



// Configuração CSRF para htmx
document.body.addEventListener('htmx:configRequest', function(event) {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}'; // Adiciona o token CSRF aos cabeçalhos da requisição
});
