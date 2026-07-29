import json
from pathlib import Path
from src.domain.dataset import Dataset, BaseType

DATA_PATH = Path("data/analysis")
REGISTRY_PATH = Path("data/registry.json")

def load_registry() -> dict:
    with open(REGISTRY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def get_datasets(basetype: BaseType) -> list[Dataset]:
    registry, datasets = load_registry(), []

    for category, files in registry["datasets"].items():
        for item in files:
            dataset = Dataset(item["file"], category, basetype, item["format"])
            datasets.append(dataset)

    return datasets

def resolve_path(dataset: Dataset) -> Path:
    path = (DATA_PATH / dataset.basetype.value / dataset.category.value / dataset.filename)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return path