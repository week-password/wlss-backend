"""add file table and update create foreign key for avatar_id

Revision ID: c2530d2a11e4
Revises: 55f1606e7086
Create Date: 2023-11-24 13:15:17.940691+00:00

"""
from alembic import op
import sqlalchemy as sa

import src


# revision identifiers, used by Alembic.
revision = "c2530d2a11e4"
down_revision = "55f1606e7086"
branch_labels = None
depends_on = None


extension_enum = src.shared.database.DbEnum("gif", "jfif", "jif", "jpe", "jpeg", "jpg", "png", "webp", name="extension")
mime_type_enum = src.shared.database.DbEnum("image/gif", "image/jpeg", "image/png", "image/webp", name="mimetype")


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "file",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("extension", extension_enum, nullable=False),
        sa.Column("mime_type", mime_type_enum, nullable=False),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_foreign_key("profile_avatar_id_fkey", "profile", "file", ["avatar_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("profile_avatar_id_fkey", "profile", type_="foreignkey")
    op.drop_table("file")
    extension_enum.drop(op.get_bind())
    mime_type_enum.drop(op.get_bind())
    # ### end Alembic commands ###
