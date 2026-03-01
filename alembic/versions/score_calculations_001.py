"""Add score calculations table

Revision ID: score_calculations_001
Revises: 2a45f89bc123
Create Date: 2026-01-26

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'score_calculations_001'
down_revision = '2a45f89bc123'  # Set this to the latest migration ID
branch_labels = None
depends_on = None


def upgrade():
    # Create score_calculations table
    op.create_table(
        'score_calculations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('reading_correct', sa.Integer(), nullable=False),
        sa.Column('writing_correct', sa.Integer(), nullable=False),
        sa.Column('math_correct', sa.Integer(), nullable=False),
        sa.Column('reading_writing_score', sa.Integer(), nullable=False),
        sa.Column('math_score', sa.Integer(), nullable=False),
        sa.Column('total_score', sa.Integer(), nullable=False),
        sa.Column('percentile', sa.Integer(), nullable=True),
        sa.Column('calculation_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_score_calculations_id'), 'score_calculations', ['id'], unique=False)
    op.create_index(op.f('ix_score_calculations_user_id'), 'score_calculations', ['user_id'], unique=False)
    op.create_index(op.f('ix_score_calculations_calculation_date'), 'score_calculations', ['calculation_date'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_score_calculations_calculation_date'), table_name='score_calculations')
    op.drop_index(op.f('ix_score_calculations_user_id'), table_name='score_calculations')
    op.drop_index(op.f('ix_score_calculations_id'), table_name='score_calculations')
    op.drop_table('score_calculations')
