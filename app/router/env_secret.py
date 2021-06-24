from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from os import environ
import requests
from typing import Optional
from fastapi import FastAPI
from pybase64 import b64encode
from nacl import encoding, public
from app.router.repository import get_github_repo

app = FastAPI()

router = APIRouter()

load_dotenv()
AUTH_TOKEN="Bearer "+environ.get('GITHUB_PAT')

# List environment secrets
@router.get("/repositories/environments/{environment_name}/secrets")
def get_github_repo_env_secrets(org: str, repo:str, environment_name:str, accept:Optional[str]= 'application/vnd.github.v3+json'):
    github_repo=get_github_repo(org,repo)
    repository_id=github_repo['id']
    url = "https://api.github.com/repositories/{}/environments/{}/secrets".format(github_repo['id'],environment_name)
    response = requests.get(url, json={'repository_id': repository_id, 'environment_name': environment_name, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    if response.ok:
        return (response.json())
    else:
        return JSONResponse(status_code=404, content={"message": "Repo or org or secret not found"})

# Get an environment public key

@router.get("/repositories/environments/{environment_name}/secrets/public-key")
def get_github_repo_env_pub_key(org: str, repo:str, environment_name:str, accept:Optional[str]= 'application/vnd.github.v3+json'):
    github_repo=get_github_repo(org,repo)
    repository_id=github_repo['id']
    url = "https://api.github.com/repositories/{}/environments/{}/secrets/public-key".format(github_repo['id'],environment_name)
    response = requests.get(url, json={'repository_id': repository_id, 'environment_name': environment_name, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    return (response.json())


#Encritpted the secret encripted value

def encrypt(public_key: str, secret_value: str) -> str:
#"""Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")

# Create or update an environment secret

@router.put("/repositories/environments/{environment_name}/secrets/{secret_name}")
def create_update_github_repo_env_secrets(org: str, repo:str, environment_name:str,secret_name:str, secret_value: str, accept:Optional[str]= 'application/vnd.github.v3+json'):
    github_repo=get_github_repo(org,repo)

    if 'message' in github_repo.keys():
        return JSONResponse(status_code=404, content={"message": "Validation error when the environment name or repo or org or secret is not found"})
    else:
        repository_id=github_repo['id']
        public_key=get_github_repo_env_pub_key(org,repo,environment_name)
        encrypted_value=encrypt(public_key['key'],secret_value)
        url = "https://api.github.com/repositories/{}/environments/{}/secrets/{}".format(github_repo['id'],environment_name,secret_name)
        response = requests.put(url, json={'repository_id': repository_id, 'environment_name': environment_name,'secret_name': secret_name, 'encrypted_value':encrypted_value,'key_id': public_key['key_id'], 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
        if response.ok:
            return JSONResponse(status_code=200, content={"message": "Env secret has been Created"})

# Delete an environment secret
@router.delete("/repositories/environments/{environment_name}/secrets/{secret_name}")
def delete_github_repo_env_secrets(org: str, repo:str, environment_name:str,secret_name:str,accept:Optional[str]= 'application/vnd.github.v3+json'):
    github_repo=get_github_repo(org,repo)
    url = "https://api.github.com/repositories/{}/environments/{}/secrets/{}".format(github_repo['id'],environment_name,secret_name)
    response = requests.delete(url, headers={'Authorization': AUTH_TOKEN})
    if response.ok:
        return ({"message": "Repo Env secret has been deleted"})
    else:
        return JSONResponse(status_code=404, content={"message": "Repo or org or secret not found"})