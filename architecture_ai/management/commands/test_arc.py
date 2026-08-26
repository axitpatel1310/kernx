import os

from django.core.management.base import BaseCommand

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from architecture_ai.services.architecture_intelligence import (
    analyze_architecture_set,
    build_intelligence_context,
)


class Command(BaseCommand):

    help = "Test Kernx architecture intelligence"

    def add_arguments(self, parser):

        parser.add_argument(
            "query",
            type=str,
        )

        parser.add_argument(
            "--results",
            type=int,
            default=20,
        )

    def handle(self, *args, **options):

        query = options["query"]

        results_count = options["results"]

        # --------------------------------------------------
        # Embeddings
        # --------------------------------------------------

        embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url=os.getenv(
                "OLLAMA_HOST",
                "http://ollama:11434",
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
        # Retrieve architectures
        # --------------------------------------------------

        documents = vectorstore.similarity_search(
            query,
            k=1,
        )

        self.stdout.write("\n")
        self.stdout.write(
            self.style.WARNING(
                "RAW RETRIEVED DOCUMENT:"
            )
        )

        self.stdout.write(
            documents[0].page_content
        )

        # --------------------------------------------------
        # Analyze
        # --------------------------------------------------

        intelligence = analyze_architecture_set(
            documents
        )

        # --------------------------------------------------
        # Build context
        # --------------------------------------------------

        context = build_intelligence_context(
            intelligence
        )

        self.stdout.write("\n")
        self.stdout.write(
            self.style.SUCCESS(
                "KERNX ARCHITECTURE INTELLIGENCE"
            )
        )

        self.stdout.write("\n" + context)