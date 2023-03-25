let selectedSeatsIDs = [];
function changeStatus(seatID){
    let seat = document.getElementById(seatID);
    if(seat.className == "seat"){
        seat.className = "seat selected";
        selectedSeatsIDs.push(seatID);
    }
    else if (seat.className == "seat selected"){
        selectedSeatsIDs = selectedSeatsIDs.filter(function(id){
            return id !== seatID;
        })
        seat.className = "seat";
    }
    else if (seat.className == "seat sold"){
        alert("Ce siège a déjà été vendu");
    }

    sessionStorage.setItem("selectedSeatsIDs", JSON.stringify(selectedSeatsIDs));
}

