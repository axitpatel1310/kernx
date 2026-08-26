from celery import shared_task
from django.utils import timezone

from architecture_ai.models import ArchitectureAnalysis
from architecture_ai.llm import analyze_architecture


@shared_task
def analyze_architecture_task(analysis_id):

    analysis = ArchitectureAnalysis.objects.get(
        id=analysis_id
    )

    try:

        analysis.status = "processing"
        analysis.save(
            update_fields=["status"]
        )

        result = analyze_architecture(
            analysis.architecture.data,
            architecture_id=analysis.architecture.id,
        )

        analysis.result = result
        analysis.status = "completed"
        analysis.completed_at = timezone.now()

        analysis.save(
            update_fields=[
                "result",
                "status",
                "completed_at",
            ]
        )

    except Exception as exc:

        analysis.status = "failed"
        analysis.error = str(exc)

        analysis.save(
            update_fields=[
                "status",
                "error",
            ]
        )

        raise