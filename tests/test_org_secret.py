from fastapi.testclient import TestClient
from app.router.org_secret import router
from .test_data import TestData

client = TestClient(router)

# Test for create or update an org secret
def test_create_update_github_org_secret():
    response = client.put("/orgs/{}/actions/secrets/{}?secret_value={}".format(TestData['org'],TestData['secret_name'],"encriptedvalue"))
    assert response.status_code == 200
    assert response.json()['message'] == 'Org secret has been Created'

# Get an organization public key
def test_get_github_org_publickey():
    response = client.get("orgs/{}/actions/secrets/public-key".format(TestData['org']))
    assert response.status_code == 200

# List organization secrets
def test_get_github_org_secrets():
    response = client.get("orgs/{}/actions/secrets".format(TestData['org']))
    assert response.status_code == 200

# Negative Test to List organization secrets
def test_get_github_invalidorg_secrets():
    response = client.get("orgs/{}/actions/secrets".format("invalidorg"))
    assert response.status_code == 404
    assert response.json()['message'] == 'org is not found'

# Delete an organization secret
def test_delete_github_org_secret():
    response = client.delete("/orgs/{}/actions/secrets/{}".format(TestData['org'],TestData['secret_name']))
    assert response.status_code == 200

# Negative Test for Delete an organization secret
def test_delete_github_org_invalidsecret():
    response = client.delete("/orgs/{}/actions/secrets/{}".format(TestData['org'],"invalidsecretname"))
    assert response.status_code == 404