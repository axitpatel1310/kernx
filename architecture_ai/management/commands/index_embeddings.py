import os

from django.core.management.base import BaseCommand

from architecture_ai.models import ArchitectureEmbedding

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
class Command(BaseCommand):
    help = "Generate embeddings for architectures and store them in Chroma"
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Starting architecture embedding process...")
        )
        embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url=os.getenv(
                "OLLAMA_HOST",
                "http://ollama:11434"
            ),
        )

        # --------------------------------------------------
        # Chroma
        # --------------------------------------------------

        vectorstore = Chroma(
            collection_name="kernx_architectures",
            embedding_function=embeddings,
            persist_directory="/app/chroma_db",
        )

        # --------------------------------------------------
        # Architectures
        # --------------------------------------------------

        architectures = ArchitectureEmbedding.objects.select_related(
            "architecture"
        ).all()

        total = architectures.count()

        self.stdout.write(
            f"Found {total} architecture records."
        )

        if total == 0:
            self.stdout.write(
                self.style.WARNING(
                    "No ArchitectureEmbedding records found."
                )
            )
            return

        # --------------------------------------------------
        # Index
        # --------------------------------------------------

        for index, item in enumerate(architectures, start=1):

            architecture = item.architecture

            vectorstore.add_texts(
                texts=[item.content],
                metadatas=[
                    {
                        "architecture_id": str(architecture.id),
                        "slug": architecture.slug,
                        "title": architecture.title,
                        "type_id": str(architecture.type_id),
                    }
                ],
                ids=[
                    str(architecture.id)
                ],
            )

            self.stdout.write(
                f"[{index}/{total}] {architecture.title}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully indexed {total} architectures."
            )
        )