from fastapi import FastAPI 

from .router import repository, webapp, functionapp, stratosphere_webapp, member, team, org_secret, env_secret, repo_secret, environment

tags_metadata = [
    {
        "name": "Github Repos",
        "description": "[Operations with GitHub repos]",
    },
    {
        "name": "Azure Web Apps",
        "description": "[Manage Azure Web Apps]",
    },
    {
        "name": "Azure Function Apps",
        "description": "[Manage Azure Function Apps]",
    },
    {
        "name": "Azure Stratospher Container Web Apps",
        "description": "[Manage Azure Strato Web Apps]",
    },
    {
        "name": "Github Org Members",
        "description": "[Manage GitHub org members]",
    },
    {
        "name": "Github Org Teams",
        "description": "[Manage GitHub org members]",
    },

    {
        "name": "Github repo secrets",
        "description": "[Manage GitHub Repository Secret]",
    },
    {
        "name": "Github org secrets",
        "description": "[Manage GitHub Organization Secret]",
    },
    {
        "name": "Github environment",
        "description": "[Manage GitHub Repository Environment]",
    },

    {
        "name": "Github environment secret",
        "description": "[Manage GitHub Repository Environment Secret]",
    }

]

app = FastAPI(
    openapi_tags=tags_metadata,
    docs_url = "/api/v1/docs",
    openapi_url = "/api/v1/openapi.json",
    redoc_url = "/api/v1/redocs",
    title = "ALM API",
    version = "1.0",
    description = "Provides API for Application Lifecycle Management",
)
app.include_router(
    repository.router,
    tags=["Github Repos"],
)
app.include_router(
    webapp.router,
    tags=["Azure Web Apps"],
)
app.include_router(
    functionapp.router,
    tags=["Azure Function Apps"],
)
app.include_router(
    stratosphere_webapp.router,
    tags=["Azure Stratospher Container Web Apps"],
)
app.include_router(
    member.router,
    tags=["Github Org Members"],
)
app.include_router(
    team.router,
    tags=["Github Org Teams"],
)

app.include_router(
    repo_secret.router,
    tags=["Github repo secrets"],
)
app.include_router(
    environment.router,
    tags=["Github environment"],
)

app.include_router(
    env_secret.router,
    tags=["Github environment secret"],
)

app.include_router(
    org_secret.router,
    tags=["Github org secrets"],
)



