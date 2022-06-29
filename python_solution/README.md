# Payway - User Points API

The Payway user points API allows points related to a user's transactions (for example purchase of a product at their local grocery store) to be stored and spent on a virtual platform. This API exposes the necessary functions to read transaction data, spend points given a certain spending criteria, and finally to see balances tied to different payers, which are companies that choose to rewards the user for their loyalty to their products. 

Routes are specified as follows:

- /add : allows JSON transaction data to be added to the user account
- /spend :  allows points to be spent on the user account
- /see : returns point balances as they correspond to each payer tied to the account
