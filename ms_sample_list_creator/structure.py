from dataclasses import dataclass
from typing import List


@dataclass
class Blank:
    blank_name: str
    blank_position: str
    blank_pre: int
    blank_post: int


@dataclass
class Batch:
    name: str
    identifier: int


@dataclass
class MassSpectrometry:
    rack_columns: int
    rack_rows: int
    instrument_id: str
    operator_initials: str
    injection_volume: int
    batch_key: int
    data_path: str
    output_path: str
    standby_file: str


@dataclass
class Methods:
    method_files: List[str]
    method_keys: List[int]


@dataclass
class DirectusCredentials:
    username: str
    password: str


@dataclass
class SampleData:
    name: str
    position: str
