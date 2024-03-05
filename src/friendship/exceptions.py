from __future__ import annotations

from fastapi import status

from src.shared.exceptions import NotAllowedException, NotFoundException


class CannotAcceptFriendshipRequest(NotAllowedException):
    action = "Accept friendship request."

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class CannotCancelFriendshipRequest(NotAllowedException):
    action = "Cancel friendship request."

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class CannotCreateFriendshipRequest(NotAllowedException):
    action = "Create friendship request."

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class CannotDeleteFriendship(NotAllowedException):
    action = "Delete friendship."

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class CannotRejectFriendshipRequest(NotAllowedException):
    action = "Reject friendship request."

    description = "Requested action not allowed."
    details = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class FriendshipRequestNotFoundError(NotFoundException):
    resource = "Friendship request"

    description = "Requested resource not found."
    details = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND
