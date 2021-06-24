from fastapi.testclient import TestClient
from app.router.repository import router
from .test_data import TestData

client = TestClient(router)

# create github repo test
def test_create_github_repo():
    response = client.post("orgs/{}/repos?name={}".format(TestData['org'],TestData['repotest']))
    assert response.status_code == 201

# check existing github repo test
def test_checkcreated_github_repo():
    response = client.post("orgs/{}/repos?name={}".format(TestData['org'],TestData['repotest']))
    assert response.status_code == 422
    assert response.json()["message"] == "Github Org Repo already exist"

# get github repo test
def test_get_github_repo():
    response = client.get("/repos/{}/{}".format(TestData['org'],TestData['repotest']))
    assert response.status_code == 200
    assert response.json()["name"] == TestData['repotest']

# test to check inexisting github repo
def test_get_inexistgithub_repo():
    response = client.get("/repos/{}/norepo".format(TestData['org']))
    assert response.status_code == 404
    assert response.json()["message"] == "Github Org Repo not found"

# test to list github organization repositories
def test_get_github_org_repos():
    response = client.get("/orgs/{}/repos".format(TestData['org']))
    assert response.status_code == 200

# negative test to list github organization repositories
def test_get_github_inexistingorg_repos():
    response = client.get("/orgs/{}/repos".format("invalidorg"))
    assert response.status_code == 404
    assert response.json()["message"] == "Github Org not found"

# test to list github repository branches
def test_get_github_repo_branches():
    response = client.get("/repos/{}/{}/branches".format(TestData['org'],TestData['repotest']))
    assert response.status_code == 200

# negative test to list github repository branches
def test_get_github_inexistingrepo_branches():
    response = client.get("/repos/{}/{}/branches".format(TestData['org'],"invalidorg"))
    assert response.status_code == 404
    assert response.json()["message"] == "Github Org or Repo not found"

# test to list github repository branch
def testget_github_repo_branch():
    response = client.get("/repos/{}/{}/branches/{}".format(TestData['org'],TestData['repotest'],TestData['branch']))
    assert response.status_code == 200

# negative test to list github repository branch
def test_get_github_inexistingrepo_branch():
    response = client.get("/repos/{}/{}/branches/{}".format(TestData['org'],TestData['repotest'],"invalidbranch"))
    assert response.status_code == 404
    assert response.json()["message"] == "Github Org or Repo or Branch not found"

# test to list github organization contributors
def test_get_github_repo_contributors():
    response = client.get("/repos/{}/{}/contributors".format(TestData['org'],TestData['repo']))
    assert response.status_code == 200

# test to list github contributors
def test_get_github_inexistingrepo_contributors():
    response = client.get("/repos/{}/{}/contributors".format(TestData['org'],"invalidrepo"))
    assert response.status_code == 404
    assert response.json()["message"] == "Github Org Repo not found"

def test_update_github_org_repo():
    response = client.patch("/repos/{}/{}?name={}".format(TestData['org'],TestData['repotest'],"uprepo"))
    assert response.status_code == 200
def test_revert_update_github_org_repo():
    response = client.patch("/repos/{}/{}?name={}".format(TestData['org'],"uprepo",TestData['repotest']))
    assert response.status_code == 200

# delete github repo test
def test_delete_github_repo():
    response = client.delete("/repos/{}/{}".format(TestData['org'],TestData['repotest']))
    assert response.status_code == 200
    assert response.json()["message"] == "Repo has been deleted"

# test to check deleted github repo
def test_checkdeleted_github_repo():
    response = client.delete("/repos/{}/{}".format(TestData['org'],TestData['repotest']))
    assert response.status_code == 404
    assert response.json()["message"] == "Repo or org not found"
