"""empty message

Revision ID: b171ba402b6a
Revises: 662e666daba9
Create Date: 2023-07-02 22:08:56.399670

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b171ba402b6a'
down_revision = '662e666daba9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('author', schema=None) as batch_op:
        batch_op.alter_column('about',
               existing_type=sa.TEXT(),
               type_=sa.JSON(),
               existing_nullable=True,
               postgresql_using='about::json')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('author', schema=None) as batch_op:
        batch_op.alter_column('about',
               existing_type=sa.JSON(),
               type_=sa.TEXT(),
               existing_nullable=True)

    # ### end Alembic commands ###
