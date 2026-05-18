"""Create initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2026-05-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade() -> None:
    """Create initial database schema"""
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(80), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    
    # Create chess_games table
    op.create_table(
        'chess_games',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('title', sa.String(120), nullable=False),
        sa.Column('opponent', sa.String(100), nullable=False),
        sa.Column('result', sa.Enum('win', 'loss', 'draw', name='gameresult'), nullable=False),
        sa.Column('opening', sa.String(120), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_chess_games_user_id'), 'chess_games', ['user_id'], unique=False)
    op.create_index(op.f('ix_chess_games_title'), 'chess_games', ['title'], unique=False)
    op.create_index(op.f('ix_chess_games_result'), 'chess_games', ['result'], unique=False)
    op.create_index(op.f('ix_chess_games_created_at'), 'chess_games', ['created_at'], unique=False)


def downgrade() -> None:
    """Drop initial schema"""
    
    op.drop_index(op.f('ix_chess_games_created_at'), table_name='chess_games')
    op.drop_index(op.f('ix_chess_games_result'), table_name='chess_games')
    op.drop_index(op.f('ix_chess_games_title'), table_name='chess_games')
    op.drop_index(op.f('ix_chess_games_user_id'), table_name='chess_games')
    op.drop_table('chess_games')
    
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
