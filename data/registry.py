import json
from typing import Union
from pathlib import Path

from src.domain.dataset import Dataset, BaseType, Category, FileFormat

DATA_PATH     = Path("data/analysis")
REGISTRY_PATH = Path("data/registry.json")

def _infer_basetype(filename: str) -> BaseType:
    return BaseType.EXAMPLE if ".example." in filename else BaseType.ORIGINAL

def _load_registry() -> dict[str, list[dict[str, str]]]:
    with open(REGISTRY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def _available_category(registry: dict[str, dict[str, list[dict[str, str]]]]) -> list[Category]:
    return [Category(i) for i in list(registry["datasets"].keys())]

def get_datasets(base_category: Union[Category, list[Category]] = None, basetype: BaseType = None) -> list[Dataset]:
    registry: dict[str, dict[str, list[dict[str, str]]]] = _load_registry()
    datasets: list[Dataset] = list()
    category: Category
    iterable: list[Category]
    
    if type(base_category) is not list and type(base_category) is Category:
        iterable = [base_category]
    
    elif type(base_category) is list:
        iterable = base_category
    
    elif isinstance(base_category, type(None)):
        iterable = _available_category(registry=registry)
    
    else:
        raise TypeError(f"Non available type for base_category: {type(base_category)}")
        
    for i, files in iterable:
        if type(i) is not type(Category): category = Category(i)
        else: category = i

        for item in files:
            inferred_basetype: BaseType = _infer_basetype(item["file"])

            if basetype is not None and inferred_basetype != basetype:
                continue

            dataset: Dataset = Dataset(item["file"], category, inferred_basetype, FileFormat(item["format"]))
            datasets.append(dataset)

    return datasets

def resolve_path(dataset: Dataset) -> Path:
    path: Path = (DATA_PATH / dataset.category.value / dataset.filename)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return path