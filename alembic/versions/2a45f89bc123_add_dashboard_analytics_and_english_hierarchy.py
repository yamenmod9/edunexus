"""add_dashboard_analytics_and_english_hierarchy

Revision ID: 2a45f89bc123
Revises: 1b01e70d8001
Create Date: 2026-01-25 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2a45f89bc123'
down_revision = '1b01e70d8001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Get connection to check existing columns
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # Add new columns to users table (check if they exist first)
    users_columns = [c['name'] for c in inspector.get_columns('users')]
    if 'full_name' not in users_columns:
        op.add_column('users', sa.Column('full_name', sa.String(length=200), nullable=True))
    if 'sat_exam_date' not in users_columns:
        op.add_column('users', sa.Column('sat_exam_date', sa.Date(), nullable=True))
    if 'target_score' not in users_columns:
        op.add_column('users', sa.Column('target_score', sa.Integer(), nullable=True))

    # Create index if it doesn't exist
    existing_indexes = [idx['name'] for idx in inspector.get_indexes('users')]
    if 'ix_users_sat_exam_date' not in existing_indexes:
        op.create_index(op.f('ix_users_sat_exam_date'), 'users', ['sat_exam_date'], unique=False)

    # Add new columns to questions table (check if they exist first)
    questions_columns = [c['name'] for c in inspector.get_columns('questions')]
    if 'category' not in questions_columns:
        op.add_column('questions', sa.Column('category', sa.String(length=100), nullable=True))
    if 'subcategory' not in questions_columns:
        op.add_column('questions', sa.Column('subcategory', sa.String(length=100), nullable=True))
    if 'is_bluebook' not in questions_columns:
        op.add_column('questions', sa.Column('is_bluebook', sa.Boolean(), nullable=False, server_default='0'))
    if 'passage_text' not in questions_columns:
        op.add_column('questions', sa.Column('passage_text', sa.Text(), nullable=True))
    if 'source_attribution' not in questions_columns:
        op.add_column('questions', sa.Column('source_attribution', sa.String(length=200), nullable=True))

    # SQLite doesn't support ALTER COLUMN, so we skip making topic nullable
    # New questions will use category/subcategory instead
    # Existing questions can keep their topic field as NOT NULL

    # Create new indexes for questions (check if they exist first)
    questions_indexes = [idx['name'] for idx in inspector.get_indexes('questions')]
    if 'ix_questions_category' not in questions_indexes:
        op.create_index(op.f('ix_questions_category'), 'questions', ['category'], unique=False)
    if 'ix_questions_subcategory' not in questions_indexes:
        op.create_index(op.f('ix_questions_subcategory'), 'questions', ['subcategory'], unique=False)
    if 'ix_questions_is_bluebook' not in questions_indexes:
        op.create_index(op.f('ix_questions_is_bluebook'), 'questions', ['is_bluebook'], unique=False)
    if 'idx_section_category' not in questions_indexes:
        op.create_index('idx_section_category', 'questions', ['section', 'category'], unique=False)
    if 'idx_section_subcategory' not in questions_indexes:
        op.create_index('idx_section_subcategory', 'questions', ['section', 'subcategory'], unique=False)
    if 'idx_category_subcategory' not in questions_indexes:
        op.create_index('idx_category_subcategory', 'questions', ['category', 'subcategory'], unique=False)
    if 'idx_section_bluebook' not in questions_indexes:
        op.create_index('idx_section_bluebook', 'questions', ['section', 'is_bluebook'], unique=False)

    # SQLite doesn't support ALTER TYPE, section enum is defined in code, not database
    # The SectionEnum in models already includes 'english'

    # Create bookmarks table (check if exists)
    existing_tables = inspector.get_table_names()
    if 'bookmarks' not in existing_tables:
        op.create_table('bookmarks',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('question_id', sa.Integer(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('user_id', 'question_id', name='unique_user_question_bookmark')
        )
        op.create_index(op.f('ix_bookmarks_id'), 'bookmarks', ['id'], unique=False)
        op.create_index(op.f('ix_bookmarks_user_id'), 'bookmarks', ['user_id'], unique=False)
        op.create_index(op.f('ix_bookmarks_question_id'), 'bookmarks', ['question_id'], unique=False)

    # Create daily_statistics table
    if 'daily_statistics' not in existing_tables:
        op.create_table('daily_statistics',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('date', sa.Date(), nullable=False),
            sa.Column('questions_attempted', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('questions_correct', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('questions_incorrect', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('math_attempted', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('math_correct', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('english_attempted', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('english_correct', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('total_time_spent', sa.Float(), nullable=False, server_default='0'),
            sa.Column('tests_completed', sa.Integer(), nullable=False, server_default='0'),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_daily_statistics_id'), 'daily_statistics', ['id'], unique=False)
        op.create_index(op.f('ix_daily_statistics_user_id'), 'daily_statistics', ['user_id'], unique=False)
        op.create_index(op.f('ix_daily_statistics_date'), 'daily_statistics', ['date'], unique=False)
        op.create_index('idx_user_date', 'daily_statistics', ['user_id', 'date'], unique=True)

    # Create mistake_logs table
    if 'mistake_logs' not in existing_tables:
        op.create_table('mistake_logs',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('question_id', sa.Integer(), nullable=False),
            sa.Column('user_answer', sa.String(length=1), nullable=False),
            sa.Column('attempted_at', sa.DateTime(), nullable=False),
            sa.Column('source_type', sa.String(length=20), nullable=False),
            sa.Column('source_id', sa.Integer(), nullable=False),
            sa.Column('reviewed', sa.Boolean(), nullable=False, server_default='0'),
            sa.Column('reviewed_at', sa.DateTime(), nullable=True),
            sa.Column('time_spent', sa.Float(), nullable=True),
            sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_mistake_logs_id'), 'mistake_logs', ['id'], unique=False)
        op.create_index(op.f('ix_mistake_logs_user_id'), 'mistake_logs', ['user_id'], unique=False)
        op.create_index(op.f('ix_mistake_logs_question_id'), 'mistake_logs', ['question_id'], unique=False)
        op.create_index(op.f('ix_mistake_logs_attempted_at'), 'mistake_logs', ['attempted_at'], unique=False)
        op.create_index('idx_user_attempted_at', 'mistake_logs', ['user_id', 'attempted_at'], unique=False)
        op.create_index('idx_user_reviewed', 'mistake_logs', ['user_id', 'reviewed'], unique=False)

    # Create score_predictions table
    if 'score_predictions' not in existing_tables:
        op.create_table('score_predictions',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('predicted_total_score', sa.Integer(), nullable=False),
            sa.Column('predicted_math_score', sa.Integer(), nullable=False),
            sa.Column('predicted_english_score', sa.Integer(), nullable=False),
            sa.Column('confidence_level', sa.Float(), nullable=False),
            sa.Column('sample_size', sa.Integer(), nullable=False),
            sa.Column('easy_accuracy', sa.Float(), nullable=True),
            sa.Column('medium_accuracy', sa.Float(), nullable=True),
            sa.Column('hard_accuracy', sa.Float(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('calculation_method', sa.String(length=50), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_score_predictions_id'), 'score_predictions', ['id'], unique=False)
        op.create_index(op.f('ix_score_predictions_user_id'), 'score_predictions', ['user_id'], unique=False)
        op.create_index(op.f('ix_score_predictions_created_at'), 'score_predictions', ['created_at'], unique=False)


def downgrade() -> None:
    # Drop score_predictions table
    op.drop_index(op.f('ix_score_predictions_created_at'), table_name='score_predictions')
    op.drop_index(op.f('ix_score_predictions_user_id'), table_name='score_predictions')
    op.drop_index(op.f('ix_score_predictions_id'), table_name='score_predictions')
    op.drop_table('score_predictions')

    # Drop mistake_logs table
    op.drop_index('idx_user_reviewed', table_name='mistake_logs')
    op.drop_index('idx_user_attempted_at', table_name='mistake_logs')
    op.drop_index(op.f('ix_mistake_logs_attempted_at'), table_name='mistake_logs')
    op.drop_index(op.f('ix_mistake_logs_question_id'), table_name='mistake_logs')
    op.drop_index(op.f('ix_mistake_logs_user_id'), table_name='mistake_logs')
    op.drop_index(op.f('ix_mistake_logs_id'), table_name='mistake_logs')
    op.drop_table('mistake_logs')

    # Drop daily_statistics table
    op.drop_index('idx_user_date', table_name='daily_statistics')
    op.drop_index(op.f('ix_daily_statistics_date'), table_name='daily_statistics')
    op.drop_index(op.f('ix_daily_statistics_user_id'), table_name='daily_statistics')
    op.drop_index(op.f('ix_daily_statistics_id'), table_name='daily_statistics')
    op.drop_table('daily_statistics')

    # Drop bookmarks table
    op.drop_index(op.f('ix_bookmarks_question_id'), table_name='bookmarks')
    op.drop_index(op.f('ix_bookmarks_user_id'), table_name='bookmarks')
    op.drop_index(op.f('ix_bookmarks_id'), table_name='bookmarks')
    op.drop_table('bookmarks')

    # Remove new indexes from questions
    op.drop_index('idx_section_bluebook', table_name='questions')
    op.drop_index('idx_category_subcategory', table_name='questions')
    op.drop_index('idx_section_subcategory', table_name='questions')
    op.drop_index('idx_section_category', table_name='questions')
    op.drop_index(op.f('ix_questions_is_bluebook'), table_name='questions')
    op.drop_index(op.f('ix_questions_subcategory'), table_name='questions')
    op.drop_index(op.f('ix_questions_category'), table_name='questions')

    # Remove new columns from questions
    op.drop_column('questions', 'source_attribution')
    op.drop_column('questions', 'passage_text')
    op.drop_column('questions', 'is_bluebook')
    op.drop_column('questions', 'subcategory')
    op.drop_column('questions', 'category')
    # SQLite: Cannot revert topic to NOT NULL, existing data remains compatible

    # Remove new columns from users
    op.drop_index(op.f('ix_users_sat_exam_date'), table_name='users')
    op.drop_column('users', 'target_score')
    op.drop_column('users', 'sat_exam_date')
    op.drop_column('users', 'full_name')
