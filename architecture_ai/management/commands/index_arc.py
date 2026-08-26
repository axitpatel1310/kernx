import json

from django.core.management.base import BaseCommand

from architecture_ai.models import Architecture, ArchitectureEmbedding


class Command(BaseCommand):
    help = "Prepare architectures for AI indexing"

    def handle(self, *args, **options):

        architectures = Architecture.objects.all()

        total = architectures.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Found {total} architectures."
            )
        )

        for index, architecture in enumerate(
            architectures,
            start=1
        ):

            data = architecture.data

            content = (
                f"Architecture: {architecture.title}\n"
                f"Slug: {architecture.slug}\n"
                f"Type: {architecture.type}\n\n"
                f"Architecture Data:\n"
                f"{json.dumps(data, indent=2, ensure_ascii=False)}"
            )

            ArchitectureEmbedding.objects.update_or_create(
                architecture=architecture,
                defaults={
                    "content": content
                }
            )

            self.stdout.write(
                f"[{index}/{total}] {architecture.title}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Architecture indexing completed."
            )
        )