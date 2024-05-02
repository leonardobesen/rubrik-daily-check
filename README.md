# rubrik-daily-check

Python script to check your Rubrik enviroment health

## Dependencies

- requests
- pandas
- google-api-python-client
- google-auth-oauthlib

## How to use it.

1- Create a JSON file named `config.json` with your Rubrik Security Cloud (RSC) and RSC Service Account information like in the example below and add it inside `../rubrik-daily-check/configutarion/` folder:

```
{
	"client_id": "your_client_id",
	"client_secret": "your_client_secret",
	"name": "name_you_gave",
	"access_token_uri": "https://yourdomain.my.rubrik.com/api/client_token",
	"graphql_url": "https://yourdomain.my.rubrik.com/api/graphql",
	"google_drive_upload_folder_id": ["your_drive_folders_ids_here"],
	"tz_info": "America/Sao_Paulo"
}
```

_OBS_: `google_drive_upload_folder_id` and `tz_info` are OPTIONAL.

- If `tz_info` is not declared or left blank (`""`) it will use UTC+0
- if `google_drive_upload_folder_id` or left blank (`""`) it will **skip** the process that upload the file to Google Drive

2 - _(Skip this step if you didnt declare `google_drive_upload_folder_id` on `config.json`)_
You must create a file named `google_drive.json` on `../rubrik-daily-check/configutarion/` folder. See the file example below:

```
{
  "installed": {
    "client_id": "your_client_id",
    "project_id": "your_project_id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "your_client_secret",
    "redirect_uris": ["http://localhost"]
  }
}
```

3- Download this repository and place in a computer or server that has access to your Rubrik CDMs

4- Run main.py
