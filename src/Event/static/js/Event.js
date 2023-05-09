const searchBar = document.querySelector('#search-input');

const tagifies = document.querySelectorAll('.tagify__input');
for (const tagify of tagifies) {
    tagify.setAttribute('data-placeholder', '');
}

// searchBar.addEventListener('input', function() {
//     filterItems(this.value);
// });
//
// function  filterItems() {
//     // Récupération de toutes les lignes du corps du tableau
//     const selectUser = document.querySelector('select[name="user"]')
//     const options = selectUser.querySelectorAll('option');
//
//     // Parcours de toutes les lignes du corps du tableau pour vérifier si la ligne doit être affichée ou non
//     options.forEach(function(option) {
//         const email = option.textContent.toLowerCase();
//
//         if (email.indexOf(searchBar.value.toLowerCase()) === -1 ) {
//             // Masquer la ligne si elle ne correspond pas à la chaîne de recherche
//             option.style.display = 'none';
//         } else {
//             // Afficher la ligne si elle correspond à la chaîne de recherche
//             option.style.display = '';
//         }
//     });
// }

// Tagify for artists
const artist = document.querySelector('#artist');
const artistInput = artist.querySelector("input[name='artiste']");
const artistDiv = artist.querySelector('#artist-div');
const artistTagify = new Tagify(artistInput);
const artistTagInput = artist.querySelector('span');
artistTagInput.removeAttribute('contenteditable');
artistTagInput.setAttribute('readonly', true);

const artistText = artist.querySelector('#text');
const artistAddButton = artist.querySelector('#add-button');

function addArtist() {
    artistTagify.addTags([artistText.value]);
    artistText.value = '';
    artistText.focus();
}

artistAddButton.addEventListener('click', () => {
    addArtist();
});

artistText.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        addArtist();
    }
});

const artistDeleteButton = artist.querySelector('#del-button');
artistDeleteButton.addEventListener('click', () => {
    artistTagify.removeAllTags();
    artistText.focus();
});

// Gestion des inputs radio

const radioMontant = document.querySelector('#promo_type1');
const radioPourcentage = document.querySelector('#promo_type2');

const divMontant = document.querySelector('#montant-zone');
const divPourcentage = document.querySelector('#pourcentage-zone');
radioMontant.addEventListener('change', () => {
    divMontant.classList.remove('undisplayed');
    divPourcentage.classList.add('undisplayed');
});

radioPourcentage.addEventListener('change', () => {
    divMontant.classList.add('undisplayed');
    divPourcentage.classList.remove('undisplayed');
});

// Tagify for promo codes
const promo = document.querySelector('#promo');
const promoInput = promo.querySelector("input[name='promo_codes']");
const promoDiv = promo.querySelector('#promo-div');
const promoTagify = new Tagify(promoInput);
const promoTagInput = promo.querySelector('span');
promoTagInput.removeAttribute('contenteditable');
promoTagInput.setAttribute('readonly', true);

const promoText = promo.querySelector('#nom');
const promoMontant = promo.querySelector('#montant');
const promoPourcentage = promo.querySelector('#pourcentage');
const promoAddButton = promo.querySelector('#add-button');

function addPromoCode() {
    if (radioMontant.checked) {
        promoTagify.addTags([promoText.value + ' : ' + promoMontant.value + '€']);
        promoMontant.value = '';
    } else if (radioPourcentage.checked) {
        promoTagify.addTags([promoText.value + ' : ' + promoPourcentage.value + '%']);
        promoPourcentage.value = '';
    }
    promoText.value = '';
    promoText.focus();
}

function arePromoInputsFilled() {
    return promoText.value && (radioMontant.checked && promoMontant.value) || (radioPourcentage.checked && promoPourcentage.value);
}
promoAddButton.addEventListener('click', () => {
    if (arePromoInputsFilled()) {
        addPromoCode();
    }
});

promoMontant.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        if (arePromoInputsFilled()) {
            event.preventDefault();
            addPromoCode();
        }
    }
});

promoPourcentage.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        if (arePromoInputsFilled()) {
            event.preventDefault();
            addPromoCode();
        }
    }
});

const promoDeleteButton = promo.querySelector('#del-button');
promoDeleteButton.addEventListener('click', () => {
    promoTagify.removeAllTags();
    promoText.focus();
});

new MultiSelectTag('id_user');
