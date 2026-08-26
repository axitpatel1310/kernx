import os

from django.core.management.base import BaseCommand

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


class Command(BaseCommand):
    help = "Search Kernx architectures using semantic similarity"

    def add_arguments(self, parser):
        parser.add_argument(
            "query",
            type=str,
            help="Architecture requirement to search for",
        )

        parser.add_argument(
            "--results",
            type=int,
            default=5,
            help="Number of architectures to return",
        )

    def handle(self, *args, **options):

        query = options["query"]
        number_of_results = options["results"]

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSearching Kernx architectures for:\n"{query}"\n'
            )
        )

        # --------------------------------------------------
        # Ollama Embeddings
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
        # Semantic Search
        # --------------------------------------------------

        results = vectorstore.similarity_search_with_score(
            query,
            k=number_of_results,
        )

        if not results:
            self.stdout.write(
                self.style.WARNING(
                    "No matching architectures found."
                )
            )
            return

        # --------------------------------------------------
        # Display Results
        # --------------------------------------------------

        self.stdout.write(
            self.style.SUCCESS(
                f"\nTop {len(results)} matching architectures:\n"
            )
        )

        for index, (document, score) in enumerate(
            results,
            start=1,
        ):

            metadata = document.metadata

            self.stdout.write(
                f"\n{'=' * 60}"
            )

            self.stdout.write(
                f"\n#{index}"
            )

            self.stdout.write(
                f"\nTitle: {metadata.get('title', 'Unknown')}"
            )

            self.stdout.write(
                f"\nSlug: {metadata.get('slug', 'Unknown')}"
            )

            self.stdout.write(
                f"\nArchitecture ID: "
                f"{metadata.get('architecture_id', 'Unknown')}"
            )

            self.stdout.write(
                f"\nType ID: {metadata.get('type_id', 'Unknown')}"
            )

            self.stdout.write(
                f"\nDistance: {score}"
            )

            self.stdout.write(
                f"\n{'-' * 60}"
            )

            preview = document.page_content[:500]

            self.stdout.write(
                f"\n{preview}"
            )

        self.stdout.write(
            f"\n{'=' * 60}\n"
        )