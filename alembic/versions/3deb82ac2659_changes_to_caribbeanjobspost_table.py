"""Changes to caribbeanjobspost table

Revision ID: 3deb82ac2659
Revises: 
Create Date: 2022-03-10 16:54:37.789681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3deb82ac2659'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('caribbeanjobs_posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('caribbeanjobs_job_id', sa.Integer(), nullable=True),
    sa.Column('job_title', sa.String(), nullable=False),
    sa.Column('job_company', sa.String(), nullable=False),
    sa.Column('job_category', sa.String(), nullable=True),
    sa.Column('job_location', sa.String(), nullable=True),
    sa.Column('job_salary', sa.String(), nullable=True),
    sa.Column('job_min_education_requirement', sa.String(), nullable=True),
    sa.Column('full_job_description', sa.String(), nullable=True),
    sa.Column('job_listing_datetime', sa.DateTime(timezone=True), nullable=True),
    sa.Column('job_delisting_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('job_listing_is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('caribbeanjobs_job_id')
    )
    op.create_index(op.f('ix_caribbeanjobs_posts_id'), 'caribbeanjobs_posts', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_caribbeanjobs_posts_id'), table_name='caribbeanjobs_posts')
    op.drop_table('caribbeanjobs_posts')
    # ### end Alembic commands ###
