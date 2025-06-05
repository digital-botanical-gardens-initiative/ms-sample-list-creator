from dataclasses import dataclass
from typing import List


@dataclass
class Instrument:
    name: str
    identifier: int

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Please select a valid instrument")
        if self.identifier < 0:
            raise ValueError("Instrument ID cannot be negative")


@dataclass
class Batch:
    name: str
    identifier: int

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Please select a valid batch")
        if self.identifier < 0:
            raise ValueError("Batch ID cannot be negative")


@dataclass
class Blank:
    blank_name: str
    blank_position: str
    blank_pre: int
    blank_post: int

    def __post_init__(self) -> None:
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
    path: str
    identifier: int

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Please select a method")
        if not self.path:
            raise ValueError("Please select a method")
        if self.identifier < 0:
            raise ValueError("Method ID cannot be negative")


@dataclass
class ProjectPath:
    methods: List[Method]
    standby: str
    data: str
    output: str

    def __post_init__(self) -> None:
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

    def __post_init__(self) -> None:
        if self.column < 1:
            raise ValueError("Please select a valid number of columns")
        if self.row < 1:
            raise ValueError("Please select a valid number of rows")


@dataclass
class MassSpectrometry:
    operator_initials: str
    injection_volume: float

    def __post_init__(self) -> None:
        if not self.operator_initials:
            raise ValueError("Please enter operator initials")
        if self.injection_volume < 0:
            raise ValueError("Please select a valid injection volume")


@dataclass
class DirectusCredentials:
    username: str
    password: str

    def __post_init__(self) -> None:
        if not self.username:
            raise ValueError("Please enter username")
        if not self.password:
            raise ValueError("Please enter password")


@dataclass
class SampleContainer:
    name: str
    identifier: int

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("No sample container name")
        if self.identifier < 0:
            raise ValueError("Sample container ID cannot be negative")


@dataclass
class SampleData:
    parent_sample_container: SampleContainer
    injection_volume: float
    injection_methods: List[Method]
    instrument: Instrument
    batch: Batch
    injection_volume_unit: int = 18

    def __post_init__(self) -> None:
        if not self.parent_sample_container:
            raise ValueError("No parent sample container provided")
        if self.injection_volume < 0:
            raise ValueError("Invalid injection volume")
        if self.injection_volume_unit != 18:
            raise ValueError("Invalid injection volume unit")
        if not self.injection_methods:
            raise ValueError("No injection method provided")
        if not self.instrument:
            raise ValueError("No instrument provided")
        if not self.batch:
            raise ValueError("No batch provided")


@dataclass
class SampleListData:
    sample_name: str
    path: str
    method_file: str
    rack_position: str
    injection_volume: float

    def __post_init__(self) -> None:
        if not self.sample_name:
            raise ValueError("No sample name")
        if not self.path:
            raise ValueError("No data path")
        if not self.method_file:
            raise ValueError("No method file")
        if not self.rack_position:
            raise ValueError("No rack position")
        if self.injection_volume < 0.0 or self.injection_volume == "":
            raise ValueError("No injection volume")
