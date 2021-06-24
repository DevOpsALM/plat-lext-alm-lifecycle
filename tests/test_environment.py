from fastapi.testclient import TestClient
from app.router.environment import router
from .test_data import TestData

client = TestClient(router)

# Test for create or update an repo environment
def test_create_update_github_repo_env():
    response = client.put("/repos/{}/{}/environments/{}".format(TestData['org'],TestData['repo'],TestData['environment_name']))
    assert response.status_code == 200
    assert response.json()['message'] == 'Env has been Created or updated'

# Test for get all environments from a repository
def test_get_github_repo_all_env():
    response = client.get("/repos/{}/{}/environments".format(TestData['org'],TestData['repo']))
    assert response.status_code == 200
    
# Test get an environments from a repository
def test_get_github_repo_env():
    response = client.get("/repos/{}/{}/environments/{}".format(TestData['org'],TestData['repo'],TestData['environment_name']))
    assert response.status_code == 200

# Test delete an repo environment   
def test_delete_github_repo_env():
    response = client.delete("/repos/{}/{}/environments/{}".format(TestData['org'],TestData['repo'],TestData['environment_name']))
    assert response.status_code == 200
    assert response.json()['message'] == 'Environment has been deleted'

# Test for create or update an repo environment
def test_recreate_update_github_repo_env():
    response = client.put("/repos/{}/{}/environments/{}".format(TestData['org'],TestData['repo'],TestData['environment_name']))
    assert response.status_code == 200
    assert response.json()['message'] == 'Env has been Created or updated'