import argparse
from src.analyzer.matches import scan_matches
from src.domain.scanner import ScanType
from src.domain.dataset import Category

print(scan_matches("123Batata", Category.BLACKLIST, ScanType.COMPLETE))