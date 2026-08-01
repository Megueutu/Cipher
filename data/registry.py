import json
from pathlib import Path
from src.domain.dataset import Dataset, BaseType, Category, FileFormat

DATA_PATH = Path("data/analysis")
REGISTRY_PATH = Path("data/registry.json")

def _infer_basetype(filename: str) -> BaseType:
    return BaseType.EXAMPLE if ".example." in filename else BaseType.ORIGINAL

def load_registry() -> dict:
    with open(REGISTRY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def get_datasets(basetype: BaseType) -> list[Dataset]:
    registry, datasets = load_registry(), []

    for str_category, files in registry["datasets"].items():
        category = Category(str_category)
        for item in files:
            inferred_basetype = _infer_basetype(item["file"])

            if basetype is not None and inferred_basetype != basetype:
                continue

            dataset = Dataset(item["file"], category, inferred_basetype, FileFormat(item["format"]))
            datasets.append(dataset)

    return datasets

def resolve_path(dataset: Dataset) -> Path:
    path = (DATA_PATH / dataset.basetype.value / dataset.category.value / dataset.filename)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return path