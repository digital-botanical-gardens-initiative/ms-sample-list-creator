from dataclasses import dataclass
from typing import List

@dataclass
class Instrument:
    name: str
    identifier: int

@dataclass
class Batch:
    name: str
    identifier: int

@dataclass
class Blank:
    blank_name: str
    blank_position: str
    blank_pre: int
    blank_post: int

@dataclass
class Method:
    name: str
    identifier: int

@dataclass
class Path:
    methods: List[Method]
    standby: str
    data: str
    output: str

@dataclass
class Rack:
    column: int
    row: int

@dataclass
class MassSpectrometry:
    operator_initials: str
    injection_volume: int

@dataclass
class DirectusCredentials:
    username: str
    password: str

@dataclass
class SampleData:
    name: str
    position: str