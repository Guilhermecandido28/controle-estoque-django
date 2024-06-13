
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {          
        locale: 'pt-br',
        events: 'evento/',
        initialView: 'dayGridMonth',
        locale: 'pt-br',
        headerToolbar:{
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },        
    dateClick: function() {
alert('a day has been clicked!');
}
    });
    calendar.render();

});


function adicionarPessoa() {
    // Obtém os valores do formulário
    var nome = document.getElementById("nome").value;
    var url_instagram = document.getElementById("url_instagram").value;
    console.log(url_instagram)   
     
    // Cria uma nova linha na tabela
    var newRow = document.createElement("tr");

    // Cria as células para nome e idade
    var imgCell = document.createElement("td");
    var nomeCell = document.createElement("td");

    // Define o texto das células
    var img = document.createElement("img");
    img.style.height = "50px";
    img.style.width = "50px";
    img.style.borderRadius = "50%";
    

    imgCell.classList.add("text-center");
    nomeCell.classList.add("text-start");

    
    img.src = url_instagram;

    imgCell.appendChild(img);

    nomeCell.innerText = nome;

    // Adiciona as células à nova linha
    newRow.appendChild(imgCell);
    newRow.appendChild(nomeCell);

    // Adiciona a nova linha à tabela
    document.getElementById("table-clientes").appendChild(newRow);
}


// Example starter JavaScript for disabling form submissions if there are invalid fields
const btnSalvar = document.getElementById("enviar-cliente");
btnSalvar.addEventListener("click", function(event) {
    // Selecionando o formulário
    const form = document.querySelector('.needs-validation');

    // Realizando a validação manualmente
    if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
    }
    
    // Adicionando classes de validação do Bootstrap ao formulário
    form.classList.add('was-validated');

    // Verificando se o formulário é válido
    if (form.checkValidity() === true) {
        // Se o formulário for válido, exibe o toast
        console.log('formulario enviado');
    }
});