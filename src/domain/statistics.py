from dataclasses import dataclass

from src.domain.dataset import Dataset

@dataclass
class ExecutionMeasure():
    success:  bool
    elapsed:  float
    function: str
    accessed: list[Dataset]
    
    def out(self):
        return {
            "success"  : self.success,
            "elapsed"  : self.elapsed,
            "function" : self.function,
            "accessed" : self.accessed,
        }