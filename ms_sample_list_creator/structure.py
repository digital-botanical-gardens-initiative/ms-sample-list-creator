from dataclasses import dataclass, field
from typing import List
import tkinter as tk

@dataclass
class DirectusCredentials:
    username: tk.StringVar = field(default_factory=lambda: tk.StringVar(None))
    password: tk.StringVar = field(default_factory=lambda: tk.StringVar(None))

@dataclass
class OperatorSettings:
    operator: tk.StringVar = field(default_factory=lambda: tk.StringVar(None))
    ms_id: tk.StringVar = field(default_factory=lambda: tk.StringVar(None))

@dataclass
class TkVariables:
    directus: DirectusCredentials = field(default_factory=DirectusCredentials)
    operator_settings: OperatorSettings = field(default_factory=OperatorSettings)
    col_rack_number: tk.IntVar = field(default_factory=tk.IntVar)
    row_rack_number: tk.IntVar = field(default_factory=tk.IntVar)
    pre_blk: tk.IntVar = field(default_factory=tk.IntVar)
    post_blk: tk.IntVar = field(default_factory=tk.IntVar)
    blk_name: tk.StringVar = field(default_factory=tk.StringVar)
    blk_pos: tk.StringVar = field(default_factory=tk.StringVar)
    inj_volume: tk.IntVar = field(default_factory=tk.IntVar)
    batch_key: tk.IntVar = field(default_factory=tk.IntVar)
    method_files: List[str] = field(default_factory=list)
    standby_file: tk.StringVar = field(default_factory=tk.StringVar)
    data_path: str = field(default_factory=str)
    file: str = ""

@dataclass
class DirectusSessionData:
    instrument_key: int = -1
    batch_key: int = -1
    access_token: str = ""
    method_keys: List[int] = field(default_factory=list)