let selectedSeatsIDs = [];
let csrfToken = getCookie('csrftoken');

function changeStatus(seatID){
    let seat = document.getElementById(seatID);
    if(seat.className.baseVal == "seat"){
        seat.className.baseVal = "seat selected";
        selectedSeatsIDs.push(seatID);
        updatePrice(true);
        //TODO : Deux groupes de siege avec espace au milieu
    }
    else if (seat.className.baseVal == "seat selected"){
        selectedSeatsIDs = selectedSeatsIDs.filter(function(id){
            return id !== seatID;
        })
        seat.className.baseVal = "seat";
        updatePrice(false);
    }
    else if (seat.className.baseVal == "seat sold"){
        alert("Ce siège a déjà été vendu");
    }
    updateSeats();


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
        else if (rightSeats[0].className.baseVal == "seat" && (rightSeats[1].className.baseVal == "seat sold" || rightSeats[1].className.baseVal == "seat selected" || rightSeats[1].className.baseVal == "space")){
            return false;
        }
        return true;
    }

    else if (rightSeats.length == 0 || rightSeats[0].className.baseVal == "space"){
        if (leftSeats.length == 0 || leftSeats[0].className.baseVal == "space"){
            return true;
        }
        else if (leftSeats[0].className.baseVal == "seat" && (leftSeats[1].className.baseVal == "seat sold" || leftSeats[1].className.baseVal == "seat selected" || leftSeats[1].className.baseVal == "space")){
            return false;
        }
        return true;
    }

    else{
        if (rightSeats[0].className.baseVal == "seat" && rightSeats.length==1){
            return false;
        }
        else if (leftSeats[0].className.baseVal == "seat" && leftSeats.length==1){
            return false
        }
        else if (leftSeats[0].className.baseVal == "seat" && (leftSeats[1].className.baseVal == "seat sold" || leftSeats[1].className.baseVal == "seat selected" || leftSeats[1].className.baseVal == "space")){
            return false;
        }
        else if (rightSeats[0].className.baseVal == "seat" && (rightSeats[1].className.baseVal == "seat sold" || rightSeats[1].className.baseVal == "seat selected" || rightSeats[1].className.baseVal == "space")){
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
    const previousSeatBis = previousSeat.previousSibling;
    const nextSeatBis =nextSeat.nextSibling;
    if(previousSeat != null){ 
        leftSeats.push(previousSeat);
    }
    if(nextSeat != null){
        rightSeats.push(nextSeat);
    }
    if(previousSeatBis != null){
        leftSeats.push(previousSeatBis);
    }
    if(nextSeatBis != null){
        rightSeats.push(nextSeatBis);
    }
    revelantSeats.push(leftSeats);
    revelantSeats.push(rightSeats);
    return revelantSeats;
}

function updatePrice(){

    $.ajax({
        url:"process_price/",
        type:"POST",
        data:{selectedSeatsID: selectedSeatsIDs},
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
        data: {selectedSeatsIDs: selectedSeatsIDs, currentRoom: url},
        dataType: "json",
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function(response) {
            callback(response.seatsReserved);
        }
    });
}


function updateSeats(){
    const displayedSeats = document.getElementById("places");
    displayedSeats.innerHTML = "";
    selectedSeatsIDs.sort();

    for(seatId of selectedSeatsIDs){
        if (seatId == selectedSeatsIDs[selectedSeatsIDs.length-1]){
            displayedSeats.innerHTML += seatId;
        }
        else {
            displayedSeats.innerHTML += seatId + ", ";
        }
    }

}
function checkSeats() {
    return new Promise(function(resolve, reject) {
      // Votre code de vérification ici
        for(seatID in selectedSeatsIDs){
            if (!canBeSelected(selectedSeatsIDs[seatID])) {
                reject("Vous ne pouvez pas laissez de place vide entre deux places vendues.\n Vérifier les sièges aux alentours de la place "+ selectedSeatsIDs[seatID]);
            }
        }
        reserveSeats(function(result){
            if (!result){
                reject("Vous avez tenté de sélectionner un siège déjà vendu");
            }
            else{
                resolve();
            }
        })

    });
  }
  
  // Code appelé lors du clic sur le bouton "Valider"
  function checkBeforeSubmit() {
    checkSeats()
      .then(function() {
        // Le code suivant sera exécuté si la promesse est résolue
        // C'est-à-dire si la condition de vérification est vérifiée
        // Rediriger vers la page suivante
        window.location.href = reservationURL;
      })
      .catch(function(error) {
        // Le code suivant sera exécuté si la promesse est rejetée
        // C'est-à-dire si la condition de vérification n'est pas vérifiée
        // Afficher le message d'erreur
        alert(error);
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

        fill_seat(seat);
    }

}