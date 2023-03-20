const menu = document.querySelector(".menu");
const menu_svg = document.querySelector(".menu svg");

menu_svg.addEventListener('click', () => {
    menu.classList.toggle('clicked')
})