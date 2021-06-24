from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from os import environ
import requests

router = APIRouter()

load_dotenv()
AUTH_TOKEN="Bearer "+environ.get('GITHUB_PAT')

class Team(BaseModel):
    name: str
    maintainers: Optional [List[str]] = []
    repo_names: Optional [List[str]] = []
    permission: str

# list org teams
@router.get("/orgs/{org}/teams", status_code=status.HTTP_200_OK)
def list_org_teams(org: str, accept:Optional[str] = 'application/vnd.github.v3+json'):
    url = "https://api.github.com/orgs/{}/teams".format(org)
    response = requests.get(url, headers={'Authorization': AUTH_TOKEN})
    return(response.json())

# create team
@router.post("/orgs/{org}/teams", status_code=status.HTTP_201_CREATED)
def create_org_team(org: str, team: Team, accept:Optional[str] = 'application/vnd.github.v3+json'):
    url = "https://api.github.com/orgs/{}/teams".format(org)
    response = requests.post(url, json={**team.dict()}, headers={'Authorization': AUTH_TOKEN})
    return(response.json())

# update team repo permissions
@router.put("/orgs/{org}/teams/{team_slug}/repos/{repo}", status_code=status.HTTP_201_CREATED)
def update_team_permission(org: str, team_slug: str, repo: str, permission: str, accept:Optional[str] = 'application/vnd.github.v3+json'):
    url = "https://api.github.com/orgs/{}/teams/{}/repos/{}/{}".format(org,team_slug,org,repo)
    response = requests.put(url, json={"permission": permission}, headers={'Authorization': AUTH_TOKEN})
    return(response)

# get org's team
@router.get("/orgs/{org}/teams/{team_slug}", status_code=status.HTTP_200_OK)
def get_org_team(org: str, team_slug: str, accept:Optional[str] = 'application/vnd.github.v3+json'):
    url = "https://api.github.com/orgs/{}/teams/{}".format(org,team_slug)
    response = requests.get(url, headers={'Authorization': AUTH_TOKEN})
    return(response.json())

# delete team
@router.delete("/orgs/{org}/teams/{team_slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_org_team(org: str, team_slug: str, accept:Optional[str] = 'application/vnd.github.v3+json'):
    url = "https://api.github.com/orgs/{}/teams/{}".format(org,team_slug)
    response = requests.delete(url, headers={'Authorization': AUTH_TOKEN})
    if response.ok:
        return JSONResponse(status_code=200, content={"message": "Team has been deleted"})
    else:
        return JSONResponse(status_code=404, content={"message": "Team or org not found"})

# list team repos
@router.get("/orgs/{org}/teams/{team_slug}/repos", status_code=status.HTTP_200_OK)
def get_github_team_repos(org: str,team_slug: str, accept:Optional[str] = 'application/vnd.github.v3+json'):
    team_slug=get_org_team(org,team_slug)
    if 'message' in team_slug.keys():
        return JSONResponse(status_code=404, content={"message": "Github Org or Team not found"})
    else:
        team_name = team_slug['name']
        url = "https://api.github.com/orgs/{}/teams/{}/repos".format(org,team_name)
        response = requests.get(url, json={'org': org, 'team_name': team_name, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
        return(response.json())

# list team members
@router.get("/orgs/{org}/teams/{team_slug}/members", status_code=status.HTTP_200_OK)
def get_github_team_members(org: str,team_slug: str, accept:Optional[str] = 'application/vnd.github.v3+json'):
    team_slug=get_org_team(org,team_slug)
    if 'message' in team_slug.keys():
        return JSONResponse(status_code=404, content={"message": "Github Org or Team not found"})
    else:
        team_name = team_slug['name']
        url = "https://api.github.com/orgs/{}/teams/{}/members".format(org,team_name)
        response = requests.get(url, json={'org': org, 'team_name': team_name, 'accept': accept}, headers={'Authorization': AUTH_TOKEN})
        return(response.json())

# update a team
@router.patch("/orgs/{org}/teams/{team_slug}", status_code=status.HTTP_200_OK)
def update_github_team(org: str,team_slug: str,name: str, auto_init: Optional[bool] = True, accept:Optional[str] = 'application/vnd.github.v3+json'):
    team_slug=get_org_team(org,team_slug)
    if 'message' in team_slug.keys():
        return JSONResponse(status_code=404, content={"message": "Github Org or Team not found"})
    else:
        team_name = team_slug['name']
        url = "https://api.github.com/orgs/{}/teams/{}".format(org,team_name)
        response = requests.patch(url, json={'name': name, 'auto_init': auto_init}, headers={'Authorization': AUTH_TOKEN})
        return(response.json())

# list team projects
@router.get("/orgs/{org}/teams/{team_slug}/projects", status_code=status.HTTP_200_OK)
def get_github_team_projects(org: str,team_slug: str, accept:Optional[str] = 'application/vnd.github.inertia-preview+json'):
    team_slug=get_org_team(org,team_slug)
    if 'message' in team_slug.keys():
        return JSONResponse(status_code=404, content={"message": "Github Org or Team not found"})
    else:
        team_name = team_slug['name']
        url = "https://api.github.com/orgs/{}/teams/{}/projects".format(org,team_name)
        response = requests.get(url, json={'org': org, 'team_name': team_name}, headers={'Accept': accept,'Authorization': AUTH_TOKEN})
        return(response.json())