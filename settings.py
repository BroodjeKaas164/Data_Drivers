from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    clear_cache: bool = False
    clear_deep: bool = False
    micro_data_dir: Path = Path(__file__).parent / 'Data' / 'Microdata'
    macro_data_dir: Path = Path(__file__).parent / 'Data' / 'Macrodata'
    master_data_dir: Path = Path(__file__).parent / 'Data' / 'Masterdata'
    root_dir: Path = Path(__file__).parent

settings = Settings()