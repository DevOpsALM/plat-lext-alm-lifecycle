from fastapi.testclient import TestClient
from app.router.functionapp import router
from .test_data import TestData
from dotenv import load_dotenv
from os import environ

client = TestClient(router)

load_dotenv()

AZURE_CLIENT_ID=environ.get('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET=environ.get('AZURE_CLIENT_SECRET')
AZURE_TENANT_ID=environ.get('AZURE_TENANT_ID')
AZURE_RESOURCE_GROUP=environ.get('AZURE_RESOURCE_GROUP')
AZURE_SUBSCRIPTION=environ.get('AZURE_SUBSCRIPTION')

# delete functionapp test
def test_destroy_functionapp_app():
    response = client.delete("/repos/{}/{}/functionapps/{}?resource_group={}".format(TestData['webapporg'],TestData['webapprepo'],TestData['functionapp_name'],AZURE_RESOURCE_GROUP),json={'subscription':AZURE_SUBSCRIPTION, 'client_id': AZURE_CLIENT_ID, 'client_secret': AZURE_CLIENT_SECRET, 'tenant_id': AZURE_TENANT_ID})
    assert response.status_code == 200

# create functionapp test
def test_deploy_functionapp_app():
    response = client.put("/repos/{}/{}/functionapps".format(TestData['webapporg'],TestData['webapprepo']),json={"env":{'resource_group': AZURE_RESOURCE_GROUP, 'environment': TestData['environment_name'], 'app_type': TestData['app_type']},"cred":{'subscription':AZURE_SUBSCRIPTION, 'client_id': AZURE_CLIENT_ID, 'client_secret': AZURE_CLIENT_SECRET, 'tenant_id': AZURE_TENANT_ID}})
    assert response.status_code == 200
# get functionapp endpoint url test
def test_get_functionapp_app():
    response = client.get("/repos/{}/{}/functionapps".format(TestData['webapporg'],TestData['webapprepo']))
    assert response.status_code == 200
