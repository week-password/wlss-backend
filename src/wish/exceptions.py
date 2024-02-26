from __future__ import annotations

from fastapi import status

from src.shared.exceptions import NotAllowedException, NotFoundException


class CannotCreateWishError(NotAllowedException):
    action = "Create wish."

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class CannotCreateWishBookingError(NotAllowedException):
    action = "Create wish booking."

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class CannotDeleteWishError(NotAllowedException):
    action = "Delete wish."

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class CannotGetWishBookingsError(NotAllowedException):
    action = "Get wish bookings."

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class CannotGetWishesError(NotAllowedException):
    action = "Get wishes."

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class CannotUpdateWishError(NotAllowedException):
    action = "Update wish."

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class WishNotFoundError(NotFoundException):
    resource = "Wish"

    description = "Requested resource not found."
    details = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND


class WishBookingNotFoundError(NotFoundException):
    resource = "Wish booking"

    description = "Requested resource not found."
    details = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND
