from __future__ import annotations

from wlss.file.types import FileSize

from src.shared.columns import PositiveIntColumn


# pylint: disable-next=abstract-method,too-many-ancestors
class FileSizeColumn(PositiveIntColumn):
    type_ = FileSize
