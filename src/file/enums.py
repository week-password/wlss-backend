from __future__ import annotations

from typing import TYPE_CHECKING

from varname import nameof

from src.shared.enum import Enum, types


if TYPE_CHECKING:
    from typing import Self


@types(str)
class Extension(Enum):
    GIF = "gif"
    JFIF = "jfif"
    JIF = "jif"
    JPE = "jpe"
    JPEG = "jpeg"
    JPG = "jpg"
    PNG = "png"
    WEBP = "webp"

    @property
    def mime_type(self: Self) -> MimeType:  # pragma: no cover
        """Get associated mime-type."""
        return _extension_mime_type[self]


class MimeType(Enum):
    IMAGE_GIF = "image/gif"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    IMAGE_WEBP = "image/webp"


_extension_mime_type = {
    Extension.GIF: MimeType.IMAGE_GIF,
    Extension.JFIF: MimeType.IMAGE_JPEG,
    Extension.JIF: MimeType.IMAGE_JPEG,
    Extension.JPE: MimeType.IMAGE_JPEG,
    Extension.JPEG: MimeType.IMAGE_JPEG,
    Extension.JPG: MimeType.IMAGE_JPEG,
    Extension.PNG: MimeType.IMAGE_PNG,
    Extension.WEBP: MimeType.IMAGE_WEBP,
}


assert set(Extension) == set(_extension_mime_type), (
    # pylint: disable-next=consider-using-f-string
    "Each `{Extension}` enum member should have according mime-type registered in `{_extension_mime_type}` dict."
    .format(Extension=nameof(Extension), _extension_mime_type=nameof(_extension_mime_type))
)
