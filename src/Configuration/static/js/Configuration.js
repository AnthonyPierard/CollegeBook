
/*const seat = document.querySelector(".seat");
console.log(seat)
seat.addEventListener('click', () => {
    console.log(seat)
    menu.classList.toggle('clicked') // créer une classe à un élément et la retire si on reclique
})*/

function fill_seat(obj){
    const seat_area = document.createElement('div');
    seat_area.classList.add('seat-area');
    const theatre = document.querySelector('.theatre');
    theatre.appendChild(seat_area);
    for (const index in obj){
        const row = document.createElement('div');
        row.classList.add(obj[index].class);
        seat_area.appendChild(row);
        if(obj[index].seat != null){
               const all_seat = obj[index].seat;

            for (const seat of all_seat){
                const balise_seat = document.createElement('div');
                const new_seat = seat.split(' ');
                for (const class_seat of new_seat) {
                    balise_seat.classList.add(class_seat);
                }
                row.appendChild(balise_seat);
            }
        }

    }


}
async function prepare_json(url) {

    //on retire ce qu'il y avait dans le seat-area
    const seat_area = document.querySelector('.seat-area');
    seat_area.remove();
    //on va chercher ce qu'il y a dans le json
    const requestURL = url;
    const request = new Request(requestURL);
    const response = await fetch(request);
    const seat = await response.json();

    fill_seat(seat);
}