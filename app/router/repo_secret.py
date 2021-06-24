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

# Get Github repository public key
@router.get("/repos/{org}/{repo}/actions/secrets/public-key")
def get_github_repo_publickey(org: str,repo:str,accept:Optional[str]= 'application/vnd.github.v3+json'):
    url = "https://api.github.com/repos/{}/{}/actions/secrets/public-key".format(org,repo)
    response = requests.get(url, json={'org': org, 'repo': repo, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    if response.ok:
        return (response.json())
    else:
        return JSONResponse(status_code=404, content={"message": "Github repository public key not found"})

# Get Github Repository Secrets
@router.get("/repos/{org}/{repo}/actions/secrets/{secret_name}")
def get_github_repo_secrets(org: str,repo:str,secret_name: str,accept:Optional[str]= 'application/vnd.github.v3+json'):
    url = "https://api.github.com/repos/{}/{}/actions/secrets/{}".format(org,repo,secret_name)
    response = requests.get(url, json={'org': org, 'repo': repo, 'secret_name': secret_name,'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    if response.ok:
        return (response.json())
    else:
        return JSONResponse(status_code=404, content={"message": "Repo or org or secret not found"})

#Encritpted the secret encripted value

def encrypt(public_key: str, secret_value: str) -> str:
#"""Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")

# Create and update github Repository Secrets
@router.put("/repos/{org}/{repo}/actions/secrets/{secret_name}")
def create_update_github_repo_secret(org: str,repo: str, secret_name:str, value: str, accept:Optional[str]= 'application/vnd.github.v3+json'):
    public_key=get_github_repo_publickey(org,repo)
    encrypted_value=encrypt(public_key['key'],value)
    url = "https://api.github.com/repos/{}/{}/actions/secrets/{}".format(org,repo,secret_name)
    response = requests.put(url, json={'org': org, 'repo': repo, 'secret_name': secret_name, 'encrypted_value':encrypted_value,'key_id': public_key['key_id'],'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    
    if response.ok:
        return ({"message": "Repo secret has been Created"})
    else:
        return JSONResponse(status_code=404, content={"message": "Repo or org or secret not found"})
 
# Delete github Repository Secrets
@router.delete("/repos/{org}/{repo}/actions/secrets/{secret_name}")
def delete_github_repo_secret(org: str, repo: str, secret_name: str, accept:Optional[str]= 'application/vnd.github.v3+json'):
    url = "https://api.github.com/repos/{}/{}/actions/secrets/{}".format(org,repo,secret_name)
    response = requests.delete(url, headers={'Authorization': AUTH_TOKEN})

    if response.ok:
        return JSONResponse(status_code=200, content={"message": "Repo Secret has been deleted"})
    else:
        return JSONResponse(status_code=404, content={"message": "Repo or org or secret not found"})

