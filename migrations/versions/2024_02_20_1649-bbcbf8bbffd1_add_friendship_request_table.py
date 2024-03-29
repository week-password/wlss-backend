"""add friendship_request table

Revision ID: bbcbf8bbffd1
Revises: 8b9892ad80c5
Create Date: 2024-02-20 16:49:24.169913+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bbcbf8bbffd1"
down_revision = "8b9892ad80c5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "friendship_request",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("receiver_id", sa.Integer(), nullable=False),
        sa.Column("sender_id", sa.Integer(), nullable=False),
        sa.Column(
            "status", sa.Enum("ACCEPTED", "PENDING", "REJECTED", name="friendship_request_status_enum"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["receiver_id"],
            ["account.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sender_id"],
            ["account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("friendship_request")
    sa.Enum(name="friendship_request_status_enum").drop(op.get_bind(), checkfirst=False)
    # ### end Alembic commands ###
