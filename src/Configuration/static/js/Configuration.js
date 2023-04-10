
function clickable_seats_and_spaces(){
    const seats_and_spaces = document.querySelectorAll('.seat, .space')
    console.log(seats_and_spaces)
    for (const element of seats_and_spaces) {
        element.addEventListener('click', () => {
            element.classList.toggle('seat')
            element.classList.toggle('space')
        })
    }
}

//remplis le seat-area de siège ou d'espace debout
function fill_seat(json_dictionnary){
    const seat_area = document.createElement('div');
    seat_area.classList.add('seat-area');
    const theatre = document.querySelector('.theatre');
    theatre.appendChild(seat_area);
    //va regarder dans le json les seats
    for (const index in json_dictionnary){
        const row = document.createElement('div');
        row.classList.add(json_dictionnary[index].class);
        seat_area.appendChild(row);
        if(json_dictionnary[index].seat != null){
               const all_seat = json_dictionnary[index].seat;

            for (const seat of all_seat){
                const marker_seat = document.createElement('div');
                const new_seat = seat.split(' ');
                for (const class_seat of new_seat) {
                    marker_seat.classList.add(class_seat);
                }
                row.appendChild(marker_seat);
            }
        }

    }
    clickable_seats_and_spaces()

}
//fonction pour choisir le json
async function prepare_json(url) {
    //on retire ce qu'il y avait dans le seat-area
    const seat_area = document.querySelector('.seat-area');
    seat_area.remove();
    //on va chercher ce qu'il y a dans le json
    const requestURL = url.value;
    const request = new Request(requestURL);
    const response = await fetch(request);
    const seat = await response.json();

    fill_seat(seat);
}