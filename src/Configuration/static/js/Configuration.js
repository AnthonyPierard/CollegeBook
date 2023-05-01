const edition_mode = document.getElementsByName("mode");
let selected_mode = "";

edition_mode.forEach((mode) => {
  mode.addEventListener('change', function() {
    if (mode.checked) {
      selected_mode = mode.value;
    }
  });
});

//rends les sièges clickables
function clickable_seats_and_spaces(){
    const seats_and_spaces = document.querySelectorAll('.seat, .space');
    for (const element of seats_and_spaces) {
        element.addEventListener('click', (event) => {
            if (!element.classList.contains('space') && selected_mode === "assignation") {
                set_place_type(element);
                console.log("OK")
            } else {
                element.classList.toggle('seat');
                element.classList.toggle('space');
            }
        });
    }
}

//créer un élément au dessus qui permet de sélectionner une ligne entière
function clickable_select_row() {
    const select_rows = document.querySelectorAll('.select-row');
    for (const select_row of select_rows) {
        select_row.addEventListener('click', (event) => {
            const row = select_row.parentNode;
            const all_seat = row.childNodes;

            all_seat.forEach(function(seat) {
                if (seat.classList[0] !== "select-row") {
                    if (!seat.classList.contains('space') && selected_mode === "assignation") {
                        const types = document.querySelectorAll("#checkboxList input[type='checkbox']");
                        let selected_type = "";

                        types.forEach((type) => {
                            if (type.checked) {
                              selected_type = type.value.replace(" ", "").toLowerCase();
                            }
                        });

                        const other_classes = [...seat.classList].filter(c => c !== 'seat' && c !== 'space');
                        other_classes.forEach((c) => {
                            seat.classList.remove(c);
                        });

                        if (selected_type !== "") {
                            if (!seat.classList.contains(selected_type)) {
                                seat.classList.add(selected_type);

                                let styleTag = document.querySelector('style');
                                if (!styleTag) {
                                    styleTag = document.createElement('style');
                                    document.head.appendChild(styleTag);
                                }

                                // Récupérer la feuille de style et la règle CSS correspondant au type de siège
                                const styleSheet = styleTag.sheet;
                                const rule = Array.from(styleSheet.cssRules).find((r) => r.selectorText === `.seat.${selected_type}`);

                                // Vérifier si une couleur a déjà été générée pour ce type de siège
                                let color = seatColors[selected_type];
                                if (!color) {
                                    // Générer une nouvelle couleur
                                    color = random_color();
                                    seatColors[selected_type] = color;
                                }

                                // Ajouter une nouvelle règle CSS si elle n'existe pas, sinon mettre à jour la règle existante
                                if (!rule) {
                                    styleSheet.insertRule(`.seat.${selected_type} { background-color: ${color}; }`, styleSheet.cssRules.length);
                                } else {
                                    rule.style.backgroundColor = color;
                                }
                            }
                        }
                    } else {
                        seat.classList.toggle('seat');
                        seat.classList.toggle('space');
                    }
                }
            });
        });
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
        if(json_dictionnary[index].class!="none") {
            const row = document.createElement('div');
            row.classList.add(json_dictionnary[index].class);
            seat_area.appendChild(row);
            const select_row = document.createElement('div');
            select_row.classList.add("select-row");
            row.appendChild(select_row);
            if (json_dictionnary[index].seat != null) {
                const all_seat = json_dictionnary[index].seat;

                for (const seat of all_seat) {
                    const marker_seat = document.createElement('div');
                    const new_seat = seat.split(' ');
                    for (const class_seat of new_seat) {
                        marker_seat.classList.add(class_seat);
                    }
                    row.appendChild(marker_seat);
                }
            }
        }

    }
    clickable_seats_and_spaces();
    clickable_select_row();

}
//fonction pour choisir le json
async function prepare_json(url) {
    //on retire ce qu'il y avait dans le seat-area
    if(url.value!="nothing"){
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
function tmp_create(){
    let new_json = [];
    new_json.push({"nom" : document.querySelector('#id_name').value, "class" : "none"})
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
                    if(seat.classList[0]!="select-row"){
                        array_seat.push(seat.classList[0]);
                    }
                }
                else{
                    if(seat.classList[0]!="select-row"){
                        let tmp_seat= "";
                        let i = 0;
                        seat.classList.forEach(function (clas){
                            if (i==0){
                                tmp_seat = clas;
                            }
                            else {
                                tmp_seat = tmp_seat + " " + clas;
                            }
                            i++;
                        })
                        array_seat.push(tmp_seat);
                    }
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

//création de la requête et envoi à la fonction python du json
document.querySelector("#create_json").addEventListener("click", event => {
    //envoie le nouveu json créer au python pour créer un nouveau fichier json dans le dossier static
    //pour la nouvelle configuration
    if (document.querySelector('#option').value == "nothing") {
        let new_json = tmp_create();
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

//rendre disable l'input submit si c'est le choix --------
const select = document.querySelector('#config_choice');
const submit = document.querySelector('#create_json');
select.addEventListener('change', function (){
    const value = select.value;

    if(value==='nothing'){
        submit.disabled = true;
    }
    else {
        submit.disabled = false;
    }
})


//obtenir la config
function get_config(){
    // Récupérer l'élément de sélection par son ID
    const selectElement = document.getElementById("config_choice");

    // Récupérer la valeur sélectionnée
    const selectedValue = selectElement.value;

    // Afficher la valeur sélectionnée
    console.log(selectedValue);

    return selectedValue;

}

//récuperer les types de places dans le tagify
function get_place_types(){
    const places = document.getElementsByName("place_types");
    let placeValues = places[0].value;
    let allPlaces = placeValues.split(";");
    const checkboxList = document.getElementById('checkboxList');

    while (checkboxList.firstChild) {
        checkboxList.removeChild(checkboxList.firstChild);
    }

    allPlaces.forEach((place) => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = "choice";
        checkbox.value = place.split(":")[0];
        checkboxList.appendChild(checkbox);

        const label = document.createElement('label');
        label.appendChild(document.createTextNode(place.split(":")[0]));
        checkboxList.appendChild(label);

        checkbox.addEventListener('click', () => {
        const checkboxes = document.querySelectorAll('input[name=choice]');
        checkboxes.forEach((cb) => {
          if (cb !== checkbox) {
            cb.checked = false;
          }
        });
      });
    });
}

//ajout ou suppression toute les 2 secondes
setInterval(get_place_types,2000);

function random_color(){
    const hex = Math.floor(Math.random() * 16777215).toString(16);
    return '#' + ('000000' + hex).slice(-6);
}

const seatColors = {};

// attribuer un type à un siège
function set_place_type(seat) {
    const types = document.querySelectorAll("#checkboxList input[type='checkbox']");
    let selected_type = "";

    types.forEach((type) => {
        if (type.checked) {
          selected_type = type.value.replace(" ", "").toLowerCase();
        }
    });

    seat.addEventListener('click', function() {
        const seat_classes = seat.classList;
        seat_classes.forEach((seat_class) => {
            if (seat_class !== "seat" && seat_class !== "space") {
                seat.classList.remove(seat_class);
            }
        });
        if (selected_type != "") {
            if (!seat.classList.contains(selected_type)) {
                seat.classList.add(selected_type);

                let styleTag = document.querySelector('style');
                if (!styleTag) {
                    styleTag = document.createElement('style');
                    document.head.appendChild(styleTag);
                }

                // Récupérer la feuille de style et la règle CSS correspondant au type de siège
                const styleSheet = styleTag.sheet;
                const rule = Array.from(styleSheet.cssRules).find((r) => r.selectorText === `.seat.${selected_type}`);

                // Vérifier si une couleur a déjà été générée pour ce type de siège
                let color = seatColors[selected_type];
                if (!color) {
                    // Générer une nouvelle couleur
                    color = random_color();
                    seatColors[selected_type] = color;
                }

                // Ajouter une nouvelle règle CSS si elle n'existe pas, sinon mettre à jour la règle existante
                if (!rule) {
                    styleSheet.insertRule(`.seat.${selected_type} { background-color: ${color}; }`, styleSheet.cssRules.length);
                } else {
                    rule.style.backgroundColor = color;
                }
            }
        }
    });
}
