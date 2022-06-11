import fetch from "node-fetch";


//can reach server via : http://localhost:8080
function fetchSampleData(){
    fetch("https://ipinfo.io/json")
    .then(function (response) {
        return response.json();
    })
    .then(function (myJson){
        console.log(myJson);
    })
    .catch(function (error) {
        console.log("error : " + error);
    })
    return;
}

function postTransactions(){

}

function spendPoints(){

}

function getBalances(){

}

fetchSampleData();