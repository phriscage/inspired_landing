"""create users table

Revision ID: 2713aad37476
Revises: None
Create Date: 2013-09-24 06:51:16.987042

"""

# revision identifiers, used by Alembic.
revision = '2713aad37476'
down_revision = None

from alembic import op
from sqlalchemy import *
from sqlalchemy.dialects.mysql import INTEGER as Integer


def upgrade():
    op.create_table(
        'users',
        Column('user_id', Integer(unsigned=True), primary_key=True, nullable=False),
        Column('email_address', String(length=255), unique=True, index=True, nullable=False),
        Column('created_at', DateTime, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

def downgrade():
    op.drop_table('users')
