# Payway - User Points API

The Payway user points API allows points related to a user's transactions (for example purchase of a product at their local grocery store) to be stored and spent on a virtual platform. This API exposes the necessary functions to read transaction data, spend points given a certain spending criteria, and finally to see balances tied to different payers, which are companies that choose to rewards the user for their loyalty to their products.

## Running the server

1. Navigate to `/python_solution/main`

2. When in the `main` directory, run `uvicorn main:app --reload` on the command line

The server is now up and running!

## Routes

Routes are first and foremost tied to individual user accounts via the path `/users/{username}`

For example, the route for user with username `yoshi` would be `http://127.0.0.1:8000/users/yoshi`

Routes are specified as follows:

- /add : allows JSON transaction data to be added to the user account
- /spend :  allows points to be spent on the user account
- /points : returns point balances as they correspond to each payer tied to the account

Things I worked on and polished with this project:

- Unit testing, and Test Driven Development (via Pytest)
- Using different APIs to communicate with the webserver (fetch/node.js, fastapi)
- Understanding of Python Data Classes
