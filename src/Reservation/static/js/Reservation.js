let selectedSeatsIDs = {};
let configType;
let csrfToken = getCookie('csrftoken');
const lockedTypes = ["seat sold", "seat selected", "space"];
const seatColors = {};
//TODO: TIMEOUT
function changeStatus(seatID){
    let seat = document.getElementById(seatID);
    if(seatTypes.includes(seat.className.baseVal)){
        selectedSeatsIDs[seatID] = seat.className.baseVal;
        seat.className.baseVal = "seat selected";
        updatePrice();
    }
    else if (seat.className.baseVal == "seat selected"){
        seat.className.baseVal = selectedSeatsIDs[seatID];
        delete selectedSeatsIDs[seatID];
        updatePrice();
    }
    else if (seat.className.baseVal == "seat sold"){
        alert("Ce siège a déjà été vendu");
    }

    sessionStorage.setItem("selectedSeatsIDs", JSON.stringify(selectedSeatsIDs));
}

function canBeSelected(seatID){
    const adjacentSeats = getAdjacentSeats(seatID);
    const rightSeats = adjacentSeats[0];
    const leftSeats = adjacentSeats[1];
    if (leftSeats.length == 0 || leftSeats[0].className.baseVal == "space"){
        if (rightSeats.length == 0 || rightSeats[0].className.baseVal == "space"){
            return true;
        }
        else if (seatTypes.includes(rightSeats[0].className.baseVal) && lockedTypes.includes(rightSeats[1].className.baseVal)){
            return false;
        }
        return true;
    }

    else if (rightSeats.length == 0 || rightSeats[0].className.baseVal == "space"){
        if (leftSeats.length == 0 || leftSeats[0].className.baseVal == "space"){
            return true;
        }
        else if (seatTypes.includes(leftSeats[0].className.baseVal) && lockedTypes.includes(leftSeats[1].className.baseVal)){
            return false;
        }
        return true;
    }

    else{
        if (seatTypes.includes(rightSeats[0].className.baseVal) && rightSeats.length==1){
            return false;
        }
        else if (seatTypes.includes(leftSeats[0].className.baseVal) && leftSeats.length==1){
            return false
        }
        else if (seatTypes.includes(leftSeats[0].className.baseVal) && lockedTypes.includes(leftSeats[1].className.baseVal)){
            return false;
        }
        else if (seatTypes.includes(rightSeats[0].className.baseVal) && lockedTypes.includes(rightSeats[1].className.baseVal)){
            return false;
        }
        return true;
    }
}


function getAdjacentSeats(seatID){
    const clickedSeat = document.getElementById(seatID)
    let revelantSeats = [];
    let leftSeats = [];
    let rightSeats = [];
    let seatColumn;
    if(seatID.length == 3){
        seatColumn = parseInt(seatID[1]+seatID[2]);
    }
    else{
        seatColumn = parseInt(seatID[1]);
    }
    const previousSeat = clickedSeat.previousSibling;
    const nextSeat = clickedSeat.nextSibling;
    if(previousSeat != null){ 
        leftSeats.push(previousSeat);
        const previousSeatBis = previousSeat.previousSibling;
        if (previousSeatBis != null){
            leftSeats.push(previousSeatBis);
        }
    }
    if(nextSeat != null){
        rightSeats.push(nextSeat);
        const nextSeatBis =nextSeat.nextSibling;
        if (nextSeatBis != null){
            rightSeats.push(nextSeatBis);
        }
    }
    revelantSeats.push(leftSeats);
    revelantSeats.push(rightSeats);
    return revelantSeats;
}

function updatePrice(){

    $.ajax({
        url:"process_price/",
        type:"POST",
        data:{selectedSeatsID: JSON.stringify(selectedSeatsIDs)},
        dataType:"json",
        headers:{
            'X-CSRFToken': csrfToken
        },
        success: function(response){
            const price = response.total_price;
            const places = response.selected_seats;
            $("#price").text("Prix total : " + price + " €");
            $("#places").text(places);
        }
    });
}

