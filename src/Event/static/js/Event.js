const searchBar = document.querySelector("#search-input");

const tagifies = document.querySelectorAll(".tagify__input");
    for (const tagify of tagifies) {
        tagify.setAttribute("data-placeholder", "")
    }


searchBar.addEventListener('input', function() {
    filterItems(this.value);
});

function  filterItems() {
    // Récupération de toutes les lignes du corps du tableau
    const selectUser = document.querySelector('select[name="user"]')
    const options = selectUser.querySelectorAll('option');

    // Parcours de toutes les lignes du corps du tableau pour vérifier si la ligne doit être affichée ou non
    options.forEach(function(option) {
        const email = option.textContent.toLowerCase();

        if (email.indexOf(searchBar.value.toLowerCase()) === -1 ) {
            // Masquer la ligne si elle ne correspond pas à la chaîne de recherche
            option.style.display = 'none';
        } else {
            // Afficher la ligne si elle correspond à la chaîne de recherche
            option.style.display = '';
        }
    });
}

//Tagify for artists&
const artist = document.querySelector("#artist");
const artistInput = artist.querySelector("input[name='artiste']")
const artistTagify = new Tagify(artistInput);
const artistTagInput = artist.querySelector("span");
artistTagInput.removeAttribute("contenteditable")
artistTagInput.setAttribute("readonly", true)
const artistText = artist.querySelector("#text");
const artistAddButton = artist.querySelector("#add-button");
artistAddButton.addEventListener('click', () => {
    artistTagify.addTags([artistText.value]);
    artistText.value = "";
    artistText.focus()
});
const artistDeleteButton = artist.querySelector("#del-button");
artistDeleteButton.addEventListener('click', () => {
    artistTagify.removeAllTags();
    artistText.focus();
});

//Tagify for promo codes
const promo = document.querySelector("#promo");
const promoInput = promo.querySelector("input[name='promo_codes']");
const promoTagify = new Tagify(promoInput);
const promoTagInput = promo.querySelector("span");
promoTagInput.removeAttribute("contenteditable")
promoTagInput.setAttribute("readonly", true)

const promoText = promo.querySelector("#nom");
const promoAddButton = promo.querySelector("#add-button");

promoAddButton.addEventListener('click', () => {
    promoTagify.addTags([promoText.value]);
    promoText.value = "";
    promoText.focus()
});

const promoDeleteButton = promo.querySelector("#del-button");
promoDeleteButton.addEventListener('click', () => {
    promoTagify.removeAllTags();
    promoText.focus();
});

//Gestion des inputs radio

const radioMontant = document.querySelector("#promo_type1")
const radioPourcentage = document.querySelector("#promo_type2")

const divMontant = document.querySelector("#montant-zone")
const divPourcentage = document.querySelector("#pourcentage-zone")
radioMontant.addEventListener('change', () => {
    divMontant.classList.remove("undisplayed");
    divPourcentage.classList.add("undisplayed");
})

radioPourcentage.addEventListener('change', () => {
    divMontant.classList.add("undisplayed");
    divPourcentage.classList.remove("undisplayed");

})