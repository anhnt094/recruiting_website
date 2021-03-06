"""rename Jobs s to Job

Revision ID: 5e50871b435a
Revises: 423ce49dfa62
Create Date: 2018-07-02 02:07:56.424482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e50871b435a'
down_revision = '423ce49dfa62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('github_url', sa.String(length=200), nullable=True),
    sa.Column('github_issues_number', sa.Integer(), nullable=True),
    sa.Column('author', sa.String(length=100), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.Column('updated_time', sa.DateTime(), nullable=True),
    sa.Column('content', sa.String(length=10000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_created_time'), 'job', ['created_time'], unique=False)
    op.create_index(op.f('ix_job_updated_time'), 'job', ['updated_time'], unique=False)
    op.drop_index('ix_jobs_created_time', table_name='jobs')
    op.drop_index('ix_jobs_updated_time', table_name='jobs')
    op.drop_table('jobs')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jobs',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('github_url', sa.VARCHAR(length=200), nullable=True),
    sa.Column('github_issues_number', sa.INTEGER(), nullable=True),
    sa.Column('author', sa.VARCHAR(length=100), nullable=True),
    sa.Column('created_time', sa.DATETIME(), nullable=True),
    sa.Column('updated_time', sa.DATETIME(), nullable=True),
    sa.Column('content', sa.VARCHAR(length=10000), nullable=True),
    sa.Column('title', sa.VARCHAR(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_jobs_updated_time', 'jobs', ['updated_time'], unique=False)
    op.create_index('ix_jobs_created_time', 'jobs', ['created_time'], unique=False)
    op.drop_index(op.f('ix_job_updated_time'), table_name='job')
    op.drop_index(op.f('ix_job_created_time'), table_name='job')
    op.drop_table('job')
    # ### end Alembic commands ###
