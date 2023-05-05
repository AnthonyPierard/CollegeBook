const edition_mode = document.getElementsByName("mode");
let selected_mode = "";
const seatColors = {};
const style = document.createElement('style');

function defineColors() {
    setColor("sold")
    const places = document.getElementsByName("place_types");
    let placeValues = places[0].value;
    let allPlaces = placeValues.split(";");
    console.log(seatColors)
    for (let place of allPlaces) {
        place = place.split(":")[0].replace(" ", "").toLowerCase();
        setColor(place)
    }
}

function setColor(placeType) {
  let color = seatColors[placeType];
  let styleTag = document.querySelector('style');
  if (!styleTag) {
    styleTag = document.createElement('style');
    document.head.appendChild(styleTag);
  }
  const styleSheet = styleTag.sheet;
  const rule = Array.from(styleSheet.cssRules).find((r) => r.selectorText === `.seat.${placeType}`);
  if (!color) {
    color = getDistinctColor();
    seatColors[placeType] = color;
    if (!rule) {
      styleSheet.insertRule(`.seat.${placeType} { color: ${color}; }`, styleSheet.cssRules.length);
    } else {
      rule.style.color = color;
    }
  }
}

function getDistinctColor() {
  let color;
  do {
    color = random_color();
  } while (Object.values(seatColors).some(c => colorDiff(c, color) < 200));
  return color;
}

function colorDiff(c1, c2) {
  const r1 = parseInt(c1.substr(1, 2), 16);
  const g1 = parseInt(c1.substr(3, 2), 16);
  const b1 = parseInt(c1.substr(5, 2), 16);
  const r2 = parseInt(c2.substr(1, 2), 16);
  const g2 = parseInt(c2.substr(3, 2), 16);
  const b2 = parseInt(c2.substr(5, 2), 16);
  return Math.abs(r1 - r2) + Math.abs(g1 - g2) + Math.abs(b1 - b2);
}

defineColors()

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
            } else if (selected_mode == "suppression"){
                if(element.classList.length>1){
                    element.classList.forEach(function (classe){
                        element.classList.remove(classe);
                        element.classList.add('space');
                    })
                }
                else{
                    element.classList.remove('space');
                    element.classList.add('seat');
                    element.classList.add('classic');
                }
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
                                    styleSheet.insertRule(`.seat.${selected_type} { color: ${color}; }`, styleSheet.cssRules.length);
                                } else {
                                    rule.style.color = color;
                                }
                            }
                        }
                    } else if (selected_mode === "suppression"){
                        if(seat.classList.length>1){
                            seat.classList.forEach(function (classe){
                                seat.classList.remove(classe);
                                seat.classList.add('space');
                            })
                        }
                        else{
                            seat.classList.remove('space');
                            seat.classList.add('seat');
                            seat.classList.add('classic');
                        }
                    }
                }
            });
        });
    }
}

function create_seat_svg() {
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewbox', "0 0 32 32");
    create_path_svg(svg, "M9,29H5c-1.1,0-2-0.9-2-2V17c0-1.7,1.3-3,3-3h0c1.7,0,3,1.3,3,3V29z");
    create_path_svg(svg, "M27,29h-4V17c0-1.7,1.3-3,3-3h0c1.7,0,3,1.3,3,3v10C29,28.1,28.1,29,27,29z");
    create_rect_svg(svg, 9, 19, 14, 10)
    create_rect_svg(svg, 9, 9, 14, 10)
    create_path_svg(svg, "M6,14V7.8C6,5.7,7.7,4,9.8,4h12.3C24.3,4,26,5.7,26,7.8V14");
    return svg
}

function create_path_svg(parent,  d) {
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', d);
    path.classList.add("seat-style");
    parent.appendChild(path)
}

