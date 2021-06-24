from fastapi import APIRouter, status, HTTPException
from dotenv import load_dotenv
from os import environ
import requests

router = APIRouter()

load_dotenv()
AUTH_TOKEN="Bearer "+environ.get('GITHUB_PAT')

# create github org invitation
@router.post("/orgs/{org}/invitations", status_code=status.HTTP_201_CREATED)
def create_org_invite(org: str, email: str):
    url = "https://api.github.com/orgs/{}/invitations".format(org)
    response = requests.post(url, json={'email': email}, headers={'Authorization': AUTH_TOKEN})
    return(response.json())

# cancel github org invitation
@router.delete("/orgs/{org}/invitations/{invitation_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_org_invite(org: str, invitation_id: int):
    url = "https://api.github.com/orgs/{}/invitations/{}".format(org,invitation_id)
    response = requests.delete(url, headers={'Authorization': AUTH_TOKEN})
    if response.ok:
        return({"message": "Cancelled Invitation"})
    else:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

# list github org pending invitations
@router.get("/orgs/{org}/invitations", status_code=status.HTTP_200_OK)
def list_pending_invites(org: str):
    url = "https://api.github.com/orgs/{}/invitations".format(org)
    response = requests.get(url, headers={'Authorization': AUTH_TOKEN})
    return(response.json())