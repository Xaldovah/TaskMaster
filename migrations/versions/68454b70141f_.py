"""empty message

Revision ID: 68454b70141f
Revises: 7c30c308cf05
Create Date: 2023-12-07 12:27:56.092113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68454b70141f'
down_revision = '7c30c308cf05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=False),
    sa.Column('token_type', sa.String(length=50), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('token')
    # ### end Alembic commands ###