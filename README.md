# Fetch Rewards Coding Exercise - Backend Software Engineering

My solution is the following:

To run the webserver, a node runtime will be necessary.
Please run the webserver by executing node webService.js at the top level of this directory

To make requests to the webserver, use curl and the following endpoint: [http://localhost:8080](http://localhost:8080)
For example `curl http://localhost:8080/seepoints`

Another example:

```curl
curl --location --request GET 'http://localhost:8080/see'
```

```curl
curl --location --request PUT 'http://localhost:8080/add' \
--header 'Content-Type: application/json' \
--data-raw '{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }'
```

```curl
curl --location --request PUT 'http://localhost:8080/spend' \
--header 'Content-Type: application/json' \
--data-raw '{ "points": 5000 }'
```

Routes are specified as follows:

- /add : allows transaction data to be added to the user account
- /spend :  allows points to be spent on the user account
- /see : returns point balances as they correspond to each payer

Dependencies: NodeJS
Other dependencies: npm install node-fetch (see package.json)

- "type": "module" added to package.json


