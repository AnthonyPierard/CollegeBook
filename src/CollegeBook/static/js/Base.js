const links = document.querySelector(".links");
const menu_svg = document.querySelector(".menu svg");

menu_svg.addEventListener('click', () => {
    links.classList.toggle('selected')
})