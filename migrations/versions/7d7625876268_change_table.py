"""change table

Revision ID: 7d7625876268
Revises: b5321e580048
Create Date: 2021-05-05 22:07:35.619365

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7d7625876268'
down_revision = 'b5321e580048'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fiction', 'quote_count')
    op.drop_column('fiction', 'chapter_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fiction', sa.Column('chapter_count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('fiction', sa.Column('quote_count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