function create_rect_svg(parent, x, y, width, height) {
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute("x", x);
    rect.setAttribute("y", y);
    rect.setAttribute("width", width);
    rect.setAttribute("height", height);
    rect.classList.add("seat-style");
    parent.appendChild(rect)
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
            if(row.classList.contains("seat-row")){
                const select_row = document.createElement('div');
                const select_row_svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                const select_row_path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                select_row_svg.setAttribute("width","16")
                select_row_svg.setAttribute("height","16")
                select_row_svg.setAttribute("fill","currentColor")
                select_row_svg.setAttribute("viewBox","0 0 16 16")
                select_row_svg.classList.add("bi")
                select_row_svg.classList.add("bi-arrow-down-circle-fill")
                select_row_path.setAttribute("d","M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v5.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V4.5z")
                select_row_svg.appendChild(select_row_path)
                select_row.appendChild(select_row_svg)
                select_row.classList.add("select-row");
                row.appendChild(select_row);
            }

            if (json_dictionnary[index].seat != null) {
                const all_seat = json_dictionnary[index].seat;

                for (const seat of all_seat) {
                    const svg_seat = create_seat_svg()
                    const new_seat = seat.split(' ');
                    for (const class_seat of new_seat) {
                        svg_seat.classList.add(class_seat);
                    }
                    row.appendChild(svg_seat);
                }
            }
            if(json_dictionnary[index].class=="standing-zone"){
                const nbr_place = document.querySelector("#nbr_place");
                const input_nbr_place = document.createElement('input');
                input_nbr_place.type="number";
                input_nbr_place.id="value_place";
                input_nbr_place.value=json_dictionnary[index].nbr_place;
                nbr_place.innerHTML = "Nombre de place debout :";
                nbr_place.appendChild(input_nbr_place);
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
            const nbr_place = document.querySelector("#value_place").value;
            new_json.push({"class" : "standing-zone", "nbr_place" : nbr_place});
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

//recevoir les types depuis le json
function get_file_types(){
    const current_config = get_config().replaceAll("/", "_");
    const xhr = new XMLHttpRequest();

    // Configurez la requête avec la méthode GET et l'URL de la vue Django
    xhr.open('GET', `get_place_types/${current_config}`);

    // Définissez l'en-tête de la requête pour spécifier que nous voulons recevoir des données JSON
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Attachez une fonction de rappel pour traiter la réponse lorsque la requête est terminée
    xhr.onload = function() {
        // Vérifiez que la requête s'est terminée avec succès
        if (xhr.status === 200) {
          // Parsez la réponse JSON en un objet JavaScript
          const djangoModel = JSON.parse(xhr.responseText);
          // Utilisez l'objet DjangoModel ici comme vous le souhaitez
          console.log(djangoModel);
        } else {
        console.log(xhr.status)
        console.log('Erreur lors de la récupération de l\'objet Django.');
        }
    };

    // Envoyez la requête
    xhr.send();
}

/* Pour plus tard créer les checkbox via cette fonction
function create_checkbox(place){
    const checkboxList = document.getElementById('checkboxList');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.name = "choice";
    checkbox.value = place;
    checkboxList.appendChild(checkbox);

    const label = document.createElement('label');
    label.appendChild(document.createTextNode(place));
    checkboxList.appendChild(label);

    checkbox.addEventListener('click', () => {
    const checkboxes = document.querySelectorAll('input[name=choice]');
    checkboxes.forEach((cb) => {
      if (cb !== checkbox) {
        cb.checked = false;
      }
    });
}*/

let nbr_cat = 0;
//récuperer les types de places dans le tagify
function get_place_types(){
    const places = document.getElementsByName("place_types");
    let placeValues = places[0].value;
    let allPlaces = placeValues.split(";");
    let nbr_cat_now;
    if(allPlaces[0].length === 0){
        nbr_cat_now = 0;
    } else {
        nbr_cat_now = allPlaces.length;
    }
    if(nbr_cat!=nbr_cat_now){
        const checkboxList = document.getElementById('checkboxList');

        while (checkboxList.firstChild) {
            checkboxList.removeChild(checkboxList.firstChild);
        }

        const sold_checkbox = document.createElement('input');
        sold_checkbox.type = 'checkbox';
        sold_checkbox.name = "choice";
        sold_checkbox.value = "sold";
        checkboxList.appendChild(sold_checkbox);

        const sold_label = document.createElement('label');
        sold_label.appendChild(document.createTextNode("sold"));
        checkboxList.appendChild(sold_label);

        sold_checkbox.addEventListener('click', () => {
            const checkboxes = document.querySelectorAll('input[name=choice]');
            checkboxes.forEach((cb) => {
                if (cb !== sold_checkbox) {
                    cb.checked = false;
                }
            });
        });

        const classic_checkbox = document.createElement('input');
        classic_checkbox.type = 'checkbox';
        classic_checkbox.name = "choice";
        classic_checkbox.value = "classic";
        checkboxList.appendChild(classic_checkbox);

        const classic_label = document.createElement('label');
        classic_label.appendChild(document.createTextNode("classic"));
        checkboxList.appendChild(classic_label);

        classic_checkbox.addEventListener('click', () => {
            const checkboxes = document.querySelectorAll('input[name=choice]');
            checkboxes.forEach((cb) => {
                if (cb !== classic_checkbox) {
                    cb.checked = false;
                }
            });
        });

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
        nbr_cat = nbr_cat_now;
    }

}

//ajout ou suppression toute les 2 secondes
setInterval(get_place_types,2000);

function random_color(){
    const hex = Math.floor(Math.random() * 16777215).toString(16);
    return '#' + ('000000' + hex).slice(-6);
}


// attribuer un type à un siège
function set_place_type(seat) {
    const types = document.querySelectorAll("#checkboxList input[type='checkbox']");
    let selected_type = "";

    types.forEach((type) => {
        if (type.checked) {
          selected_type = type.value.replace(" ", "").toLowerCase();
        }
    });

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
                styleSheet.insertRule(`.seat.${selected_type} { color: ${color}; }`, styleSheet.cssRules.length);
            } else {
                rule.style.color = color;
            }
        }
    }
}

function set_checkbox_color() {
    const checkboxes = document.querySelectorAll('#checkboxList input[type="checkbox"]');

    checkboxes.forEach((checkbox) => {
        const label = checkbox.nextElementSibling;
        const labelValue = label.textContent.toLowerCase();
        if (seatColors.hasOwnProperty(labelValue)) {
            console.log('GOOOOOD');
            const color = seatColors[labelValue];
            label.style.color = color;
        } else {
            console.log('NUUUL');
            console.log(seatColors);
            console.log(labelValue);
            console.log(seatColors[labelValue]);
        }
    });
}


setInterval(set_checkbox_color, 2000);

function set_checkbox_color() {
    const checkboxes = document.querySelectorAll('#checkboxList input[type="checkbox"]');

    checkboxes.forEach((checkbox) => {
        const label = checkbox.nextElementSibling;
        const labelValue = label.textContent.toLowerCase().replace(" ", "");
        if (seatColors.hasOwnProperty(labelValue)) {
            const color = seatColors[labelValue.replace(" ", "")];
            label.style.color = color;
        }
    });
}

document.addEventListener('keydown', function(event) {
  if (event.ctrlKey) {
    get_file_types();
  }
});