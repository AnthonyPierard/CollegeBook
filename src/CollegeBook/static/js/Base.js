const body = document.querySelector('body');
const links = document.querySelector('.links');
const menuSVG = document.querySelector('.menu svg');

menuSVG.addEventListener('click', () => {
    links.classList.toggle('selected');
    body.classList.toggle('scroll-disabled');
});
