"""empty message

Revision ID: 4c280b3ed5bc
Revises: 
Create Date: 2021-03-19 19:44:56.870067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c280b3ed5bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('api_key', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_api_key'), 'user', ['api_key'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_api_key'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###