"""migrate test

Revision ID: 00b8a8d4ff9e
Revises: 
Create Date: 2024-04-10 22:35:42.381867

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '00b8a8d4ff9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dosen',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('nidn', sa.String(length=30), nullable=False),
    sa.Column('nama', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.String(length=13), nullable=False),
    sa.Column('alamat', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.Column('level', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)

    op.create_table('mahasiswa',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('nim', sa.String(length=30), nullable=False),
    sa.Column('nama', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.String(length=13), nullable=False),
    sa.Column('alamat', sa.String(length=100), nullable=False),
    sa.Column('dosen_satu', sa.BigInteger(), nullable=True),
    sa.Column('dosen_dua', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['dosen_dua'], ['dosen.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['dosen_satu'], ['dosen.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('dim_financial_type')
    op.drop_table('dim_time')
    op.drop_table('fact_purchase')
    op.drop_table('dim_purchase_detail')
    op.drop_table('fact_sale')
    op.drop_table('dim_sale_detail')
    op.drop_table('dim_user')
    op.drop_table('dim_product_variant')
    op.drop_table('dim_supplier')
    op.drop_table('fact_financial')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fact_financial',
    sa.Column('financial_type_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True),
    sa.Column('cash_in', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('cash_out', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('balance', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('dim_supplier',
    sa.Column('supplier_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('supplier_name', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('supplier_id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('dim_product_variant',
    sa.Column('product_variant_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('category_name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('variant_name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('product_variant_code', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('product_variant_name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('product_quantity', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('purchase_price', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('sale_price', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('brand', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('variant_stock', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('product_variant_id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('dim_user',
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('role_name', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('dim_sale_detail',
    sa.Column('sale_detail_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('sale_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('product_variant_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('sale_price', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('quantity', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('subtotal', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('sale_detail_id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('fact_sale',
    sa.Column('sale_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True),
    sa.Column('total_item', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('total_price', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('profit', mysql.DOUBLE(asdecimal=True), nullable=True),
    sa.PrimaryKeyConstraint('sale_id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('dim_purchase_detail',
    sa.Column('purchase_detail_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('purchase_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('product_variant_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('purchase_price', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('quantity', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('subtotal', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('purchase_detail_id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('fact_purchase',
    sa.Column('purchase_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('supplier_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_id', mysql.BIGINT(display_width=20), autoincrement=False, nullable=True),
    sa.Column('total_item', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('total_price', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('purchase_id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('dim_time',
    sa.Column('time_id', mysql.BIGINT(display_width=20), autoincrement=True, nullable=False),
    sa.Column('date', mysql.DATETIME(), nullable=True),
    sa.Column('day', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('month', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('month_name', mysql.TINYTEXT(), nullable=False),
    sa.Column('quarter', mysql.TINYTEXT(), nullable=False),
    sa.Column('year', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('time_id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('dim_financial_type',
    sa.Column('financial_type_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('financial_type_name', mysql.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('financial_type_id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('mahasiswa')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('dosen')
    # ### end Alembic commands ###
