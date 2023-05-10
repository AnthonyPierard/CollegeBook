//rends les sièges clickables
function clickable_seats_and_spaces(){
    const seats_and_spaces = document.querySelectorAll('.seat, .space');
    for (const element of seats_and_spaces) {
        element.addEventListener('click', () => {
            element.classList.toggle('seat');
            element.classList.toggle('space');
        })
    }
}

//créer un élément au dessus qui permet de sélectionner une ligne entière
function clickable_select_row(){
    const select_rows = document.querySelectorAll('.select-row');
    for (const select_row of select_rows) {
        select_row.addEventListener('click', () => {
            const row = select_row.parentNode;
            const all_seat = row.childNodes;
            all_seat.forEach(function (seat){
                if(seat.classList[0] != "select-row"){
                    seat.classList.toggle('seat');
                    seat.classList.toggle('space');
                }
            })
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
        const select_row = document.createElement('div');
        select_row.classList.add("select-row");
        row.appendChild(select_row);
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
    clickable_seats_and_spaces();
    clickable_select_row();

}
//fonction pour choisir le json
async function prepare_json(url) {
    //on retire ce qu'il y avait dans le seat-area
    if(url.value!="rien"){
        const seat_area = document.querySelector('.seat-area');
        seat_area.remove();
        //on va chercher ce qu'il y a dans le json
        const requestURL = url.value;
        const request = new Request(requestURL);
        const response = await fetch(request);
        const seat = await response.json();

        fill_seat(seat);
    }

}

//création du json de la page HTML
function create_json_from_html(){
    let json = [];
    json.push({"nom" : document.querySelector('#id_nom').value});
    
    const seat_area = document.querySelector('.seat-area');
    
    const rows = seat_area.childNodes;
    rows.forEach(row => {
        const row_class = row.classList[0];

        if (row_class === "standing-zone") {
            json.push({"class" : "standing-zone"});
        } else if (row_class === "seat-row") {
            const row_json = create_seat_row_json(row);
            json.push(row_json);
        } else if (row_class === "none-row") {
            json.push({"class" : "none-row"});
        }
    });
    
    return json;
}

function create_seat_row_json(row) {
    const row_json = {"class" : 'seat-row'};
    const seats = row.childNodes;
    const row_seats = [];

    seats.forEach(seat => {
        const seat_class = seat.ClassList[0];

        if (seat_class !== "select-row") {
            const seat_json = create_seat_json(seat);
            row_seats.push(seat_json);
        }
    });

    row_json["seat"] = row_seats;
    
    return row_json;
}

function create_seat_json(seat) {
    const seat_class = seat.ClassList;
    let seat_json = seat_class[0];

    if (seat_class.length > 1) {
        seat_json = seat_class.join(" ")
    }

    return seat_json;
}

//création de la requête et envoi à la fonction python
document.querySelector("#create_json").addEventListener("click", event => {
    //envoie le nouveu json créer au python pour créer un nouveau fichier json dans le dossier static
    //pour la nouvelle configuration
    if (document.querySelector('#option').classList.length == 0) {

        let new_json = create_json_from_html();
        let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
        var request = new Request('/configuration/create_json/', {
            method: 'POST',
            headers: {'X-CSRFToken': csrfTokenValue, 'Content-Type': 'application/json'},
            body: JSON.stringify(new_json),
        });

        fetch(request)
            .then(response => response.json())
    }

})
