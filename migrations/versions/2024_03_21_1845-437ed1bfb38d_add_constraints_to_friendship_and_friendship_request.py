"""add constraints to friendship and friendship request

Revision ID: 437ed1bfb38d
Revises: 69d6fbe5d8cd
Create Date: 2024-03-21 18:45:51.449602+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "437ed1bfb38d"
down_revision = "69d6fbe5d8cd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(
        "sender_id__receiver_id__unique_together",
        "friendship_request",
        ["sender_id", "receiver_id"],
    )
    op.create_check_constraint("sender_id__receiver_id__differ", "friendship_request", "sender_id != receiver_id")
    op.create_check_constraint("account_id__friend_id__differ", "friendship", "account_id != friend_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("sender_id__receiver_id__unique_together", "friendship_request", type_="unique")
    op.drop_constraint("sender_id__receiver_id__differ", "friendship_request", type_="check")
    op.drop_constraint("account_id__friend_id__differ", "friendship", type_="check")
    # ### end Alembic commands ###
