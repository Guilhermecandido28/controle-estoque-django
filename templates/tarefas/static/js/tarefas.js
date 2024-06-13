document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {       
        
        initialView: 'timeGridDay',
        timeZone: 'America/Sao_Paulo',
        locale: 'pt-br',
        headerToolbar:{
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        
        events: 'eventos/',  // URL do endpoint que retorna os eventos
        eventClick: function(info) {
            // Mostrar tooltip ao clicar no evento
            var tooltipContent = '<div><strong>' + info.event.title + '</strong><br>' + info.event.extendedProps.description + '</div>';

            tippy(info.el, {
                content: tooltipContent,
                allowHTML: true,
                interactive: true,
                theme: 'light',
                placement: 'top',
                trigger: 'click',
                maxWidth: 300
            });
        }
    });        

    calendar.render();
});

function marcarTarefaConcluida(evento) {
    // Aqui você deve enviar uma requisição para o backend (Django) para marcar a tarefa como concluída
    var evento_id = evento.id;

    fetch('/marcar_concluida/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Use isso se estiver usando CSRF protection no Django
        },
        body: JSON.stringify({ id: evento_id })
    })
    .then(response => {
        if (response.ok) {
            // Atualizar o evento no calendário para refletir o novo status
            evento.setProp('backgroundColor', 'green');  // Alterar a cor do evento para verde (concluído)
            console.log('Tarefa marcada como concluída com sucesso');
        } else {
            console.error('Erro ao marcar tarefa como concluída');
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
    });
}


var form = document.getElementById('tarefa-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            var formData = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('Form submission response:', data);
                if (data.success) {
                    calendar.refetchEvents();  // Atualiza os eventos no calendário
                    alert('A tarefa foi adicionada com sucesso!');
                    form.reset();  // Reseta o formulário
                } else {
                    alert('Ocorreu um erro: ' + (data.error || data.errors.join(', ')));
                }
            })
            .catch(error => console.error('Erro ao submeter o formulário:', error));
        });
    }



// Configuração CSRF para htmx
document.body.addEventListener('htmx:configRequest', function(event) {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
});



document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }

        form.classList.add('was-validated');

        const formData = new FormData(form);
        fetch("{% url 'adicionar_tarefa' %}", {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                Object.keys(data.errors).forEach(function (field) {
                    const fieldElement = document.getElementById('id_' + field);
                    fieldElement.classList.add('is-invalid');
                    fieldElement.insertAdjacentHTML('afterend', '<div class="invalid-feedback">' + data.errors[field].join('<br>') + '</div>');
                });
            }
        })
        .catch(error => console.error('Erro:', error));
    });
});

