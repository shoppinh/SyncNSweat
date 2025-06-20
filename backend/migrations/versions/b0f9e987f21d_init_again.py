"""init again

Revision ID: b0f9e987f21d
Revises: 
Create Date: 2025-04-27 19:11:04.141740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b0f9e987f21d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exercises',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('body_part', sa.String(), nullable=True),
    sa.Column('target', sa.String(), nullable=True),
    sa.Column('secondary_muscles', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('equipment', sa.String(), nullable=True),
    sa.Column('gif_url', sa.String(), nullable=True),
    sa.Column('instructions', sa.ARRAY(sa.String()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercises_id'), 'exercises', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('fitness_goal', sa.Enum('STRENGTH', 'ENDURANCE', 'WEIGHT_LOSS', 'MUSCLE_GAIN', 'GENERAL_FITNESS', name='fitnessgoal'), nullable=True),
    sa.Column('fitness_level', sa.Enum('BEGINNER', 'INTERMEDIATE', 'ADVANCED', name='fitnesslevel'), nullable=True),
    sa.Column('available_days', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('workout_duration_minutes', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_profiles_id'), 'profiles', ['id'], unique=False)
    op.create_index(op.f('ix_profiles_name'), 'profiles', ['name'], unique=False)
    op.create_table('workouts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('focus', sa.String(), nullable=True),
    sa.Column('duration_minutes', sa.Integer(), nullable=True),
    sa.Column('playlist_id', sa.String(), nullable=True),
    sa.Column('playlist_name', sa.String(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workouts_date'), 'workouts', ['date'], unique=False)
    op.create_index(op.f('ix_workouts_id'), 'workouts', ['id'], unique=False)
    op.create_table('preferences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.Column('available_equipment', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('music_genres', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('music_tempo', sa.String(), nullable=True),
    sa.Column('target_muscle_groups', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('exercise_types', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('spotify_connected', sa.Boolean(), nullable=True),
    sa.Column('spotify_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('profile_id')
    )
    op.create_index(op.f('ix_preferences_id'), 'preferences', ['id'], unique=False)
    op.create_table('workout_exercises',
    sa.Column('workout_id', sa.Integer(), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=False),
    sa.Column('sets', sa.Integer(), nullable=True),
    sa.Column('reps', sa.String(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('rest_seconds', sa.Integer(), nullable=True),
    sa.Column('completed_sets', sa.Integer(), nullable=True),
    sa.Column('weights_used', sa.ARRAY(sa.String()), nullable=True),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['workout_id'], ['workouts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('workout_id', 'exercise_id')
    )
    op.create_index('idx_workout_exercise_order', 'workout_exercises', ['workout_id', 'order'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_workout_exercise_order', table_name='workout_exercises')
    op.drop_table('workout_exercises')
    op.drop_index(op.f('ix_preferences_id'), table_name='preferences')
    op.drop_table('preferences')
    op.drop_index(op.f('ix_workouts_id'), table_name='workouts')
    op.drop_index(op.f('ix_workouts_date'), table_name='workouts')
    op.drop_table('workouts')
    op.drop_index(op.f('ix_profiles_name'), table_name='profiles')
    op.drop_index(op.f('ix_profiles_id'), table_name='profiles')
    op.drop_table('profiles')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_exercises_id'), table_name='exercises')
    op.drop_table('exercises')
    # ### end Alembic commands ###
