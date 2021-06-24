from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import Optional
import base64
from dotenv import load_dotenv
from os import environ
import requests
from pydantic import BaseModel, validator
from authlib.integrations.requests_client import OAuth2Session
import time
from app.router.repo_secret import create_update_github_repo_secret
router = APIRouter()
load_dotenv()
AUTH_TOKEN="Bearer "+environ.get('GITHUB_PAT')

class Deploy_Environment(BaseModel):
    project_name: str
    geography: str
    environment: str
    app_type: str
    subscription: str
    client_id: str
    client_secret: str
    tenant_id:str

    @validator('project_name','geography','environment','app_type','subscription','client_id','client_secret','tenant_id')
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
    @validator('geography')
    @classmethod
    def geography_validation(cls, v):
        env=["eu","us","apac","au"]
        if v not in env:
           raise ValueError(f'{v} is not valid, the valid geography are ''[%s]' % ', '.join(map(str, env)))
        return v
class Destroy_Environment(BaseModel):
    project_name: str
    geography: str

    @validator('project_name','geography')
    @classmethod
    def environment_validation(cls, v):
        if(len(v) == 0):
            raise ValueError('param value should not be empty')
        elif v == "string":
            raise ValueError('%s is not valid value' % v)
        return v
def getStratosphereAccessToken():
    client_id = environ.get('ALM_CLIENT_ID')
    client_secret = environ.get('ALM_CLIENT_SECRET')
    token_endpoint = "https://login.live.external.byp.ai/realms/Stratosphere/protocol/openid-connect/token"
    session = OAuth2Session(client_id, client_secret)
    session.fetch_token(token_endpoint)
    return str(session.token["access_token"])

def removeSpecialChars(projectname,env,reponame):
    repo_name=''.join(e for e in reponame if e.isalnum())
    return (projectname+'-'+repo_name.lower()+'-'+env)

def validateContainerWebName(project_name,env,reponame):
    container_web_name=removeSpecialChars(project_name,env,reponame)
    if(len(container_web_name) <= 24):
        return True

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

@router.put("/repos/{org}/{repo}/containerweb")
def deploy_stratosphere_container_web_app(org: str, repo: str, env: Deploy_Environment, accept:Optional[str] = 'application/vnd.github.luke-cage-preview+json'):
    client_id1 = environ.get('ALM_CLIENT_ID')
    client_secret1 = environ.get('ALM_CLIENT_SECRET')
    print("---------------------------------------------------------------")
    print(client_id1)
    print(client_secret1)
    print("---------------------------------------------------------------")
    if(validateContainerWebName(env.project_name,env.environment,repo)):
        create_update_github_repo_secret(org,repo,"STRATO_AZURE_CLIENT_ID",env.client_id)
        create_update_github_repo_secret(org,repo,"STRATO_AZURE_CLIENT_SECRET",env.client_secret)
        create_update_github_repo_secret(org,repo,"STRATO_AZURE_SUBSCRIPTION",env.subscription)
        template_path = "docker_templates/"
        destination_path = ".github/docker/"
        file_name = "Dockerfile_" + env.app_type
        create_file(org,repo,template_path,file_name,destination_path)
        template_path = "action_templates/"
        destination_path = ".github/workflows/"
        file_name = "create_stratospher_container_web_app_workflow.yaml"
        create_file(org,repo,template_path,file_name,destination_path)
        time.sleep(3)
        url = "https://api.github.com/repos/{}/{}/dispatches".format(org,repo)
        response = requests.post(url, json={"event_type": "create_stratosphere_container_web", "client_payload": {**env.dict(),"strato":{"repo":repo,"stratospher_access_token":getStratosphereAccessToken(), "container_web_app_name":removeSpecialChars(env.project_name,env.environment,repo)}}}, headers={'Accept':accept, 'Authorization': AUTH_TOKEN})
        if response.ok:
            return JSONResponse(status_code=200, content={"Container Web Name": removeSpecialChars(env.project_name,env.environment,repo)})
        else:
            return(response.json())
    else:
         return ({"message": "The Combination of Project Name, Repository and Environment cannot exceed 24 characters excluding reposiotry special characters"})



@router.delete("/repos/{org}/{repo}/containerweb/{containerweb_name}")
def destroy_stratosphere_container_web_app(org: str, repo: str, containerweb_name: str, env: Destroy_Environment, accept:Optional[str] = 'application/vnd.github.luke-cage-preview+json'):
    template_path = "action_templates/"
    destination_path = ".github/workflows/"
    file_name = "delete_stratospher_container_web_app_workflow.yaml"
    create_file(org,repo,template_path,file_name,destination_path)
    url = "https://api.github.com/repos/{}/{}/dispatches".format(org,repo)
    response = requests.post(url, json={"event_type": "delete_stratosphere_container_web", "client_payload": {**env.dict(),"webapp_name":containerweb_name,"stratospher_access_token":getStratosphereAccessToken()}}, headers={'Accept':accept, 'Authorization': AUTH_TOKEN})
    return(response)

@router.get("/repos/{owner}/{repo}/containerweb")
def get_stratosphere_container_web_app(owner: str, repo:str, accept:Optional[str] = 'Accept: application/vnd.github.3.raw'):
    file_path=".github/contaierweb/contaierweb.json"
    url = "https://api.github.com/repos/{}/{}/contents/{}".format(owner,repo,file_path)
    response = requests.get(url, headers={'Accept': accept,'Authorization': AUTH_TOKEN})
    return(response.json())

