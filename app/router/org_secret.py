from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from os import environ
import requests
from typing import Optional
from fastapi import FastAPI
from pybase64 import b64encode
from nacl import encoding, public


app = FastAPI()

router = APIRouter()

load_dotenv()
AUTH_TOKEN="Bearer "+environ.get('GITHUB_PAT')

# List organization secrets
@router.get("/orgs/{org}/actions/secrets")
def get_github_org_secrets(org: str,accept:Optional[str]= 'application/vnd.github.v3+json'):
    url = "https://api.github.com/orgs/{}/actions/secrets".format(org)
    response = requests.get(url, json={'org': org, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    if response.ok:
        return (response.json())
    else:
        return JSONResponse(status_code=404, content={"message": "org is not found"})


# Get an organization public key
@router.get("/orgs/{org}/actions/secrets/public-key")
def get_github_org_publickey(org: str,accept:Optional[str]= 'application/vnd.github.v3+json'):
    url = "https://api.github.com/orgs/{}/actions/secrets/public-key".format(org)
    response = requests.get(url, json={'org': org, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    return (response.json())


#Encritpted the secret encripted value

def encrypt(public_key: str, secret_value: str) -> str:
#"""Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


# Create or update an organization secret

@router.put("/orgs/{org}/actions/secrets/{secret_name}")
def create_update_github_org_secret(org: str, secret_name:str, secret_value: str, visibility: str='private', accept:Optional[str]= 'application/vnd.github.v3+json'):
    public_key=get_github_org_publickey(org)
    encrypted_value=encrypt(public_key['key'],secret_value)
    url = "https://api.github.com/orgs/{}/actions/secrets/{}".format(org,secret_name)
    response = requests.put(url, json={'org': org, 'secret_name': secret_name, 'encrypted_value':encrypted_value,'key_id': public_key['key_id'],'accept': accept, 'visibility':visibility}, headers={'Authorization': AUTH_TOKEN})


    if response.ok:
        return ({"message": "Org secret has been Created"})
    else:
        return JSONResponse(status_code=204, content={"message": "org or secret is not found"})

# Delete an organization secret

@router.delete("/orgs/{org}/actions/secrets/{secret_name}")
def delete_github_org_secret(org: str, secret_name: str, accept:Optional[str]= 'application/vnd.github.v3+json'):
    url = "https://api.github.com/orgs/{}/actions/secrets/{}".format(org,secret_name)
    response = requests.delete(url, headers={'Authorization': AUTH_TOKEN})

    if response.ok:
        return JSONResponse(status_code=200, content={"message": "Org Secret has been deleted"})
    else:
        return JSONResponse(status_code=404, content={"message": "Org or secret not found"})

