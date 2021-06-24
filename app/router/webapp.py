from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import Optional
import base64
from dotenv import load_dotenv
from os import environ
import requests
from pydantic import BaseModel, validator
from app.router.functionapp import removeSpecialChars
import time
from app.router.repo_secret import create_update_github_repo_secret

router = APIRouter()

load_dotenv()
AUTH_TOKEN="Bearer "+environ.get('GITHUB_PAT')

class Environment(BaseModel):
    resource_group: str
    environment: str
    app_type: str

    @validator('resource_group','environment','app_type')
    @classmethod
    def environment_validation(cls, v):
        if(len(v) == 0):
            raise ValueError('param value should not be empty')
        elif v == "string":
            raise ValueError('%s is not valid value' % v)
        return v
    @validator('environment')
    @classmethod
    def environment_type_validation(cls, v):
        env=["dev","preprod","prod","qa","demo","poc"]
        if v not in env:
           raise ValueError(f'{v} is not valid, the valid environments are ''[%s]' % ', '.join(map(str, env)))
        return v
class Credentials(BaseModel):
    subscription: str
    client_id: str
    client_secret: str
    tenant_id:str
    @validator('subscription','client_id','client_secret','tenant_id')
    @classmethod
    def credentials_validation(cls, v):
        if(len(v) == 0):
            raise ValueError('param value should not be empty')
        elif v == "string":
            raise ValueError('%s is not valid value' % v)
        return v

def get_content(template_path,file_name):
    workflow_content = open(template_path + file_name, "r").read()
    message_bytes = workflow_content.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

def create_file(org,repo,template_path,file_name,destination_path):
    path = destination_path + file_name
    url = "https://api.github.com/repos/{}/{}/contents/{}".format(org,repo,path)
    base64_message = get_content(template_path,file_name)
    commit_message = "file creation"
    blob_sha = requests.get(url)
    if 'sha' in blob_sha.json().keys():
        response = requests.put(url, json={'message': commit_message, 'content': base64_message, 'sha': blob_sha.json()['sha'] }, headers={'Authorization': AUTH_TOKEN})
    else:
        response = requests.put(url, json={'message': commit_message, 'content': base64_message }, headers={'Authorization': AUTH_TOKEN})
    return(response.json())

@router.put("/repos/{org}/{repo}/webapps")
def deploy_web_app(org: str, repo: str, env: Environment, cred: Credentials, accept:Optional[str] = 'application/vnd.github.luke-cage-preview+json'):
    create_update_github_repo_secret(org,repo,"AZURE_CLIENT_ID",cred.client_id)
    create_update_github_repo_secret(org,repo,"AZURE_CLIENT_SECRET",cred.client_secret)
    create_update_github_repo_secret(org,repo,"AZURE_SUBSCRIPTION",cred.subscription)
    create_update_github_repo_secret(org,repo,"AZURE_RESOURCE_GROUP",env.resource_group)
    template_path = "docker_templates/"
    destination_path = ".github/docker/"
    file_name = "Dockerfile_" + env.app_type
    create_file(org,repo,template_path,file_name,destination_path)
    template_path = "action_templates/"
    destination_path = ".github/workflows/"
    file_name = "create_web_app_workflow.yaml"
    create_file(org,repo,template_path,file_name,destination_path)
    time.sleep(3)
    url = "https://api.github.com/repos/{}/{}/dispatches".format(org,repo)
    response = requests.post(url, json={"event_type": "create_web_app", "client_payload": {**env.dict(),**cred.dict(),"repo":removeSpecialChars(repo)}}, headers={'Accept':accept, 'Authorization': AUTH_TOKEN})
    if response.ok:
        return JSONResponse(status_code=200, content={"webapp name": "alm-app-"+env.app_type+"-"+removeSpecialChars(repo)+"-"+env.environment})
    else:
        return(response.json())

@router.delete("/repos/{org}/{repo}/webapps/{webapp_name}")
def destroy_web_app(org: str, repo: str, webapp_name: str, resource_group: str, cred: Credentials, accept:Optional[str] = 'application/vnd.github.luke-cage-preview+json'):
    create_update_github_repo_secret(org,repo,"AZURE_CLIENT_ID",cred.client_id)
    create_update_github_repo_secret(org,repo,"AZURE_CLIENT_SECRET",cred.client_secret)
    create_update_github_repo_secret(org,repo,"AZURE_SUBSCRIPTION",cred.subscription)
    create_update_github_repo_secret(org,repo,"AZURE_RESOURCE_GROUP",resource_group)
    template_path = "action_templates/"
    destination_path = ".github/workflows/"
    file_name = "delete_web_app_workflow.yaml"
    create_file(org,repo,template_path,file_name,destination_path)
    url = "https://api.github.com/repos/{}/{}/dispatches".format(org,repo)
    response = requests.post(url, json={"event_type": "delete_web_app", "client_payload": {**cred.dict(),"webapp_name":webapp_name,"resource_group":resource_group}}, headers={'Accept':accept, 'Authorization': AUTH_TOKEN})
    return(response)

@router.get("/repos/{owner}/{repo}/webapps")
def get_web_app(owner: str, repo:str, accept:Optional[str] = 'Accept: application/vnd.github.3.raw'):
    file_path=".github/webapps/webapps.json"
    url = "https://api.github.com/repos/{}/{}/contents/{}".format(owner,repo,file_path)
    response = requests.get(url, headers={'Accept': accept,'Authorization': AUTH_TOKEN})
    return(response.json())