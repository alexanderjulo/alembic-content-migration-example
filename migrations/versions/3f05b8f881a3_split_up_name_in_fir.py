"""split up name in first- and lastname.

Revision ID: 3f05b8f881a3
Revises: 3821916c0277
Create Date: 2013-05-06 15:24:23.815282

"""

# revision identifiers, used by Alembic.
revision = '3f05b8f881a3'
down_revision = '3821916c0277'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# we build a quick link for the current connection of alembic
connection = op.get_bind()

# now we build a helper table, that is kind of a hybrid. it has both,
# the name column and the first- and lastname attribute because it will
# be used in the migration, when both are available and necessary.
# in this case we define all attributes, because we also need the id
# to identify rows, if you had more columns you would only have to specify
# the relevant ones
contacthelper = sa.Table(
    'contacts',
    sa.MetaData(),
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(length=100)),
    sa.Column('firstname', sa.String(length=30)),
    sa.Column('lastname', sa.String(length=70)),
)


def upgrade():
    # we add the new columns first
    op.add_column(
        'contacts',
        sa.Column(
            'firstname',
            sa.String(length=30),
            nullable=True
        )
    )
    op.add_column(
        'contacts',
        sa.Column(
            'lastname',
            sa.String(length=70),
            nullable=True
        )
    )
    # at this state right now, the old column is not deleted and the
    # new columns are present already. So now is the time to run the
    # content migration. We use the connection to grab all data from
    # the table, split up name into first- and lastname and update the
    # row, which is identified by its id
    for contact in connection.execute(contacthelper.select()):
        firstname, lastname = contact.name.split(' ')
        connection.execute(
            contacthelper.update().where(
                contacthelper.c.id == contact.id
            ).values(
                firstname=firstname,
                lastname=lastname
            )
        )
    # now that all data is migrated we can just drop the old column
    # without having lost any data
    op.drop_column('contacts', u'name')


def downgrade():
    # for downgrading we do it exactly the other way around
    # we add the old column again
    op.add_column(
        'contacts',
        sa.Column(
            u'name',
            mysql.VARCHAR(length=100),
            nullable=True
        )
    )
    # select all data, join firstname and lastname together to name
    # and update the entry identified by it's id.
    for contact in connection.execute(contacthelper.select()):
        name = "%s %s" % (contact.firstname, contact.lastname)
        connection.execute(
            contacthelper.update().where(
                contacthelper.c.id == contact.id
            ).values(
                name=name
            )
        )
    # now we can drop the two new columns without having lost any data.
    op.drop_column('contacts', 'firstname')
    op.drop_column('contacts', 'lastname')
