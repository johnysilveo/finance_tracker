from dataclasses import dataclass


@dataclass
class Category:
    name: str
    description: str | None = None
    id: int | None = None
    is_deleted: bool = False
    created_at: str | None = None