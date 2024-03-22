"""add created_at to profile

Revision ID: 37f4deae3e29
Revises: 437ed1bfb38d
Create Date: 2024-03-21 19:34:03.645758+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "37f4deae3e29"
down_revision = "437ed1bfb38d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("profile", sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("profile", "created_at")
    # ### end Alembic commands ###
