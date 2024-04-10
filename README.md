# rubrik-daily-check
 Python script to check your Rubrik enviroment health

## Dependencies
- requests

## How to use it.

1- Create a JSON file named `config.json` with your Rubrik Security Cloud (RSC) and RSC Service Account information, like in the example below:
```
{
	"client_id": "your_client_id",
	"client_secret": "your_client_secret",
	"name": "name_you_gave",
	"access_token_uri": "https://yourdomain.my.rubrik.com/api/client_token",
	"graphql_url": "https://yourdomain.my.rubrik.com/api/graphql"
}
```
2- Download this repository and place in a computer or server that has access to your Rubrik CDMs

3- Run main.py
