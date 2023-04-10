

//remplis le seat-area de siège ou d'espace debout
function fill_seat(obj){
    const seat_area = document.createElement('div');
    seat_area.classList.add('seat-area');
    const theatre = document.querySelector('.theatre');
    theatre.appendChild(seat_area);
    //va regarder dans le json les seats
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
    //part where when we click on a space or a seat it's change for the other one
    $('.seat').on('click', function(e){
        this.classList.remove('seat');
        this.classList.add('space');
        //don't forget to add the possibility to reclick on the object
        $('.space').on('click', function(e){
            this.classList.remove('space');
            this.classList.add('seat');
        })
    })

    $('.space').on('click', function(e){
        this.classList.remove('space');
        this.classList.add('seat');
        $('.seat').on('click', function(e) {
            this.classList.remove('seat');
            this.classList.add('space');
        })
    })


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