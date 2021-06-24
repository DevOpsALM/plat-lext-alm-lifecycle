from fastapi.testclient import TestClient
from app.router.repo_secret import router
from .test_data import TestData

client = TestClient(router)

def test_get_github_repo_publickey():
    response = client.get("/repos/{}/{}/actions/secrets/public-key".format(TestData['org'],TestData['repo']))
    assert response.status_code == 200

def test_get_github_repo_notfound_publickey():
    response = client.get("/repos/{}/test/actions/secrets/public-key".format(TestData['org']))
    assert response.status_code == 404
    assert response.json()["message"] == "Github repository public key not found"

# create or update github repo secret
def test_create_update_github_repo_secret():
    response = client.put("/repos/{}/{}/actions/secrets/{}?value={}".format(TestData['org'],TestData['repo'],"ALMSECRT","ALMSECRT"))
    assert response.status_code == 200

# get github repo secret test
def test_github_repo_secrets():
    response = client.get("/repos/{}/{}/actions/secrets/{}".format(TestData['org'],TestData['repo'],"ALMSECRT"))
    assert response.status_code == 200

# delete github repo secret test
def test_delete_github_repo_secret():
    response = client.delete("/repos/{}/{}/actions/secrets/{}?value={}".format(TestData['org'],TestData['repo'],"ALMSECRT","ALMSECRT"))
    assert response.status_code == 200

# delete github repo secret test
def test_delete_github_repo_deletedsecret():
    response = client.delete("/repos/{}/{}/actions/secrets/{}?value={}".format(TestData['org'],TestData['repo'],"ALMSECRT","ALMSECRT"))
    assert response.status_code == 404
    assert response.json()["message"] == "Repo or org or secret not found"

# get github repo secret test
def test_github_repo_inexistingsecrets():
    response = client.get("/repos/{}/{}/actions/secrets/{}".format(TestData['org'],TestData['repo'],"ALMSECRT"))
    assert response.status_code == 404
    assert response.json()["message"] == "Repo or org or secret not found"

