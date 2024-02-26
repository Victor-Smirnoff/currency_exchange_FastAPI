"""add name for unique constraint

Revision ID: 1ed27c661017
Revises: 1898d75792ec
Create Date: 2024-02-26 15:31:23.942812

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1ed27c661017"
down_revision: Union[str, None] = "1898d75792ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "exchangerates_base_currency_id_target_currency_id_key", "exchangerates", type_="unique"
    )
    op.create_unique_constraint(
        "unique_id", "exchangerates", ["base_currency_id", "target_currency_id"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("unique_id", "exchangerates", type_="unique")
    op.create_unique_constraint(
        "exchangerates_base_currency_id_target_currency_id_key",
        "exchangerates",
        ["base_currency_id", "target_currency_id"],
    )
    # ### end Alembic commands ###