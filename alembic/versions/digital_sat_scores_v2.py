"""
Digital SAT Score Calculations - Complete Restructure

Revision ID: digital_sat_scores_v2
Revises: previous migration
Create Date: 2026-01-26

Changes:
- Drop old score_calculations table (paper SAT structure)
- Create new score_calculations table (Digital SAT / Bluebook structure)
- Add module-based fields with adaptive difficulty
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite


# revision identifiers
revision = 'digital_sat_scores_v2'
down_revision = 'score_calculations_001'
branch_labels = None
depends_on = None


def upgrade():
    """
    Upgrade to Digital SAT (Bluebook) structure.
    """
    # Drop old table if it exists
    op.execute("DROP TABLE IF EXISTS score_calculations")

    # Create new Digital SAT score_calculations table
    op.create_table(
        'score_calculations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),

        # Reading & Writing Module scores
        sa.Column('rw_module1_correct', sa.Integer(), nullable=False, comment='R&W Module 1 correct (0-27)'),
        sa.Column('rw_module2_correct', sa.Integer(), nullable=False, comment='R&W Module 2 correct (0-27)'),
        sa.Column('rw_module2_difficulty', sa.String(10), nullable=False, comment='easy/medium/hard'),

        # Math Module scores
        sa.Column('math_module1_correct', sa.Integer(), nullable=False, comment='Math Module 1 correct (0-22)'),
        sa.Column('math_module2_correct', sa.Integer(), nullable=False, comment='Math Module 2 correct (0-22)'),
        sa.Column('math_module2_difficulty', sa.String(10), nullable=False, comment='easy/medium/hard'),

        # Calculated section scores
        sa.Column('reading_writing_score', sa.Integer(), nullable=False, comment='R&W score (200-800)'),
        sa.Column('math_score', sa.Integer(), nullable=False, comment='Math score (200-800)'),
        sa.Column('total_score', sa.Integer(), nullable=False, comment='Total score (400-1600)'),

        # Percentile and confidence
        sa.Column('percentile', sa.Integer(), comment='Estimated percentile (1-99)'),
        sa.Column('confidence', sa.String(10), comment='low/medium/high'),

        # Estimation metadata
        sa.Column('is_estimated', sa.Boolean(), nullable=False, default=True, comment='Always True'),

        # Metadata
        sa.Column('calculation_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),

        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )

    # Create indexes
    op.create_index(op.f('ix_score_calculations_id'), 'score_calculations', ['id'], unique=False)
    op.create_index(op.f('ix_score_calculations_user_id'), 'score_calculations', ['user_id'], unique=False)
    op.create_index(op.f('ix_score_calculations_total_score'), 'score_calculations', ['total_score'], unique=False)
    op.create_index(op.f('ix_score_calculations_calculation_date'), 'score_calculations', ['calculation_date'], unique=False)


def downgrade():
    """
    Downgrade from Digital SAT back to paper SAT structure.
    (Not recommended - this will lose data)
    """
    # Drop Digital SAT table
    op.drop_index(op.f('ix_score_calculations_calculation_date'), table_name='score_calculations')
    op.drop_index(op.f('ix_score_calculations_total_score'), table_name='score_calculations')
    op.drop_index(op.f('ix_score_calculations_user_id'), table_name='score_calculations')
    op.drop_index(op.f('ix_score_calculations_id'), table_name='score_calculations')
    op.drop_table('score_calculations')

    # Recreate old paper SAT structure
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
        sa.Column('percentile', sa.Integer()),
        sa.Column('calculation_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )

    op.create_index(op.f('ix_score_calculations_id'), 'score_calculations', ['id'], unique=False)
    op.create_index(op.f('ix_score_calculations_user_id'), 'score_calculations', ['user_id'], unique=False)
    op.create_index(op.f('ix_score_calculations_calculation_date'), 'score_calculations', ['calculation_date'], unique=False)
