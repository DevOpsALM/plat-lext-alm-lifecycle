from fastapi.testclient import TestClient
from app.router.stratosphere_webapp import router
from .test_data import TestData
from dotenv import load_dotenv
from os import environ

client = TestClient(router)

STRATO_CLIENT_ID=environ.get('STRATO_CLIENT_ID')
STRATO_CLIENT_SECRET=environ.get('STRATO_CLIENT_SECRET')
STRATO_TENANT_ID=environ.get('STRATO_TENANT_ID')
AZURE_SUBSCRIPTION=environ.get('AZURE_SUBSCRIPTION')

# create container webapp test
def test_deploy_stratosphere_container_web_app():
    response = client.put("/repos/{}/{}/containerweb".format(TestData['webapporg'],TestData['webapprepo']),json={'project_name': TestData['project_name'],'geography': TestData['geography'], 'environment': TestData['environment_name'], 'app_type': TestData['app_type'],'subscription': AZURE_SUBSCRIPTION, 'client_id': STRATO_CLIENT_ID, 'client_secret': STRATO_CLIENT_SECRET, 'tenant_id': STRATO_TENANT_ID})
    assert response.status_code == 200
# get container webapp endpoint url test
def test_get_stratosphere_container_web_app():
    response = client.get("/repos/{}/{}/containerweb".format(TestData['webapporg'],TestData['webapprepo']))
    print(response.json())
    assert response.status_code == 200
# delete container webapp test
def test_destroy_stratosphere_container_web_app():
    response = client.delete("/repos/{}/{}/containerweb/{}".format(TestData['webapporg'],TestData['webapprepo'],TestData['containerweb_name']),json={'project_name': TestData['project_name'], 'geography': TestData['geography']})
    assert response.status_code == 200
