const searchBar = document.querySelector("#search-input");

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
