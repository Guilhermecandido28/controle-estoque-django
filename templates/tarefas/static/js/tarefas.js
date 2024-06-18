document.addEventListener('DOMContentLoaded', function() {
    // Definição do calendário
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {                
        locale: 'pt-br',
        height: '1000px', 
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: 'eventos/',  
        eventClick: function(info) {
            const visualizarModal = new bootstrap.Modal(document.getElementById("visualizarModal"));
            var eventId = info.event.id;
            document.getElementById("visualizar_tarefa").innerText = info.event.title;
            document.getElementById("visualizar_inicio").innerText = new Date(info.event.start).toLocaleString();
            document.getElementById("visualizar_fim").innerText = info.event.end !== null ? new Date(info.event.end).toLocaleString() : new Date(info.event.start).toLocaleString();
            document.getElementById("visualizar_responsavel").innerText = info.event.extendedProps.funcionario.nome;
            document.getElementById("visualizar_status").innerText = info.event.extendedProps.status == true ? 'Concluída' : 'Pendente';
            visualizarModal.show();
        },
        dateClick: function(info) {
            const cadastrarModal = new bootstrap.Modal(document.getElementById("cadastrarModal"));
            console.log("Data selecionada:", info.dateStr);
            document.getElementById("inicio").value = converterData(info.dateStr);
            document.getElementById("fim").value = converterData(info.dateStr);
            cadastrarModal.show();
        }
    });        

    // Renderizar o calendário
    calendar.render();
    const msg = document.getElementById("messages")
    // Adicionar evento de clique no botão de cadastrar
    document.getElementById('btnCadEvento').addEventListener('click', async (e) => {
        e.preventDefault();
        
        let form = document.getElementById('formCadEvento');
        let formData = new FormData(form);

        const dados = await fetch("/tarefas/adicionar_tarefa/", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        });

        const resposta = await dados.json(); 

        if (!resposta['success']) {
            msg.innerHTML = `<div class="alert alert-danger" role="alert">${resposta['errors']}</div>`;
        } else {
            
            msg.innerHTML = `<div class="alert alert-success" role="alert">Tarefa salva com sucesso!</div>`;
            form.reset();

            
            console.log(resposta['color'])
            const novoEvento = {
                id: resposta['id'],
                title: resposta['tarefa'],
                start: resposta['inicio'],
                end: resposta['prazo'],
                color: resposta['color'],            
                extendedProps: {
                    funcionario: resposta['funcionario'],
                    status: resposta['status']
                }
            };

            calendar.addEvent(novoEvento);
            removerMsg()
            const cadastrarModal = new bootstrap.Modal(document.getElementById("cadastrarModal"));
            cadastrarModal.hide();

        }    
    });
    function removerMsg(){
        setTimeout(() =>{            
            document.getElementById("messages").innerHTML = "";
        }, 3000)
    }
});



// Configuração CSRF para htmx
document.body.addEventListener('htmx:configRequest', function(event) {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
});



function converterData(data) {
    let dataObj;
    try {
        // Tenta criar um objeto Date a partir da data fornecida
        dataObj = new Date(data);
    } catch (e) {
        // Se falhar, assume que a data já está no formato ISO 8601
        dataObj = new Date(data);
        console.warn("Falha ao criar objeto Date, assumindo formato ISO 8601:", dataObj); // Loga a nova tentativa com ISO 8601
    }

    const ano = dataObj.getFullYear();
    const mes = String(dataObj.getMonth() + 1).padStart(2, '0');
    const dia = String(dataObj.getDate() + 1).padStart(2, '0');
    const hora = String(dataObj.getHours()).padStart(2, '0');
    const minuto = String(dataObj.getMinutes()).padStart(2, '0');

    const dataFormatada = `${ano}-${mes}-${dia} ${hora}:${minuto}`;    

    return dataFormatada;
}

// Configuração CSRF para htmx
document.body.addEventListener('htmx:configRequest', function(event) {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
});




