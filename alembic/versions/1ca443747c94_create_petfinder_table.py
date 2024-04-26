"""create petfinder table

Revision ID: 1ca443747c94
Revises: 
Create Date: 2024-04-26 10:03:54.172714

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ca443747c94'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table("animals",
                        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
                        sa.Column("name", sa.Text),
                        sa.Column("species", sa.Text),
                        sa.Column("breed", sa.Text),
                        sa.Column("color", sa.Text)
                    )

def downgrade() -> None:
    op.drop_table("animals")
