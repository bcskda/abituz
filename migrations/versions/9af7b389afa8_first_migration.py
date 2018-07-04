"""first migration

Revision ID: 9af7b389afa8
Revises: 
Create Date: 2018-07-04 13:24:53.032478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9af7b389afa8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('program',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=11), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_program_code'), 'program', ['code'], unique=False)
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_name'), 'student', ['name'], unique=False)
    op.create_table('university',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('faculty',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('university_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['university_id'], ['university.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('application',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('faculty_id', sa.Integer(), nullable=False),
    sa.Column('program_id', sa.Integer(), nullable=False),
    sa.Column('is_revoked', sa.Boolean(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('datasource', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['faculty_id'], ['faculty.id'], ),
    sa.ForeignKeyConstraint(['program_id'], ['program.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('student_id', 'faculty_id', 'program_id')
    )
    op.create_index(op.f('ix_application_datasource'), 'application', ['datasource'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_application_datasource'), table_name='application')
    op.drop_table('application')
    op.drop_table('faculty')
    op.drop_table('university')
    op.drop_index(op.f('ix_student_name'), table_name='student')
    op.drop_table('student')
    op.drop_index(op.f('ix_program_code'), table_name='program')
    op.drop_table('program')
    # ### end Alembic commands ###
