from fastapi.testclient import TestClient
from app.router.team import router
from .test_data import TestData

client = TestClient(router)

# list github org teams test
def test_list_org_teams():
    response = client.get("/orgs/{}/teams".format(TestData['org']))
    assert response.status_code == 200

# create github org team test
def test_create_org_team():
    response = client.post("/orgs/{}/teams".format(TestData['org']), json={'name': TestData['team'], 'maintainers': [], 'repo_names': [], 'permission': 'admin'})
    assert response.status_code == 201

# get github org's team test
def test_get_org_team():
    response = client.get("/orgs/{}/teams/{}".format(TestData['org'],TestData['team']))
    assert response.status_code == 200
    
# list github team repos test
def test_get_github_team_repos():
    response = client.get("/orgs/{}/teams/{}/repos".format(TestData['org'],TestData['team']))
    assert response.status_code == 200

# test to check inexisting github Org or Team
def test_get_github_inexistingteam_repos():
    response = client.get("/orgs/{}/teams/noteam/repos".format(TestData['org']))
    assert response.status_code == 404
    assert response.json()["message"] == "Github Org or Team not found"

   
# list github team repo projects
def test_get_github_team_projects():
    response = client.get("/orgs/{}/teams/{}/projects".format(TestData['org'],TestData['team']))
    assert response.status_code == 200

# test to check inexisting github Org or Team for projects
def test_get_github_inexistingteam_projects():
    response = client.get("/orgs/{}/teams/noteam/projects".format(TestData['org']))
    assert response.status_code == 404
    assert response.json()["message"] == "Github Org or Team not found"


# list github team members test
def test_get_github_team_members():
    response = client.get("/orgs/{}/teams/{}/members".format(TestData['org'],TestData['team']))
    assert response.status_code == 200

# test to check inexisting github Org or Team
def test_get_github_inexistingteam_members():
    response = client.get("/orgs/{}/teams/noteam/members".format(TestData['org']))
    assert response.status_code == 404
    assert response.json()["message"] == "Github Org or Team not found"

# update a team test
def test_update_github_team():
    response = client.patch("/orgs/{}/teams/{}?name={}".format(TestData['org'],TestData['team'],TestData['team']))
    assert response.status_code == 200

# update a team test
def test_update_github_invalid_team():
    response = client.patch("/orgs/{}/teams/{}?name={}".format(TestData['org'],"testteam",TestData['team']))
    assert response.status_code == 404
    assert response.json()["message"] == "Github Org or Team not found"

# delete github org team test
def test_delete_org_team():
    response = client.delete("/orgs/{}/teams/{}".format(TestData['org'],TestData['team']))
    assert response.status_code == 200
    assert response.json() == {"message": "Team has been deleted"}
    # delete non existing team
    response = client.delete("/orgs/{}/teams/{}".format(TestData['org'],TestData['team']))
    assert response.status_code == 404
    assert response.json() == {"message": "Team or org not found"}
