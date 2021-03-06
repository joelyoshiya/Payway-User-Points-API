# Payway - User Points API

The Payway user points API allows points related to a user's transactions (for example purchase of a product at their local grocery store) to be stored and spent on a virtual platform. This API exposes the necessary functions to read transaction data, spend points given a certain spending criteria, and finally to see balances tied to different payers, which are companies that choose to rewards the user for their loyalty to their products. 

To run the webserver, a node runtime will be necessary. Please visit [the node home site](https://nodejs.org/en/) for installation if necessary. 
Run the webserver by executing `node webService.js` at the top level of this directory

To make requests to the webserver, I used curl and the following endpoint: [http://localhost:8080](http://localhost:8080)
For example `curl http://localhost:8080/see` as a valid route serviced by the webserver.

Routes are specified as follows:

- /add : allows JSON transaction data to be added to the user account
- /spend :  allows points to be spent on the user account
- /see : returns point balances as they correspond to each payer tied to the account

 Example of curl requests sent to the web service:

```curl
curl --location --request GET 'http://localhost:8080/see'
```

Returns all payer points balances

```curl
curl --location --request PUT 'http://localhost:8080/add' \
--header 'Content-Type: application/json' \
--data-raw '{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }'
```

Adds a transaction to the user account

```curl
curl --location --request PUT 'http://localhost:8080/spend' \
--header 'Content-Type: application/json' \
--data-raw '{ "points": 5000 }'
```

Allows points to be spent on the user account, returning expenditures on successful completion

**Dependencies**:

- NodeJS
- node-fetch (`npm install node-fetch`) (see package.json)
- `"type": "module"` added to package.json (webService treated as a module as part of a larger service)
