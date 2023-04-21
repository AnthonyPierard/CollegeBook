let selectedSeatsIDs = [];
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
    const element = document.getElementById("price");
    stringPrice = element.innerHTML;
    stringPrice.slice(0,-1);
    let price = parseInt(stringPrice);
    if (isIncreasing){
        price = price + 5;
    }
    else{
        price = price - 5;
    }
    element.innerHTML = String(price)+"€";
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