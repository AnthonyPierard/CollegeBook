
function clickable_seats_and_spaces(){
    const seats_and_spaces = document.querySelectorAll('.seat, .space')
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

function tmp_create(){
    let new_json = [];
    new_json.push({"nom" : document.querySelector('#id_nom').value})
    const seat_area = document.querySelector('.seat-area');
    let row = seat_area.childNodes;
    for (let i=0; i<row.length; i++) {
        if(row[i].classList[0] == "standing-zone"){
            new_json.push({"class" : "standing-zone"});
        }
        else if(row[i].classList[0] == "seat-row"){
            let tmp_json = {"class" : "seat-row"};
            let seats = row[i].childNodes;
            let array_seat = [];
            seats.forEach(function (seat){
                if(seat.classList.length==1){
                    array_seat.push(seat.classList[0])
                }
                else{
                    let tmp_seat= seat.classList[0];
                    seat.classList.forEach(function (clas){
                        tmp_seat = tmp_seat + " " + clas;
                    })
                    array_seat.push(tmp_seat);
                }
            })
            tmp_json["seat"] = array_seat;
            new_json.push(tmp_json);
        }
        else if(row[i].classList[0] == "none-row"){
            new_json.push({"class" : "none-row"});
        }


    }
    return new_json;
}

document.querySelector("#create_json").addEventListener("click", event => {
    //envoie le nouveu json créer au python pour créer un nouveau fichier json dans le dossier static
    //pour la nouvelle configuration
    let new_json = tmp_create();
    const debug = {coucou : "world"};
    let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var request = new Request('/configuration/create_json/', {
        method:'POST',
        headers: {'X-CSRFToken': csrfTokenValue, 'Content-Type' : 'application/json'},
        body: JSON.stringify(new_json),
    });

    fetch(request)
        .then(response => response.json())
})

