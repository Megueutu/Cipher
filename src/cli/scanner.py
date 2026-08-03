import argparse
from argparse import ArgumentParser
from src.analyzer.matches import scan_matches
from src.domain.dataset import Category, Dataset
from src.domain.scanner import ScanType
from data.registry import resolve_path
from pathlib import Path

def scanner_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="scanner",
        description="Scanner for analyzing passwords."
    )

    parser.add_argument(
        "password",
        help="Password to be analyzed"
    )

    parser.add_argument(
        "--scan-type", "-S",
        type=ScanType,
        default=ScanType.COMPLETE,
        choices=list(ScanType),
        help="Type of scan to perform."
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-c", "--category",
        type=Category,
        default=None,
        choices=list(Category),
        help="Category of datasets to analyze."
    )

    group.add_argument(
        "-p", "--path",
        type=Path,
        help="Path to a custom dataset for analyszis"
    )

    return parser.parse_args()
