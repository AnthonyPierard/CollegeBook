
/*const seat = document.querySelector(".seat");
console.log(seat)
seat.addEventListener('click', () => {
    console.log(seat)
    menu.classList.toggle('clicked') // créer une classe à un élément et la retire si on reclique
})*/

function fill_seat(seats){
    const seat_area = document.querySelector('.seat-area');
    const row = document.createElement('div');
    row.class = seats.class;
    seat_area.appendChild(row);

    for (const seat of seats.seat){
        const balise_seat = document.createElement('div');
        console.log(seat);
    }

}
async function prepare_json() {

    const requestURL = 'C:\\Users\\Anthony Pierard\\Documents\\MA1\\GENIE\\projet\\CollegeBook\\src\\Configuration\\static\\json\\allSeat.json';
    const request = new Request(requestURL);
    const response = await fetch(request);
    const seat = await response.json();

    fill_seat(seat);
}

prepare_json();