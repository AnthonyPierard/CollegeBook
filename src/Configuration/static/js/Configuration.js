
const seat = document.querySelector(".seat");
console.log(seat)
seat.addEventListener('click', () => {
    console.log(seat)
    menu.classList.toggle('clicked') // créer une classe à un élément et la retire si on reclique
})