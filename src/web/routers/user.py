from dependency_injector.wiring import inject, Provide
from fastapi import HTTPException, Depends, APIRouter

from src.containers import ApplicationContainer
from src.interfaces.use_case.use_case import UseCasePort
from src.web.schemas import UserCreate, User

router = APIRouter()



# # POST /users → Create a new user
@router.post(
    "/user",
    tags=["users"],
    response_model=User
)
@inject
async def create_user(
        user: UserCreate,
        create_user_use_case: UseCasePort = Depends(
            Provide[ApplicationContainer.user_package.use_cases.create_user_use_case]
        )
):
    user_object = create_user_use_case.execute(
        data=user
    )
    return user_object


# GET /users/{user_id} → Fetch user details
@router.get(
    "/user/{user_id}",
    tags=["users"],
    response_model=User
)
@inject
async def get_user(
        user_id: int,
        get_user_usecase:  UseCasePort = Depends(
            Provide[ApplicationContainer.user_package.use_cases.get_user_usecase]
        )
):
    user = get_user_usecase.execute(
        record_id=user_id
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user