## Installation
1. Copy `.env.example` and rename it to `.env` and fill out the environment variables.
2. On root project run
    ```
    docker compose up
    ```
3. App will be served on configured port

## Usage
API Documentation is on the insomnia collection. Here is the endpoints:

- `POST /products`: to add a product
- `GET /products?srotBy=<sortBy>`: to get poroduct based on given sort by

Allowed `<sortBy>`:
> *) Not case sensitive 
- `Terbaru` - sort by newest added product
- `Termurah` - sort by cheapest price
- `Termahal` - sort by the most expensive price
- `Nameasc` - sort by name ascending
- `Namedesc` - sort by name descending

Default `sortBy` value is `Terbaru`

## Architecture Decision
I following the project layout standard from [Flask official documentation](https://flask.palletsprojects.com/en/2.2.x/tutorial/layout/). Which is every usecase is treated as [Blueprint](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Blueprint). But I added some separation between business logic and database operation. For business logic I keep it on blueprint's routes and for database operation I put it in `/model` folder. This way make the code more maintainable because when you change the business logic, you have low chance to messed up the database operation code.

In this project, cache mechanism and containerization is implemented.