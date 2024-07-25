from dataclasses import dataclass
from typing import Annotated

from annotated_types import MaxLen


@dataclass
class UserEntity:
    id: int
    full_name: Annotated[str, MaxLen(50)]
