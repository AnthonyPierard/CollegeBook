
/*const seat = document.querySelector(".seat");
console.log(seat)
seat.addEventListener('click', () => {
    console.log(seat)
    menu.classList.toggle('clicked') // créer une classe à un élément et la retire si on reclique
})*/

function fill_seat(obj){
    const seat_area = document.querySelector('.seat-area');
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
                    console.log(class_seat);
                    balise_seat.classList.add(class_seat);
                }
                row.appendChild(balise_seat);
            }
        }

    }


}
async function prepare_json() {

    const requestURL = "../static/json/onlySeat.json" //'https://github.com/AnthonyPierard/CollegeBook/blob/Refactoring/src/Configuration/static/json/allSeat.json'; //je ne sais pas comment y accéder
    const request = new Request(requestURL);
    const response = await fetch(request);
    const seat = await response.json();

    fill_seat(seat);
}

prepare_json();