let selectedSeatsIDs = [];

function fill_seat(json_dictionnary){
    let charcode = 65;
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
            let placeNumber = 1;
            const all_seat = json_dictionnary[index].seat;

            for (const seat of all_seat){
                const marker_seat = document.createElement('div');
                const new_seat = seat.split(' ');
                const seat_id = String.fromCharCode(charcode) + String(placeNumber);
                for (const class_seat of new_seat) {
                    marker_seat.classList.add(class_seat);
                    if (class_seat == "seat"){
                        marker_seat.id = seat_id;
                        marker_seat.onclick = function(){
                            changeStatus(this.id);
                        };
                        placeNumber = placeNumber + 1;
                    } 
                }
                row.appendChild(marker_seat);
            }
            charcode = charcode+1;
        }

    }
}

async function prepare_json(url) {
    console.log("test");
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

function changeStatus(seatID){
    let seat = document.getElementById(seatID);
    if(seat.className == "seat"){
        if(canBeSelected(seatID)){
            updatePrice(true);
            seat.className = "seat selected";
            selectedSeatsIDs.push(seatID);
        }
        //TODO : Deux groupes de siege avec espace au milieu
        else alert("Vous ne pouvez pas laissez de place vide entre deux places vendues");
    }
    else if (seat.className == "seat selected"){
        selectedSeatsIDs = selectedSeatsIDs.filter(function(id){
            return id !== seatID;
        })
        updatePrice(false);
        seat.className = "seat";
    }
    else if (seat.className == "seat sold"){
        alert("Ce siège a déjà été vendu");
    }
    updateSeats();


    sessionStorage.setItem("selectedSeatsIDs", JSON.stringify(selectedSeatsIDs));
}

function canBeSelected(seatID){
    const adjacentSeats = getAdjacentSeats(seatID);
    console.log(adjacentSeats);
    const leftSeats = adjacentSeats[1];
    const rightSeats = adjacentSeats[0];
    console.log("leftSeats: ", leftSeats);
    console.log("rightSeats: ", rightSeats);
    if (leftSeats.length == 0){
        console.log("pas de siege gauche");
        if (rightSeats.length == 0){
            return true;
        }
        else if (rightSeats[0].className == "seat" && (rightSeats[1].className == "seat sold" || rightSeats[1].className == "seat selected")){
            return false;
        }
        return true;
    }

    else if (rightSeats.length == 0){
        console.log("pas de siege droit");
        if (leftSeats.length == 0){
            return true;
        }
        else if (leftSeats[0].className == "seat" && (leftSeats[1].className == "seat sold" || leftSeats[1].className == "seat selected")){
            return false;
        }
        return true;
    }

    else{
        if (rightSeats[0].className == "seat" && rightSeats.length==1){
            return false;
        }
        else if (leftSeats[0].className == "seat" && leftSeats.length==1){
            return false
        }
        else if (leftSeats[0].className == "seat" && (leftSeats[1].className == "seat sold" ||leftSeats[1].className == "seat selected")){
            return false;
        }
        else if (rightSeats[0].className == "seat" && (rightSeats[1].className == "seat sold" || rightSeats[1].className == "seat selected")){
            return false;
        }
        return true;
    }
}


function getAdjacentSeats(seatID){
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
    console.log(seatID);
    console.log(seatColumn)
    console.log(seatID[0]+String(seatColumn-1));
    const previousSeat = document.getElementById(seatID[0]+String(seatColumn-1));
    const nextSeat = document.getElementById(seatID[0]+String(seatColumn+1));
    const previousSeatBis = document.getElementById(seatID[0]+String(seatColumn-2));
    const nextSeatBis = document.getElementById(seatID[0]+String(seatColumn+2));
    console.log(previousSeat,previousSeatBis)
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

function updatePrice(isIncreasing){
    const displayed_price = document.getElementById("price");
    stringPrice = displayed_price.innerHTML;
    stringPrice.slice(0,-1);
    let price = parseInt(stringPrice);
    if (isIncreasing){
        price = price + 5;
    }
    else{
        if (price > 0) {
            price = price - 5;
        }
    }
    displayed_price.innerHTML = String(price)+"€";
    sessionStorage.setItem("price", price);
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