async function fetchPokemons() {
    try {
        const response = await fetch('/api/v1/pokemons');
        if (!response.ok) {
            throw new Error('Failed to fetch Pokémon data');
        }
        const pokemons = await response.json();
        displayPokemons(pokemons);
    } catch (error) {
        console.error('Error fetching Pokémon data:', error);
    }
}

async function fetchPokemonsFilter() {
    const name = document.getElementById('name').value;
    const type = document.getElementById('type').value;

    try {
        // Construct the URL with query parameters
        let url = '/api/v1/pokemons';
        if (name || type) {
            url += `?`;
            if (name) url += `name=${encodeURIComponent(name)}&`;
            if (type) url += `type=${encodeURIComponent(type)}&`;
            // Remove trailing "&"
            url = url.slice(0, -1);
        }

        const response = await fetch(url);
        const pokemons = await response.json();
        displayPokemons(pokemons);
    } catch (error) {
        console.error('Error fetching Pokémon data:', error);
    }
}

function displayPokemons(pokemons) {
    const pokemonList = document.getElementById('pokemon-list');
    pokemonList.innerHTML = ''; // Clear previous content

    pokemons.forEach(pokemon => {
        const pokemonItem = document.createElement('div');
        pokemonItem.classList.add('pokemon-item');
        pokemonItem.innerHTML = `
            <h3>${pokemon.name}</h3>
            <img src="${pokemon.image_url}" alt="${pokemon.name}" style="width: 100px; height: 100px;">
            <p>Types:</p>
            <ul>
                ${pokemon.types.map(type => `<li>${type.type_name}</li>`).join('')}
            </ul>
            <hr>
        `;
        pokemonList.appendChild(pokemonItem);
    });
}
