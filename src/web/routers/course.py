from dependency_injector.wiring import Provide, inject
from fastapi import HTTPException

from fastapi import APIRouter, Depends

from src.containers import ApplicationContainer
from src.interfaces.use_case.use_case import UseCasePort
from src.web.schemas import CourseCreate, Course

router = APIRouter()

#
@router.post("/course", tags=["courses"], response_model=Course)
@inject
async def create_course(
        course: CourseCreate,
        create_course_use_case: UseCasePort = Depends(
            Provide[ApplicationContainer.course_package.use_cases.create_course_use_case]
        ),
):
    course_object = create_course_use_case.execute(course)

    return course_object

@router.get(
    "/course/{course_id}",
    tags=["courses"],
    response_model=Course
)
@inject
async def get_user(
        course_id: int,
        get_course_use_case:  UseCasePort = Depends(
            Provide[ApplicationContainer.course_package.use_cases.get_course_use_case]
        )
):
    course = get_course_use_case.execute(
        record_id=course_id
    )
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course