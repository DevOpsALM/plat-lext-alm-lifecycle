from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from os import environ
import requests
from typing import Optional

router = APIRouter()

load_dotenv()
AUTH_TOKEN="Bearer "+environ.get('GITHUB_PAT')

# Get Github Org Repo
@router.get("/repos/{org}/{repo}", status_code=status.HTTP_200_OK)
def get_github_repo(org: str, repo:str, accept:Optional[str] = 'application/vnd.github.v3+json'):
    url = "https://api.github.com/repos/{}/{}".format(org,repo)
    print("-----------------------------------------------------------------------")
    print(AUTH_TOKEN)
    print("-----------------------------------------------------------------------")
    response = requests.get(url, json={'org': org, 'repo': repo, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    if response.status_code == 404:
        return JSONResponse(status_code=404, content={"message": "Github Org Repo not found"})
    else:
        return(response.json())

# create github repo
@router.post("/orgs/{org}/repos", status_code=status.HTTP_201_CREATED)
def create_github_repo(org: str,name: str, auto_init: Optional[bool] = True, accept:Optional[str] = 'application/vnd.github.v3+json'):
    url = "https://api.github.com/orgs/{}/repos".format(org)
    print("-----------------------------------------------------------------------")
    print(AUTH_TOKEN)
    print("-----------------------------------------------------------------------")
    response = requests.post(url, json={'name': name, 'auto_init': auto_init}, headers={'Authorization': AUTH_TOKEN})
    if response.status_code == 422:
        return JSONResponse(status_code=422, content={"message": "Github Org Repo already exist"})
    else:
        return(response.json())

# delete github repo
@router.delete("/repos/{org}/{repo_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_github_repo(org: str,repo_name: str, accept:Optional[str] = 'application/vnd.github.v3+json'):
    url = "https://api.github.com/repos/{}/{}".format(org,repo_name)
    response = requests.delete(url, headers={'Authorization': AUTH_TOKEN})
    if response.ok:
        return JSONResponse(status_code=200, content={"message": "Repo has been deleted"})
    else:
       return JSONResponse(status_code=404, content={"message": "Repo or org not found"})


#List organization repositories
@router.get("/orgs/{org}/repos", status_code=status.HTTP_200_OK)
def get_github_org_repos(org: str, accept:Optional[str] = 'application/vnd.github.v3+json'):
    url = "https://api.github.com/orgs/{}/repos".format(org)
    response = requests.get(url, json={'org': org, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    if response.status_code == 404:
        return JSONResponse(status_code=404, content={"message": "Github Org not found"})
    else:
        return(response.json())

# Update a repository
@router.patch("/repos/{owner}/{repo}", status_code=status.HTTP_200_OK)
def update_github_org_repo(owner: str,repo: str,name: str, auto_init: Optional[bool] = True, accept:Optional[str] = 'application/vnd.github.v3+json'):
    url = "https://api.github.com/repos/{}/{}".format(owner,repo)
    response = requests.patch(url, json={'name': name, 'auto_init': auto_init}, headers={'Authorization': AUTH_TOKEN})
    if response.status_code == 200:
        return(response.json())
    else:
       return JSONResponse(status_code=404, content={"message": "Repo or org not found"})

# Get repository contributors
@router.get("/repos/{owner}/{repo}/contributors", status_code=status.HTTP_200_OK)
def get_github_repo_contributors(owner: str, repo:str, accept:Optional[str] = 'application/vnd.github.v3+json'):
    url = "https://api.github.com/repos/{}/{}/contributors".format(owner,repo)
    response = requests.get(url, json={'owner': owner, 'repo': repo, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    if response.status_code == 404:
        return JSONResponse(status_code=404, content={"message": "Github Org Repo not found"})
    else:
        return(response.json())


# Get branches
@router.get("/repos/{owner}/{repo}/branches", status_code=status.HTTP_200_OK)
def get_github_repo_branches(owner: str, repo:str, accept:Optional[str] = 'application/vnd.github.v3+json'):
    url = "https://api.github.com/repos/{}/{}/branches".format(owner,repo)
    response = requests.get(url, json={'owner': owner, 'repo': repo, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    if response.status_code == 404:
        return JSONResponse(status_code=404, content={"message": "Github Org or Repo not found"})
    else:
        return(response.json())

# Get a branch
@router.get("/repos/{owner}/{repo}/branches/{branch}", status_code=status.HTTP_200_OK)
def get_github_repo_branch(owner: str, repo:str, branch:str, accept:Optional[str] = 'application/vnd.github.v3+json'):
    url = "https://api.github.com/repos/{}/{}/branches/{}".format(owner,repo,branch)
    response = requests.get(url, json={'owner': owner, 'repo': repo, 'branch':branch, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
    if response.status_code == 404:
        return JSONResponse(status_code=404, content={"message": "Github Org or Repo or Branch not found"})
    else:
        return(response.json())