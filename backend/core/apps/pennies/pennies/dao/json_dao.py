import json
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel

from pennies.model.request import PenniesRequest


@dataclass
class JsonDao:

    data_dir: Path

    def write_base_model(self, base: BaseModel, filename: str):
        with open(str(Path(self.data_dir, filename)), "w", encoding="utf-8") as f:
            f.write(base.json(ensure_ascii=False, indent=4))

    def read_base_model(self, base: ClassVar[BaseModel], filename: str):
        with open(str(Path(self.data_dir, filename))) as f:
            return base.parse_obj(json.load(f))

    def read_request(self, filename: str) -> PenniesRequest:
        return self.read_base_model(PenniesRequest, filename)
