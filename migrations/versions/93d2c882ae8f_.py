"""empty message

Revision ID: 93d2c882ae8f
Revises: 
Create Date: 2023-09-21 00:00:53.077111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93d2c882ae8f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('facebook', sa.String(length=50), nullable=True),
    sa.Column('first_name', sa.Unicode(length=256), nullable=True),
    sa.Column('last_name', sa.Unicode(length=256), nullable=True),
    sa.Column('user_name', sa.String(length=64), nullable=True),
    sa.Column('avatar', sa.String(length=200), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_mod', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('author',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=160), nullable=True),
    sa.Column('birth_year', sa.Integer(), nullable=True),
    sa.Column('author_page', sa.String(length=160), nullable=True),
    sa.Column('view', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('img', sa.String(length=240), nullable=True),
    sa.Column('fiction_count', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('about', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
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
    op.create_table('fiction',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Unicode(length=300), nullable=True),
    sa.Column('status', sa.Unicode(length=300), nullable=True),
    sa.Column('view', sa.Integer(), nullable=True),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('cover', sa.Text(), nullable=True),
    sa.Column('publish_year', sa.Integer(), nullable=True),
    sa.Column('page_count', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('tiki_link', sa.Text(), nullable=True),
    sa.Column('mediafire_link', sa.Text(), nullable=True),
    sa.Column('slug', sa.String(length=160), nullable=True),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.Column('short_desc', sa.String(length=160), nullable=True),
    sa.Column('tag', sa.Unicode(length=300), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chapter',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=160), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('view_count', sa.Integer(), nullable=True),
    sa.Column('fiction', sa.Integer(), nullable=True),
    sa.Column('chapter_order', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['fiction'], ['fiction.id'], ),
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
    op.create_table('like',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('fiction_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['fiction_id'], ['fiction.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'fiction_id')
    )
    op.create_table('media',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.Unicode(length=300), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('media_type', sa.Unicode(length=300), nullable=True),
    sa.Column('fiction_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['fiction_id'], ['fiction.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quote',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('quote', sa.Text(), nullable=True),
    sa.Column('fiction', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('img', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['fiction'], ['fiction.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fiction', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fiction'], ['fiction.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookmark',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('chapter_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['chapter_id'], ['chapter.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'chapter_id')
    )
    op.create_table('history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('chapter_id', sa.Integer(), nullable=True),
    sa.Column('fiction_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('quote_id', sa.Integer(), nullable=True),
    sa.Column('media_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('content', sa.String(length=300), nullable=True),
    sa.Column('type', sa.String(length=30), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['chapter_id'], ['chapter.id'], ),
    sa.ForeignKeyConstraint(['fiction_id'], ['fiction.id'], ),
    sa.ForeignKeyConstraint(['media_id'], ['media.id'], ),
    sa.ForeignKeyConstraint(['quote_id'], ['quote.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('history')
    op.drop_table('bookmark')
    op.drop_table('task')
    op.drop_table('quote')
    op.drop_table('media')
    op.drop_table('like')
    op.drop_table('fiction_following')
    op.drop_table('chapter')
    op.drop_table('fiction')
    op.drop_table('author_following')
    op.drop_table('user_following')
    op.drop_table('author')
    op.drop_table('user')
    # ### end Alembic commands ###
