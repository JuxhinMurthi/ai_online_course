from src.celery.celery_app import celery_app
from src.models.models import Course

@celery_app.task
def generate_all_course_summaries(courses: list[dict]):
    """ Generate all course summaries for given courses and update course status to 'Completed'. """

    # Lazy import to prevent circular import
    from src.adapters.database.postgres import PostgresDbService
    from src.adapters.ai.openai_integration import OpenAIService

    database = PostgresDbService()

    course_list = list()
    for course in courses:
        ai_service = OpenAIService()
        summary = ai_service.generate_summary(course_description=course["course_description"])
        if summary:
            course_list.append({"id": course["id"], "ai_summary": summary, "status": "Completed"})

    if course_list:
        database.bulk_update(model=Course, updates=course_list)



