import http from 'http'
/*
Please write a web service that accepts HTTP requests and 
returns responses based on the conditions outlined in the next
 */


// design specific requests/responses that are inbound and outbound on the web service
// must be able to listen in for HTTP requests and handle response appropriately
// must have an internal data structure with payer, points, and transaction dates specified

//must architect specific responses for each route

// incoming data will most likely be a JSON string (easier for transporting)
var jsObject = { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" };
var transaction = JSON.stringify(jsObject); //this is the format we will expect coming to the server
var jsObject2 = { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }
var transaction2 = JSON.stringify(jsObject2);


class userAccount {
    constructor (transactions){
        this.totPoints = 0; //initialized to zero
        this.myTransactions = []; //array of transactions coming from add route
        this.myPayers = new Map(); // Map containing payer:points key-value pairs

        // this.myTransactions.push(JSON.parse(transaction)); //represent a transaction being added (JSobject)
        // this.myTransactions.push(JSON.parse(transaction2));
        // this.myTransactions.forEach(transaction => this.totPoints += transaction.points);
        //console.log("my total points: " + this.totPoints);
    }    
}

/*  
    Input: JSON String representing one single transaction

    Request header: PUT (
    The server will return 200 (OK) or 204 (No Content). If the information does not exist, 
    the API may create the resource, as done in a POST request, and return 201 (Created).)

    a route that takes in JSON string regarding of the format:
    '{ "payer": <payer_name>, "points": <integer>, "timestamp": <date in JS Date.toJSON() format> }'
    and adds to list of transactions pertinent to user account / updates total points
*/
function addTransaction(data){
    //turn JSON string into object
    let transaction = JSON.parse(data);

    //TODO check for duplicate transaction (same timestamp)

    if( acct.myPayers.has(transaction.payer)){
        acct.myPayers.set(transaction.payer, acct.myPayers.get(transaction.payer) + transaction.points);
    }else{
        acct.myPayers.set(transaction.payer, transaction.points);
    }
    acct.myPayers.forEach((value,key) => console.log(key,value));

    //push transaction into proper location based on date (old -> new)
    // will use Array.prototype.splice() based on Date value
    // insert where the current transactions timestamp is found to be earlier than the current index (start from beginning), else push on to end
    let date = new Date(transaction.timestamp);
    for (let index = 0; index < acct.myTransactions.length; index++) {
        let currDate = new Date(acct.myTransactions[index].timestamp);
        if(date < currDate){
            acct.myTransactions.splice(index, 0, transaction);
            break;
        }else if(index == (acct.myTransactions.length - 1)){
            console.log("at the end!");
            acct.myTransactions.push(transaction);
        }
    }
    acct.myTransactions.forEach(transaction => console.log(transaction));
    acct.totPoints += transaction.points; //update total points count
return 200;
}

/*
    Request header: PUT (
    The server will return 200 (OK) or 204 (No Content). If the information does not exist, 
    the API may create the resource, as done in a POST request, and return 201 (Created).)

    Request Ex. Format: { "points": 5000 }
    Function that spends a user specified number of points on the account based on the following conditions:
    Conditions:
        We want the oldest points to be spent first (oldest based on transaction timestamp, not the order they’re received)
        We want no payer's points to go negative.
    Returns: a list of points spent ​{ "payer": <string>, "points": <integer> }​ 
*/
function spendPoints(numPoints){
    if(numPoints > acct.totPoints){

    }
    // check a ds holding transactions sorted old to new
    // check if subtracting transaction pts would put payer total sum neg
    // if not, spend the points
    // if so, skip transaction
    // check if numPoints spent, if not move to next oldest transaction

    acct.totPoints -= numPoints;
}

/*  
    Request header: GET
    The server will return either 200 (OK) along with the data (e.g., JSON) or 404 (NOT FOUND).

    outputs all point balancer per payer tied to user account
    Returns: a list of point balances per payer ​{ "payer": <string>, "points": <integer> }​ 
*/
function retPointBalances(acct){
    //return a data struct that only has payers and total points
    var pointBalances = {}; 
    class payer_points {
        constructor(payer, points){
            this.payer = payer
            this.points = points
        }
    }
    acct.myTransactions.forEach(transaction => 
       Object.assign(pointBalances, {payer:transaction.payer, points:transaction.points}));
    return pointBalances;
}

function runServer(){
    const host = 'localhost';
    const port = 8080

    http.createServer((request, response) => {
    const { headers, method, url } = request;
    let body = [];
    request.on('error', (err) => {
        console.error(err);
    }).on('data', (chunk) => {
        body.push(chunk);
    }).on('end', () => {
        body = Buffer.concat(body).toString();
          // at this point, `body` has the entire request body stored in it as a string
        //console.log("body: " + body);
        
        // FORMATION OF RESPONSE
        response.on('error', (err) => {
        console.error(err);
        });
        switch (request.url) {
            case "/add":
                let status_code = addTransaction(body, acct);
                console.log("tot points now: " + acct.totPoints)
                response.writeHead(status_code);
                response.end("transaction added");
                break
            case "/spend":
                let expenses = spendPoints(request,body, acct);
                response.writeHead(200, {'Content-Type': 'application/json'})
                response.write(expenses);
                response.end();
                break
            case "/see":
                response.writeHead(200, {'Content-Type': 'application/json'})
                let pts = JSON.stringify(retPointBalances(acct));
                console.log("pts :" + pts);
                response.write(pts);
                response.end(pts);
                break
            default:
                response.writeHead(404);
                response.end(JSON.stringify({error:"Resource not found"}));
        }
        // Note: the 2 lines above could be replaced with this next one:

        //const responseBody = { headers, method, url, body };

        //response.write(JSON.stringify(responseBody));
        //response.end();

        // Note: the 2 lines above could be replaced with this next one:
        // response.end(JSON.stringify(responseBody))

        // END OF NEW STUFF
    });
    }).listen(port, host, () => {
        console.log(`Server is running on http://${host}:${port}`);
    });
}

// initialize the user account class object
var acct = new userAccount(transaction);
// run server
runServer();