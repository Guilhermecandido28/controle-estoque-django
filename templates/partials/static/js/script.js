function menuShow(){
    let menuMobile =  document.querySelector('.menu-mobile');
    if (menuMobile.classList.contains('open')){
        menuMobile.classList.remove('open');
        document.querySelector('.icon').src = 'assets/img/menu_white_36dp.svg';
    } else {
        menuMobile.classList.add('open')
        document.querySelector('.icon').src = 'assets/img/close_white_36dp.svg';
    }
}

var menuItem = document.querySelectorAll('.item-menu') // serve para guardar uma classe
var conteudo = document.querySelector('.conteudo');
function selectLink(event) {
    // Declara a variável `menuItem` dentro da função
    var menuItem = document.querySelectorAll('.item-menu');
  
    // Pega o item clicado
    const item = event.target;
  
    // Adiciona a classe `ativo` ao item clicado
    item.classList.add('ativo');
  
    // Remove a classe `ativo` de todos os outros itens do menu
    menuItem.forEach((item) => {
      if (item !== item) {
        item.classList.remove('ativo');
      }
    });
  
    // Evita que a página seja recarregada
    event.preventDefault();
}  

// Expandir o menu

var btnExp = document.querySelector('#btn-exp')
var menuSide = document.querySelector('.menu-lateral')


btnExp.addEventListener('click',function(){    menuSide.classList.toggle('expandir')
    
})


function mostrarSenha() {
    var inputPass = document.getElementById('senha');
    var btnShowPass = document.getElementById('btn-senha');

    if (inputPass.type === 'password') {
        inputPass.setAttribute('type', 'text');
        btnShowPass.classList.replace('bi-eye', 'bi-eye-slash');
    } else {
        inputPass.setAttribute('type', 'password');
        btnShowPass.classList.replace('bi-eye-slash', 'bi-eye');
    }
}

function mostrarRepetirSenha() {
    var inputRepetirSenha = document.getElementById('repetir-senha');
    var btnShowRepetirSenha = document.getElementById('btn-repetir-senha');

    if (inputRepetirSenha.type === 'password') {
        inputRepetirSenha.setAttribute('type', 'text');
        btnShowRepetirSenha.classList.replace('bi-eye', 'bi-eye-slash');
    } else {
        inputRepetirSenha.setAttribute('type', 'password');
        btnShowRepetirSenha.classList.replace('bi-eye-slash', 'bi-eye');
    }
}