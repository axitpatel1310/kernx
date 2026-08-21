import json
from pathlib import Path
from django.conf import settings
from .models import Architecture, ArchitectureType

def import_architectures():
    dataset_dir = Path(settings.BASE_DIR) / "architecture_ai/dataset"

    Architecture.objects.all().delete()
    ArchitectureType.objects.all().delete()
    print(dataset_dir)
    print(dataset_dir.exists())
    print(list(dataset_dir.glob("*.json")))
        
    for file in dataset_dir.glob("*.json"):

        type_obj, _ = ArchitectureType.objects.get_or_create(
            slug=file.stem,
            defaults={
                "name": file.stem.replace("_", " ").title()
            }
        )

        with open(file, "r", encoding="utf-8") as f:
            architectures = json.load(f)

        for architecture in architectures:
            Architecture.objects.create(
                type=type_obj,
                slug=architecture["slug"],
                title=architecture["project"]["name"],
                data=architecture,
            )

    print("Import complete.")