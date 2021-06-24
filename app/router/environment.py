from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from os import environ
import requests
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

router = APIRouter()

load_dotenv()
AUTH_TOKEN="Bearer "+environ.get('GITHUB_PAT')

# Get all environments for a repository
@router.get("/repos/{org}/{repo}/environments")
def get_github_repo_env(org: str, repo:str, accept:Optional[str]= 'application/vnd.github.v3+json'):
    url = "https://api.github.com/repos/{}/{}/environments".format(org,repo)
    response = requests.get(url, json={'org': org, 'repo': repo, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    return (response.json())

# Get an environments from a repository
@router.get("/repos/{org}/{repo}/environments/{environment_name}")
def get_github_repo_all_env(org: str, repo:str, environment_name:str, accept:Optional[str]= 'application/vnd.github.v3+json'):
    url = "https://api.github.com/repos/{}/{}/environments/{}".format(org,repo,environment_name)
    response = requests.get(url, json={'org': org, 'repo': repo, 'environment_name': environment_name, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    return (response.json())

# Create or update an repo environment
@router.put("/repos/{org}/{repo}/environments/{environment_name}")
def create_update_github_repo_env(org: str,repo: str, environment_name:str, accept:Optional[str]= 'application/vnd.github.v3+json'):
    url = "https://api.github.com/repos/{}/{}/environments/{}".format(org,repo,environment_name)
    response = requests.put(url, headers={'Authorization': AUTH_TOKEN})

    if response.ok:
        return ({"message": "Env has been Created or updated"})
    else:
        return JSONResponse(status_code=422, content={"message": "Validation error when the environment name or repo or org is not found"})

# Delete an repo environment
@router.delete("/repos/{org}/{repo}/environments/{environment_name}")
def delete_github_repo_env(org: str,repo: str, environment_name:str, accept:Optional[str]= 'application/vnd.github.v3+json'):
    url = "https://api.github.com/repos/{}/{}/environments/{}".format(org,repo,environment_name)
    response = requests.delete(url, headers={'Authorization': AUTH_TOKEN})

    if response.ok:
        return ({"message": "Environment has been deleted"})
    else:
        return JSONResponse(status_code=422, content={"message": "Validation error when the environment name or repo or org is not found"})