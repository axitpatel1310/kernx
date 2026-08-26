from django.core.management.base import BaseCommand

from architecture_ai.models import Architecture

from architecture_ai.llm import (
    retrieve_similar_architectures,
)

from architecture_ai.services.architecture_intelligence import (
    analyze_architecture_set,
    build_intelligence_context,
    find_architecture_gaps,
    build_gap_context,
)


class Command(BaseCommand):

    help = "Test Kernx architecture gap analysis"

    def add_arguments(self, parser):

        parser.add_argument(
            "architecture_id",
            type=str,
        )

    def handle(self, *args, **options):

        architecture_id = options[
            "architecture_id"
        ]

        # ----------------------------------------------
        # Current Architecture
        # ----------------------------------------------

        architecture = Architecture.objects.get(
            id=architecture_id
        )

        current_data = architecture.data

        self.stdout.write(
            f"\nAnalyzing: {architecture.title}\n"
        )

        # ----------------------------------------------
        # Retrieve similar architectures
        # ----------------------------------------------

        documents = retrieve_similar_architectures(
            str(current_data),
            k=20,
            exclude_architecture_id=architecture.id,
        )

        self.stdout.write(
            f"Retrieved {len(documents)} similar architectures.\n"
        )

        # ----------------------------------------------
        # Intelligence
        # ----------------------------------------------

        intelligence = analyze_architecture_set(
            documents
        )

        # ----------------------------------------------
        # Gap analysis
        # ----------------------------------------------

        gaps = find_architecture_gaps(
            current_data,
            intelligence,
        )

        # ----------------------------------------------
        # Display
        # ----------------------------------------------

        self.stdout.write(
            "\nKERNX ARCHITECTURE INTELLIGENCE\n"
        )

        self.stdout.write(
            build_intelligence_context(
                intelligence
            )
        )

        self.stdout.write(
            "\n\n"
        )

        self.stdout.write(
            build_gap_context(
                gaps
            )
        )