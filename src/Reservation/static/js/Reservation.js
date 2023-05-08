let selectedSeatsIDs = {};
let configType;
let csrfToken = getCookie('csrftoken');
const lockedTypes = ["seat sold", "seat selected", "space"];

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
            $("#places").text("Siège(s) sélectionné(s) : " + places);
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
            fill_page(seat)
        }
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
    let remainingSeatsText;
    let remainingSeats
    if(json_dictionnary[1] != undefined){
        inputLabelText = "Cette représentation propose aussi des places debouts. Si vous souhaitez réserver des places debouts, entrez directement le nombre dans le champs ci-dessous";
        fill_seat(json_dictionnary)
    }

    const selectDiv = document.createElement('div');
    selectDiv.classList.add("input-box") 

    const theatre = document.querySelector('.theatre');
    theatre.appendChild(selectDiv)

    const inputLabel = document.createTextNode(inputLabelText);
    
    const inputBox = document.createElement("input");
    inputBox.type = "number";
    inputBox.id = "seatSelection";
    inputBox.min = "0";
    inputBox.required = true;
    inputBox.step ="1";
    inputBox.value = "0";

    if(json_dictionnary[0]["class"] == "standing-zone"){
        remainingSeatsText = document.createTextNode("Il reste actuellement "+ json_dictionnary[0]["nbr_place"] + " places disponnibles");
        remainingSeats=json_dictionnary[0]["nbr_place"];
        inputBox.max=remainingSeats
    }
    else if (json_dictionnary[0]["class"] == "none"){
        remainingSeatsText = document.createTextNode("Il reste actuellement "+ json_dictionnary[1]["nbr_place"] + " places disponnibles")
        remainingSeats=json_dictionnary[1]["nbr_place"]; 
        inputBox.max=remainingSeats
    }

    inputBox.addEventListener('input', function() {
        if(json_dictionnary[1] != undefined || (json_dictionnary[0]["name"] != "undefined" && json_dictionnary[2] != undefined)){
            keys = []
            for(let key in selectedSeatsIDs){
                if (selectedSeatsIDs[key]=="seat debout"){
                    keys.push(key)
                }
            }
        }
        else {
            keys = Object.keys(selectedSeatsIDs);
        }
        if(inputBox.value>remainingSeats){
            console.log("salut")
            inputBox.value = remainingSeats
            alert("Vous ne pouvez pas demander plus de places debout qu'il n'y en a de disponibles")
        }
        if (inputBox.value > keys.length){
            const seatsOffset = inputBox.value - keys.length;
            for (let i = 0; i < seatsOffset; i++){
                selectedSeatsIDs["Debout"+(keys.length+i)] = "seat debout";
            }
        }
        else if (inputBox.value < keys.length){
            const seatsOffset = keys.length - inputBox.value;
            for (let i = keys.length-1 ; i >= keys.length - seatsOffset; i--){
                const key = keys[i];
                delete selectedSeatsIDs[key];
            }
        }
        sessionStorage.setItem("selectedSeatsIDs", JSON.stringify(selectedSeatsIDs));
        updatePrice();
    });


 
    


    selectDiv.appendChild(inputLabel)
    selectDiv.appendChild(inputBox)
    selectDiv.appendChild(remainingSeatsText)

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
