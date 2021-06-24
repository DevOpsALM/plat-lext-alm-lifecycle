from fastapi.testclient import TestClient
from app.router.member import router
from .test_data import TestData

client = TestClient(router)

# create github org's team invite test
def test_create_org_invite():
    response = client.post("/orgs/{}/invitations?email={}".format(TestData['org'],TestData['email']))
    TestData['invitation_id'] = response.json()['id']
    assert response.status_code == 201

# list github org's team pending invites test
def test_list_pending_invites():
    response = client.get("/orgs/{}/invitations".format(TestData['org']))
    assert response.status_code == 200

# cancel github org's team invite test
def test_cancel_org_invite():
    response = client.delete("/orgs/{}/invitations/{}".format(TestData['org'], TestData['invitation_id']))
    assert response.status_code == 204