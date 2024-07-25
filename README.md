# Pokémon API Application

This application fetches data from the PokeAPI and stores it in a PostgreSQL database. It provides an API to query and retrieve Pokémon information either in bulk or based on their name and type.

## Setup Instructions

### Pre-requisites

- Python 3.7+
- PostgreSQL database
- API credentials from [PokeAPI](https://pokeapi.co/)

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:

   - Create a .env file in the root directory:
     ```ini
     CONFIG_PATH=config/config.ini
     ```
   - Update config/config.ini with PokeAPI configuration:

   ```ini
    [pokeapi]
    BASE_URL=https://pokeapi.co/api/v2/pokemon
    LIMIT=100
    TIMEOUT=20
   ```

   Change Limit and Timeout as needed.

4. Set up PostgreSQL database:
   - Create a PostgreSQL database.
   - Set the database URL in .env file or config/config.ini:
     ```ini
     DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
     ```
5. Initialize the database schema (Manually):

   - Use the following SQL statements to create the necessary tables:

     ```sql
     CREATE TABLE pokemon (
     id SERIAL PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     image_url TEXT
     );

     CREATE TABLE types (
         id SERIAL PRIMARY KEY,
         type_name VARCHAR(255) NOT NULL
     );

     CREATE TABLE pokemon_type (
         id SERIAL PRIMARY KEY,
         pokemon_id INT REFERENCES pokemon(id),
         type_id INT REFERENCES types(id)
     );
     ```

6. Fetch Pokémon data from PokeAPI and store in the database:
   ```ini
   python fetch_pokemon_api.py
   ```
7. Start the FastAPI application:
   ```ini
   uvicorn main:app --reload
   ```
8. Access the application:
   - Open your browser and navigate to http://localhost:8000/.
     This has a simple interactive interface to make API calls as needed.
     Filtering by name and by type can be done.
   - Use tools like curl or Postman to interact with the API endpoints.

- **API Endpoints:**
  - GET /api/v1/pokemons: Retrieve Pokémon data.
- Query Parameters:
  - name: Filter by Pokémon name (case-insensitive, partial match).
  - type: Filter by Pokémon type (case-insensitive, partial match).

### Example Usage:

```bash
    GET /api/v1/pokemons?name=pikachu&type=electric
```

### Database Schema

The application uses a PostgreSQL database with the following schema:

### Tables

1. **pokemon**

   - `id`: Primary key for the Pokémon.
   - `name`: Name of the Pokémon.
   - `image_url`: URL to the image of the Pokémon.

2. **types**

   - `id`: Primary key for the Pokémon type.
   - `type_name`: Name of the Pokémon type.

3. **pokemon_type**
   - `id`: Primary key for the Pokémon-type relationship.
   - `pokemon_id`: Foreign key referencing the `id` column in the `pokemon` table.
   - `type_id`: Foreign key referencing the `id` column in the `types` table.

### Relationships

- `pokemon` and `types` tables are related through the `pokemontype` table using foreign key constraints.

### Schema Design

This schema allows for storing Pokémon details such as their name, associated types, and image URLs in a structured manner, facilitating efficient querying and retrieval of Pokémon data through the API.

### Additional Notes

Ensure PostgreSQL is running and accessible and database is setup as per the schema used.
Adjust configurations (config.ini, .env) as per your environment.
