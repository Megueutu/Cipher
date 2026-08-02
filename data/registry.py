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

def get_datasets(base_category: Category = None, basetype: BaseType = None) -> list[Dataset]:
    registry, datasets = load_registry(), []

    for str_category, files in registry["datasets"].items():
        category = Category(str_category)

        if not category == base_category and base_category:
            continue

        for item in files:
            inferred_basetype = _infer_basetype(item["file"])

            if basetype is not None and inferred_basetype != basetype:
                continue

            dataset = Dataset(item["file"], category, inferred_basetype, FileFormat(item["format"]))
            datasets.append(dataset)

    return datasets

def resolve_path(dataset: Dataset) -> Path:
    path = (DATA_PATH / dataset.category.value / dataset.filename)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return path