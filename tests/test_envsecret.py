from fastapi.testclient import TestClient
from app.router.env_secret import router
from .test_data import TestData

client = TestClient(router)

# Test for create or update an repo environment
def test_create_update_github_repo_env_secrets():
    response = client.put("/repositories/environments/{}/secrets/{}?org={}&repo={}&secret_value={}".format(TestData['environment_name'],TestData['secret_name'],TestData['org'],TestData['repo'],TestData['secret_value'])) 
    assert response.status_code == 200
    assert response.json()['message'] == 'Env secret has been Created'

# Test for list environment secrets
def test_get_github_repo_env_secrets():
    response = client.get("/repositories/{}/environments/{}/secrets?org={}&repo={}".format(TestData['repo'],TestData['environment_name'],TestData['org'],TestData['repo']))
    assert response.status_code == 200

# Negative Test for list environment secrets
def test_get_github_repo_invalidenv_secrets():
    response = client.get("/repositories/{}/environments/{}/secrets?org={}&repo={}".format(TestData['repo'],"invalidenv",TestData['org'],TestData['repo']))
    assert response.status_code == 404
    assert response.json()['message'] == 'Repo or org or secret not found'

# Test for list environment Public Key
def test_get_github_repo_env_pub_key():
    response = client.get("/repositories/{}/environments/{}/secrets/public-key?org={}&repo={}".format(TestData['repo'],TestData['environment_name'],TestData['org'],TestData['repo']))
    assert response.status_code == 200

# Test for delte environment secrets
def test_delete_github_repo_env_secrets():
    response = client.delete("/repositories/{}/environments/{}/secrets/{}?org={}&repo={}".format(TestData['repo'],TestData['environment_name'],TestData['secret_name'],TestData['org'],TestData['repo']))
    assert response.status_code == 200

# Negative Test for delte environment secrets
def test_delete_github_repo_env_invalidsecrets():
    response = client.delete("/repositories/{}/environments/{}/secrets/{}?org={}&repo={}".format(TestData['repo'],TestData['environment_name'],"invalidsecret",TestData['org'],TestData['repo']))
    assert response.status_code == 404
    assert response.json()["message"] == "Repo or org or secret not found"
