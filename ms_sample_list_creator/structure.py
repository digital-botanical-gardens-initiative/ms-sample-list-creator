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

    def __post_init__(self):
        if not self.blank_name:
            raise ValueError("Please enter blank name")
        if not self.blank_position:
            raise ValueError("Please enter blank position")
        if self.blank_pre < 0:
            raise ValueError("Please select a valid number of pre injection blanks")
        if self.blank_post < 0:
            raise ValueError("Please select a valid number of post injection blanks")


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
    def __post_init__(self):
        if not self.methods:
            raise ValueError("Please select at least one method")
        if not self.standby:
            raise ValueError("Please enter standby path")
        if not self.data:
            raise ValueError("Please enter data path")
        if not self.output:
            raise ValueError("Please enter output path")


@dataclass
class Rack:
    column: int
    row: int
    def __post_init__(self):
        if self.column < 1:
            raise ValueError("Please select a valid number of columns")
        if self.row < 1:
            raise ValueError("Please select a valid number of rows")


@dataclass
class MassSpectrometry:
    operator_initials: str
    injection_volume: int
    def __post_init__(self):
        if not self.operator_initials:
            raise ValueError("Please enter operator initials")
        if self.injection_volume < 1:
            raise ValueError("Please select a valid injection volume")


@dataclass
class DirectusCredentials:
    username: str
    password: str
    def __post_init__(self):
        if not self.username:
            raise ValueError("Please enter username")
        if not self.password:
            raise ValueError("Please enter password")

@dataclass
class SampleData:
    name: str
    position: str
