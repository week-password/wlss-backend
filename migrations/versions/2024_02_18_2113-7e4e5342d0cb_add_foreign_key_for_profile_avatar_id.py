"""add foreign key for profile avatar_id

Revision ID: 7e4e5342d0cb
Revises: 1b645cd5f92c
Create Date: 2024-02-18 21:13:18.143434+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7e4e5342d0cb"
down_revision = "1b645cd5f92c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key("profile__file__foreign_key", "profile", "file", ["avatar_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("profile__file__foreign_key", "profile", type_="foreignkey")
    # ### end Alembic commands ###
