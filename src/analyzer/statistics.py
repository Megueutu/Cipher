import time

from src.domain.statistics import ExecutionMeasure

def measure(func, *args, **kwargs) -> dict:
    start = time.perf_counter()

    try:
        result, datasets_list = func(*args, **kwargs)
        datasets = [dt.filename for dt in datasets_list]

        return result, ExecutionMeasure(
            success=True,
            elapsed=time.perf_counter() - start,
            function=func.__name__,
            accessed=datasets
        ).out()

    except Exception:
        return None, ExecutionMeasure(
            success=False,
            elapsed=time.perf_counter() - start,
            function=func.__name__,
            accessed=datasets
        ).out()