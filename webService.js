import http from 'http'
/*
    WebService.js
    Represents a user account instance that communicates with a client
    to update transactions on the account, see point balances,
    and spent point balances. webService tied to a single user account instance.
 */
class userAccount {
    constructor (){
        this.totPoints = 0; // account points start from zero
        this.myTransactions = []; //array of transactions coming from add route
        this.myPayers = new Map(); // Map containing payer:points key-value pairs
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
    try {
        let transaction = JSON.parse(data);
        // Check for duplicate transactions
        acct.myTransactions.forEach(oldTransaction => {
            if (transaction.payer == oldTransaction.payer
                && transaction.points == oldTransaction.points &&
                transaction.timestamp == transaction.timestamp){
                    throw new Error('duplicate transaction cannot be added');
                }
        })
        // Update list of payers with total points (used for RetPointBalances)
        if( acct.myPayers.has(transaction.payer)){
            acct.myPayers.set(transaction.payer, acct.myPayers.get(transaction.payer) + transaction.points);
        }else{
            acct.myPayers.set(transaction.payer, transaction.points);
        }
        // Add transaction to list sorted by timestamp
        if(acct.myTransactions.length == 0){
            acct.myTransactions.push(transaction);
        }else{
            // insert where the current transactions timestamp is found to
            // be earlier than the current index, else push on to end
            let date = new Date(transaction.timestamp);
            for (let index = 0; index < acct.myTransactions.length; index++) {
                let currDate = new Date(acct.myTransactions[index].timestamp);
                if(date < currDate){
                    acct.myTransactions.splice(index, 0, transaction);
                    break;
                }else if(index == (acct.myTransactions.length - 1)){
                    acct.myTransactions.push(transaction);
                    break;
                }
            }
        }
        acct.totPoints += transaction.points; //update total points count
        return [200, "successfuly added transaction"];
    }catch(err){
        return [400,err];
    }   
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
function spendPoints(request){
    try{
        let spendPoints = JSON.parse(request).points;
        if(spendPoints > acct.totPoints){
            return [400, "error: spend request exceeds points available on account"];
        }
        let unspentPoints = spendPoints;
        let expenses = [];
        // check transactions sorted old to new (by timestamp)
        for (let index = 0; index < acct.myTransactions.length; index++) {
            //console.log("unspent Points: " + unspentPoints);
            // if there are no longer any points to spend, stop checking transactions
            if(unspentPoints == 0){
                break;
            }
            let transaction = acct.myTransactions[index];
            // calculate amount to be deducted from transaction
            let deduction = 0;
            if( unspentPoints < transaction.points){
                //only spend spendPoints number of points - not the whole transaction amount
                deduction -= unspentPoints;
            }else{
                //spend the whole transaction amount
                deduction -= transaction.points;
            }
            let payer = transaction.payer;
            // since we don't want any payer's points to go negative
            if((acct.myPayers.get(payer) + deduction) >= 0){
                acct.myPayers.set(payer, acct.myPayers.get(payer) + deduction);
                unspentPoints += deduction; // the calculated deduction is no longer unspent (now spent)
                acct.totPoints += deduction; //update global counter of points for acct
                acct.myTransactions[index].points -= deduction;
                // if all points related to the transaction have been exhausted remove from transaction list
                if(acct.myTransactions[index].points == 0){
                    acct.myTransactions.splice(index, 1); //remove from current transactions (spent)
                    index -= 1;//account for splicing used transaction
                }
                let pushedPrior = false;
                expenses.forEach(entry => {
                    if(entry.payer == payer){ 
                        pushedPrior = true;
                        entry.points += deduction;
                    }else{
                        return;
                    }
                })
                if(!pushedPrior){
                    expenses.push({
                        payer: transaction.payer,
                        points: deduction
                    });
                }
            }else{
                continue;
            }
        }if(unspentPoints == 0){
            return [200, expenses];
        }else{
            return [500, "error: internal servor error - not all points requested to be spent were deducted"]
        }
    }catch(err){
        return [400, err];
    }
}

/*  
    Request header: GET
    The server will return either 200 (OK) along with the data (e.g., JSON) or 404 (NOT FOUND).

    outputs all point balancer per payer tied to user account
    Returns: a list of payers and their point balances in JSON format: [ "payer": <points>,...]
    Format: JS Object (use JSTON.stringify() upon func return to convert to JSON string for)
*/
function retPointBalances(){
    //return a data struct that only has payers and total points
    if(acct.myPayers.size == 0){
        return [404, {error: "There are no points associated with this account"}];
    }
    let payload = {}
    acct.myPayers.forEach((value, key) => {
        payload[key] = value;
    });
    return [200, payload];
}

/*
    Runs server and services requests from client
*/
function runServer(){
    const host = 'localhost';
    const port = 8080

    http.createServer((request, response) => {
    let body = [];
    request.on('error', (err) => {
        console.error(err);
    }).on('data', (chunk) => {
        body.push(chunk);
    }).on('end', () => {
        body = Buffer.concat(body).toString();        
        response.on('error', (err) => {
        console.error(err);
        });
        switch (request.url) {
            case "/add":
                if (body.length <= 0){
                    response.writeHead(400, {'Content-Type': 'application/json'});
                    response.end(JSON.stringify({error: "empty body"}));
                    break;
                }
                let result = addTransaction(body);
                response.writeHead(result[0]);
                response.end(result[1].toString());
                break
            case "/spend":
                if (body.length <= 0){
                    response.writeHead(400, {'Content-Type': 'application/json'});
                    response.end(JSON.stringify({error: "empty body"}));
                    break;
                }
                let result2 = spendPoints(body);
                if (result2[0] >= 400){
                    response.writeHead(result2[0]);
                    response.end(result2[1].toString());
                }else{
                    response.writeHead(result2[0], {'Content-Type': 'application/json'});
                    response.end(JSON.stringify(result2[1]));
                }
                break
            case "/see":
                let result3 = retPointBalances();
                response.writeHead(result3[0],{'Content-Type': 'application/json'});
                response.end(JSON.stringify(result3[1]));
                break
            default:
                response.writeHead(404);
                response.end(JSON.stringify({error:"Resource not found"}));
        }
    });
    }).listen(8080);
}

// initialize the user account class object
var acct = new userAccount();
runServer();