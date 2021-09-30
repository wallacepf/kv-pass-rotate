import hvac
import os
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)

vault_addr = os.getenv('VAULT_ADDR') if os.getenv('VAULT_ADDR') != '' else logging.error('VAULT_ADDR is null')
secret_rotation_time = os.getenv('SECRET_ROTATION_TIME')
role_id = os.getenv('ROLE_ID') if os.getenv('ROLE_ID') != '' else logging.error('ROLE_ID is null')
secret_id = os.getenv('SECRET_ID') if os.getenv('SECRET_ID') != '' else logging.error('SECRET_ID is null')
secret_path = os.getenv('SECRET_PATH') if os.getenv('SECRET_PATH') != '' else logging.error('SECRET_PATH is null')
secret_key = os.getenv('SECRET_KEY')

client = hvac.Client(
    url=vault_addr
)

def login():
    try:
        token = client.auth.approle.login(
            role_id=role_id,
            secret_id=secret_id
        )
        token = client.adapter.get_login_token(token)
    except Exception as err:
        logging.error(err)
    else:
        logging.info(f'Logged in. Token: {token}')
    return token
    
def passwordgen(token):
    try:
        headers = {"X-Vault-Token": f'{token}'}
        url = f'{vault_addr}/v1/sys/policies/password/demo/generate'
        r = requests.get(url, headers=headers)
        password = r.json()['data']['password']
        my_secret = {
            secret_key: r.json()['data']['password'],
        }
    except Exception as err:
        logging.error(err)
    else:
        logging.warning(
            f'Password Generation was Successful. Password: {password}')
    return my_secret


if __name__ == '__main__':
    while True:
        if client.is_authenticated():
            client.secrets.kv.v2.create_or_update_secret(
                path=secret_path,
                secret=passwordgen(token),
            )
            client.secrets.kv.v2.update_metadata(
                path=secret_path,
                delete_version_after=secret_rotation_time+"m",
            )
            read_response = client.secrets.kv.v2.read_secret_version(
                path=secret_path,
            )

            logging.info(read_response['data'])

            logging.warning(f'Sleeping {secret_rotation_time} minutes')
            time.sleep(int(os.getenv('SECRET_ROTATION_TIME')) * 60)
        else:
            token = login()