function reserveSeats(callback) {
    $.ajax({
        url: "reserve_seats/",
        type: "POST",
        data: {selectedSeatsIDs: JSON.stringify(selectedSeatsIDs), currentRoom: url, roomType: configType},
        dataType: "json",
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function(response) {
            callback(response.seatsReserved);
        }
    });
}

// Code appelé lors du clic sur le bouton "Valider"
function checkBeforeSubmit() {
    checkSeats()
    .then(function() {
        window.location.href = reservationURL;
    })
    .catch(function(error) {
        alert(error);
    });
}
function checkSeats() {
    seatSelected = true;
    return new Promise(function(resolve, reject) {

        if (configType != "standing-zone"){
            for(seatID in selectedSeatsIDs){
                if (!seatID.includes("Debout")){
                    if (!canBeSelected(seatID)) {
                        //TODO: Verifier si pas le choix de laisser siege vide (e.g:9 achats sur une rangée de 10 ou 3 places dispo en tout mais groupe de 2 veut reserver)
                        seatSelected = false
                        reject("Vous ne pouvez pas laissez de place vide entre deux places vendues.\n Vérifier les sièges aux alentours de la place "+ seatID);
                    }
                }
            }
        }
        if (seatSelected){
            reserveSeats(function(result){
                if (!result){
                    reject("Vous avez tenté de sélectionner un siège déjà vendu");
                }
                else{
                    resolve();
                }
            })
        }
        
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  async function prepare_json(url) {
    //on retire ce qu'il y avait dans le seat-area
    window.addEventListener("load", function() {
        document.getElementById("validateButton").addEventListener('click',checkBeforeSubmit);
    });
    if(url.value!="nothing"){
        const seat_area = document.querySelector('.seat-area');
        seat_area.remove();
        //on va chercher ce qu'il y a dans le json
        const requestURL = url;
        const request = new Request(requestURL);
        const response = await fetch(request);
        const seat = await response.json();
        if (seat[0]["class"] == "standing-zone" && seat[1]["class"] == "undefined" || (seat[1]["class"] == "standing-zone" && seat[2]["class"] == "undefined")){
            configType = "standing-zone"
        }
        else if((seat[0]["class"] == "standing-zone" && seat[1]["class"] != "undefined") || (seat[1]["class"] == "standing-zone" && seat[2]["class"] != "undefined") ){
            configType = "standing-zone+seat"
        }
        else{
            configType = "seat"
        }
        if (configType != "standing-zone" && configType!="standing-zone+seat"){
            fill_seat(seat);
        }
        else{
            console.log(configType)
            fill_page(seat)
        }
        defineColors();
    }
  
  }
  
//remplis le seat-area de siège ou d'espace debout
function fill_seat(json_dictionnary){
    let charcode = 65;
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

            if (json_dictionnary[index].seat != null) {
                let placeNumber = 1;
                const all_seat = json_dictionnary[index].seat;

                for (const seat of all_seat) {
                    const svg_seat = create_seat_svg()
                    const new_seat = seat.split(' ');
                    const seat_id = String.fromCharCode(charcode) + String(placeNumber);
                    for (const class_seat of new_seat) {
                        svg_seat.classList.add(class_seat);
                        if (class_seat == "seat"){
                            svg_seat.id = seat_id;
                            svg_seat.onclick = function(){
                                changeStatus(this.id);
                            };
                            placeNumber = placeNumber + 1;
                        } 
                    }
                    row.appendChild(svg_seat);
                }
                charcode = charcode+1;
            }
        }

    }
}

function fill_page(json_dictionnary) {
    let inputLabelText = "Cette représentation ne propose que des places debouts. Veuillez séléctionner le nombre de place que vous souhaitez réserver"
    let keys = [];
    let remainingSeats;
    if(json_dictionnary[1] != undefined){
        inputLabelText = "Cette représentation propose aussi des places debouts. Si vous souhaitez réserver des places debouts, entrez directement le nombre dans le champs ci-dessous";
        fill_seat(json_dictionnary)
    }

    const selectDiv = document.createElement('div');
    selectDiv.classList.add("input-box");
    selectDiv.setAttribute('id', 'standing-seats');

    const content = document.querySelector('.details');
    content.appendChild(selectDiv)

    const inputLabel = document.createTextNode(inputLabelText);
    
    const inputBox = document.createElement("input");
    inputBox.type = "number";
    inputBox.id = "seatSelection";
    inputBox.min = "0";
    inputBox.required = true;
    inputBox.step ="1";
    inputBox.value = "0";
    inputBox.addEventListener('input', function() {
        if(json_dictionnary[1] != undefined){
            keys = []
            for(let key in selectedSeatsIDs){
                if (selectedSeatsIDs[key]=="seat debout"){
                    console.log(key)
                    keys.push(key)
                }
            }
        }
        else {
            keys = Object.keys(selectedSeatsIDs);
        }
        if (inputBox.value > keys.length){
            console.log("plus petit", inputBox.value, keys.length)
            const seatsOffset = inputBox.value - keys.length;
            for (let i = 0; i < seatsOffset; i++){
                selectedSeatsIDs["Debout"+(keys.length+i)] = "seat debout";
            }
        }
        else if (inputBox.value < keys.length){
            console.log("plus grand", inputBox.value, keys.length)
            const seatsOffset = keys.length - inputBox.value;
            for (let i = keys.length-1 ; i >= keys.length - seatsOffset; i--){
                const key = keys[i];
                delete selectedSeatsIDs[key];
            }
        }
        sessionStorage.setItem("selectedSeatsIDs", JSON.stringify(selectedSeatsIDs));
        updatePrice();
    });

    if(json_dictionnary[0]["class"] == "standing-zone"){
        remainingSeats = document.createTextNode("Il reste actuellement "+ json_dictionnary[0]["nbr_place"] + " places disponnibles") 
    }
    else if (json_dictionnary[0]["class"] == "none"){
        remainingSeats = document.createTextNode("Il reste actuellement "+ json_dictionnary[1]["nbr_place"] + " places disponnibles") 
    }
    


    selectDiv.appendChild(inputLabel)
    selectDiv.appendChild(inputBox)
    selectDiv.appendChild(remainingSeats)

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

function defineColors() {
    const caption = document.getElementById('caption');
    const sold = document.createElement('div');
    const selected = document.createElement('div');
    const labelSold = document.createElement('p');
    const labelSelected = document.createElement('p');
    const soldSeat = create_seat_svg();
    const selectedSeat = create_seat_svg();
    sold.classList.add("seat-caption")
    selected.classList.add("seat-caption")
    sold.style.color = "#fc8c0f";
    selected.style.color = "#268085";
    labelSold.textContent= "Vendu";
    labelSelected.textContent= "Sélectionné";
    sold.appendChild(labelSold);
    sold.appendChild(soldSeat);
    selected.appendChild(labelSelected);
    selected.appendChild(selectedSeat);
    caption.appendChild(sold);
    caption.appendChild(selected);

    seatTypes.forEach( (type) => {
        if (type !== 'seat debout') {
            const cleanedType = type.replace('seat ', '');
            setColor(cleanedType);
            const seatType = document.createElement('div');
            seatType.classList.add("seat-caption")
            seatType.style.color = seatColors[cleanedType];
            const label = document.createElement('p');
            label.textContent= cleanedType;
            const seat = create_seat_svg();
            seatType.appendChild(label);
            seatType.appendChild(seat);
            caption.appendChild(seatType);
        }
    })
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

function random_color(){
    const hex = Math.floor(Math.random() * 16777215).toString(16);
    return '#' + ('000000' + hex).slice(-6);
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