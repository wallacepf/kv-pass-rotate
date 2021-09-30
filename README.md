# Static Password Rotation

This script was made to auto-rotate static secrets using a simple password as an example

## How to use

You can run this script using a docker container image (You can find in DockerHub or here in GitHub)
Or, you can do it manually with python.

To run it locally, install all the required packages with pip:

```bash
pip install -r requirements.txt
python main.py
```

## ENV Vars

This script uses env vars to configure itself. The following env vars are needed:

VAULT_ADDR - Address of Vault's server
ROLE_ID - Role ID
SECRET_ID - Secret ID
SECRET_PATH - Secret Path where the script will write the secret
SECRET_KEY - Once we use KV as secret engine, wiht this envvar you set the secret's key name
SECRET_ROTATION_TIME - Here you set the rotation time in minutes (this info should be provided in int)



