"""add missing created_at updated_at

Revision ID: 5b979f00b2de
Revises: 938709fd0268
Create Date: 2024-02-26 18:38:53.975387+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5b979f00b2de"
down_revision = "938709fd0268"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("friendship", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.add_column("friendship_request", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.add_column("password_hash", sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.add_column("session", sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.add_column("session", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("session", "updated_at")
    op.drop_column("session", "created_at")
    op.drop_column("password_hash", "created_at")
    op.drop_column("friendship_request", "updated_at")
    op.drop_column("friendship", "updated_at")
    # ### end Alembic commands ###
