from fastapi import APIRouter
from api.v1 import user, project, task, bug, role

api_router = APIRouter()
api_router.include_router(role.router)
api_router.include_router(user.router)

api_router.include_router(project.router)
api_router.include_router(task.router)
api_router.include_router(bug.router)



























# from fastapi import APIRouter
# from api.v1 import project, task, bug, user, role

# api_router = APIRouter()
# api_router.include_router(project.router)
# api_router.include_router(task.router)
# api_router.include_router(bug.router)
# api_router.include_router(user.router)
# api_router.include_router(role.router)
