const edition_mode = document.getElementsByName("mode");
let selected_mode = "";
const seatColors = {'sold': '#fc8c0f', 'selected': '#268085','classic': '#555555', 'vip': '#ef18a7'};
const style = document.createElement('style');

//Tagify for seatType
const seatType = document.querySelector("#seat_types");
const seatTypeInput = seatType.querySelector("#id_place_types")
const promoMontant = seatType.querySelector("#montant");
const seatTypeTagify = new Tagify(seatTypeInput);
const seatTypeTagInput = seatType.querySelector("span");
seatTypeTagInput.removeAttribute("contenteditable")
seatTypeTagInput.setAttribute("readonly", true)

const seatTypeText = seatType.querySelector("#text");
const seatTypeAddButton = seatType.querySelector("#add-button");


create_checkbox_element("sold");
create_checkbox_element("classic");
defineColors()

function addSeatType() {
    if( seatTypeText.value && promoMontant.value){
        seatTypeTagify.addTags([seatTypeText.value + " : " + promoMontant.value + "€"]);
        seatTypeText.value = "";
        promoMontant.value = "";
        seatTypeText.focus()
    }
}

seatTypeAddButton.addEventListener('click', () => {
    addSeatType();
    defineColors();
});

seatTypeText.addEventListener('keydown', function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        addSeatType();
    }
});

promoMontant.addEventListener('keydown', function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        addSeatType();
    }
});

const seatTypeDeleteButton = seatType.querySelector("#del-button");
seatTypeDeleteButton.addEventListener('click', () => {
    seatTypeTagify.removeAllTags();
    seatTypeText.focus();
});

function defineColors() {
    if (!seatColors["sold"]){
        setColor("sold")
        setColor("classic")
    }

    if (seatTypeTagify.value) {
        for(const tag of seatTypeTagify.value){
            const type= tag.value.split(":")[0].replace(" ", "").toLowerCase();
            if(!seatColors[tag.value]){
                setColor(type)
            }
        }
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
    }
    if (!rule) {
        styleSheet.insertRule(`.seat.${placeType} { color: ${color}; }`, styleSheet.cssRules.length);
    } else {
        rule.style.color = color;
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
            } else if (selected_mode == "suppression"){
                if(element.classList.length>1){
                    const classes = element.classList;
                    element.classList.remove(classes[0]);
                    element.classList.remove(classes[0]);
                    element.classList.add('space');

                }
                else{
                    console.log("else")
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
    svg.setAttribute('height', '32');
    svg.setAttribute('width', '32');
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

function fill_types(seats) {
    const seat_types = seats[0].seat_types;
    seatTypeTagify.removeAllTags();
    seatTypeTagify.addTags(seat_types);
}

function is_class_in_json(class_name, json) {
    for (const element of json) {
        if (Object.values(element).includes(class_name)){
            return true;
        }
    }
    return false;
}

function reset_info_element(element) {
    element.classList.add("undisplayed");
    element.querySelector("input").required = false;
}

function make_info_element_visible(element) {
    element.classList.remove("undisplayed");
    element.querySelector("input").required = true;
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
            // if(json_dictionnary[index].class=="standing-zone"){
            //     if (!document.querySelector("#nbr-place")) {
            //         const basic_infos = document.querySelector('#basic-infos')
            //         const nbr_place = document.createElement('div')
            //         const price_place = document.createElement('div')
            //         const input_nbr_place = document.createElement('input');
            //         const input_price_place = document.createElement('input');
            //         nbr_place.id = "nbr-place";
            //         price_place.id="price_place"
            //         input_nbr_place.type="number";
            //         input_nbr_place.step = "1";
            //         input_nbr_place.min = "1";
            //         input_nbr_place.id="value_place";
            //         input_nbr_place.value=json_dictionnary[index].nbr_place;
            //         input_price_place.type="number";
            //         input_price_place.step = "0.01";
            //         input_price_place.min = "0.01";
            //         nbr_place.innerHTML = "Nombre de places debout";
            //         price_place.innerHTML = "Prix des places debout";
            //         price_place.appendChild(input_price_place);
            //         nbr_place.appendChild(input_nbr_place);
            //         basic_infos.appendChild(price_place);
            //         basic_infos.appendChild(nbr_place);
            //     }
            // }
        }
    }

    const classic_price = document.querySelector("#classic-price");
    const standing_price = document.querySelector("#standing-price");
    const standing_number = document.querySelector("#standing-number");

    reset_info_element(classic_price)
    reset_info_element(standing_price)
    reset_info_element(standing_number)
    if(is_class_in_json("seat-row", json_dictionnary)) {
        make_info_element_visible(classic_price);
    }
    if(is_class_in_json("standing-zone", json_dictionnary)) {
        make_info_element_visible(standing_price);
        make_info_element_visible(standing_number);
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

        fill_types(seat);
        fill_seat(seat);
    }

}

//création du json de la page HTML
function tmp_create(){
    let types = [];
    //Charge les éléments du tagify
    for (const tag of seatTypeTagify.value) {
        types.push(tag.value)
    }
    console.log(types);
    let new_json = [];
    new_json.push({"nom" : document.querySelector('#id_name').value, "class" : "none", "seat_types": types})
    const seat_area = document.querySelector('.seat-area');
    let row = seat_area.childNodes;
    for (let i=0; i<row.length; i++) {
        if(row[i].classList[0] == "standing-zone"){
            const nbr_place = document.querySelector("#id_standing_number").value;
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
    //envoie le nouveau json créé au python pour créer un nouveau fichier json dans le dossier static
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

function create_checkbox_element(name) {
    const checkbox_div = document.createElement('div');
    checkbox_div.classList.add('checkbox-div');
    const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = "choice";
        checkbox.value = name;
        checkbox_div.appendChild(checkbox)

        const label = document.createElement('label');
        label.appendChild(document.createTextNode(name));
        checkbox_div.appendChild(label);


        checkbox_div.appendChild(create_seat_svg());

        checkboxList.appendChild(checkbox_div);
        checkbox.addEventListener('click', () => {
            const checkboxes = document.querySelectorAll('input[name=choice]');
            checkboxes.forEach((cb) => {
                if (cb !== checkbox) {
                    cb.checked = false;
                }
            });
        });
}
let nbr_cat = 0;

//récuperer les types de places dans le tagify
function get_place_types(){
    nbr_cat_now = seatTypeTagify.value.length
    if(nbr_cat!=nbr_cat_now){
        const checkboxList = document.getElementById('checkboxList');

        while (checkboxList.firstChild) {
            checkboxList.removeChild(checkboxList.firstChild);
        }

        create_checkbox_element("sold");
        create_checkbox_element("classic");
        seatTypeTagify.value.forEach((type) => {
            create_checkbox_element(type.value.split(":")[0]);
        });
        defineColors();
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
          console.log(selected_type)
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

setInterval(set_checkbox_color, 2000);

function set_checkbox_color() {
    const checkboxes = document.querySelectorAll('#checkboxList .checkbox-div');
    checkboxes.forEach((checkbox) => {
        const label = checkbox.querySelector('label');
        const labelValue = label.textContent.toLowerCase().replace(" ", "");
        if (seatColors.hasOwnProperty(labelValue)) {
            const color = seatColors[labelValue.replace(" ", "")];
            checkbox.style.color = color;
        }
    });
}
