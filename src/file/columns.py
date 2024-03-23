from __future__ import annotations

from wlss.file.types import FileName, FileSize

from src.shared.columns import PositiveIntColumn, StrColumn


# pylint: disable-next=abstract-method,too-many-ancestors
class FileNameColumn(StrColumn):
    type_ = FileName


# pylint: disable-next=abstract-method,too-many-ancestors
class FileSizeColumn(PositiveIntColumn):
    type_ = FileSize
