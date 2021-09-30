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

```bash
# Address of Vault's server
export VAULT_ADDR=
# Role ID
export ROLE_ID=
# Secret ID
export SECRET_ID=
# Secret Path where the script will write the secret
# This should be provided without the secret root's path
# it will assume that you're using secret/ as the mount point
export SECRET_PATH=
#Once we use KV as secret engine, wiht this envvar you set the secret's key name
export SECRET_KEY=
# Here you set the rotation time in minutes (this info should be provided in int)
export SECRET_ROTATION_TIME=
```
## Vault Config Example

```bash
vault auth enable approle


vault write auth/approle/role/app1 \
    secret_id_ttl=0 \
    token_num_uses=100 \
    token_ttl=20m \
    token_policies=demo \
    secret_id_num_uses=40

vault write sys/policies/password/demo policy=@password_policy.hcl

vault policy write demo policy.hcl

```

## Password policy example

```bash
length=30

rule "charset" {
  charset = "abcdefghijklmnopqrstuvwxyz"
  min-chars = 1
}

rule "charset" {
  charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  min-chars = 1
}

rule "charset" {
  charset = "0123456789"
  min-chars = 1
}

rule "charset" {
  charset = "!@#$%^&*"
  min-chars = 1
}
```

## Policy Example

```bash
path "secret/data/demo/pwd" {
    capabilities=["read", "create", "update"]
}

path "secret/metadata/demo/pwd" {
    capabilities=["update"]
}

path "sys/policies/password/demo/generate" {
    capabilities=["read"]
}
```




