# account-checker
REST API service which checks if there is an account at mi.com for given phone number or e-mail or not.

## Usage
Run in our bash terminal:  
curl -i -X POST https://xiaomi-account-checker.herokuapp.com/check_user/phone_or_email  
OR  
curl -i -X GET https://xiaomi-account-checker.herokuapp.com/check_user/phone_or_email  


Second one will search only in database.

Don't forget to replace phone_or_email by valid value you want to check.
