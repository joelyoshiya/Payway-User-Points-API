# Discussion of Exercise

Overall, I enjoyed the exercise more than I expected! Refreshing on RESTful applications and the fetch API was engaging. Constructing the user account and the interactions that would keep the logic and integrity of the points tied to the account was a fun challenge, especially thinking about how to perform spending of points under the constraints. There are a few improvements I'd like to touch upon:

## More Expressive Error Codes

- Use of more expressive HTTP Status codes tied to more specific cases: i.e., use of `422 Unprocessable Entity` in the case that the client attempts to spend a negative amount of points, for example
    - Additionally, error handling was included 

## Increased modularity 

- I think an error handler that would wrap each route/call would help to clean up the code (especially the switch statement in the router request/response callback). This would help standardize the error catching process, forming a consistent response payload, that would be extendable to more api requests that could be developed in the future smoothly. Although, standardizing a payload of `[ <status_#>, "error message"]` was a step in the right direction.
- a response handler may have also cleaned up the switch statement
- the `addTransaction()` method should have been split up:
    - check for duplicate incoming transaction could have been a single function
    - updating the list of payers (with total points per payer) could have been its own method

## Localize/Parametrize the userAccount Class object

In my instance, I've left the non-persistent store of data tied to a user account as global variable. That means any method can access the `userAccount`class object at any time and modify its data, which in the long term and with respect to scalability poses a risk in terms of state, especially as calls with be asynchronous. This is mainly due the fact that properties are mutable via the dot operator. This could involve a few improvements:
- refactor so that properties of the class are private
- access via class methods (could be ES6 arrow functions) 
    - getters/setters - **synchronize** getting and setting
- pass account object via argument (will allow scalability down the line when multiple accounts may be involved/passed)

## More Robust Routing
As the API expands, it may be necessary to add more routes. It may also be necessary to tie certain routes to a certain version of the API. This would require a route handler and directory of routes (Express came to mind here).

## Further Error Checking
Especially for handling things such as requests to spend a negative amount of points, deducting spent points, etc., I would have like to do more error checking and thrown some edge cases to see how the API would behave.
