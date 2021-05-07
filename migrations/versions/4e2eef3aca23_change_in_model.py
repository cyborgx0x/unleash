"""change in model

Revision ID: 4e2eef3aca23
Revises: 947dfa244559
Create Date: 2021-05-06 17:23:01.308802

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4e2eef3aca23'
down_revision = '947dfa244559'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_following',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_following_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_following_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author_following',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fiction_following',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['fiction.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('following')
    op.alter_column('bookmark', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('bookmark', 'chapter_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bookmark', 'chapter_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('bookmark', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.create_table('following',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('fiction_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('author_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('post_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('content', mysql.VARCHAR(length=300), nullable=True),
    sa.Column('time', mysql.DATETIME(), nullable=True),
    sa.Column('user_following_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], name='following_ibfk_1'),
    sa.ForeignKeyConstraint(['fiction_id'], ['fiction.id'], name='following_ibfk_2'),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name='following_ibfk_3'),
    sa.ForeignKeyConstraint(['user_following_id'], ['user.id'], name='following_ibfk_6'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='following_ibfk_5'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('fiction_following')
    op.drop_table('author_following')
    op.drop_table('user_following')
    # ### end Alembic commands ###
