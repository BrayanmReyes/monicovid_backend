"""added nullable

Revision ID: c676ecd3a31a
Revises: 27e30040a574
Create Date: 2021-08-24 19:37:09.104908

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c676ecd3a31a'
down_revision = '27e30040a574'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('health_reports', 'oxygen_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('health_reports', 'temperature_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('health_reports', 'temperature_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('health_reports', 'oxygen_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
