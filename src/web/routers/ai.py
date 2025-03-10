from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.containers import ApplicationContainer
from src.interfaces.use_case.use_case import UseCasePort

router = APIRouter()

@router.post("/generate_summary/{course_id}", tags=["ai"])
@inject
def generate_summary(
        course_id: int,
        generate_course_summary_use_case: UseCasePort = Depends(
            Provide[ApplicationContainer.ai_package.use_cases.generate_course_summary_use_case]
        )
):
    summary = generate_course_summary_use_case.execute(record_id=course_id)
    return summary


@router.post("/generate_all_summaries", tags=["ai"])
@inject
def generate_all_summaries(
        all_courses: bool,
        generate_course_all_summary_use_case: UseCasePort = Depends(
            Provide[ApplicationContainer.ai_package.use_cases.generate_course_all_summary_use_case]
        )
):
    summary = generate_course_all_summary_use_case.execute(all_courses=all_courses)
    return summary