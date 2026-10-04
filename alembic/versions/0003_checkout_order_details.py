"""Add checkout details and order idempotency.

Revision ID: 0003_checkout_order_details
Revises: 0002_authentication
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0003_checkout_order_details"
down_revision = "0002_authentication"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "orders",
        sa.Column(
            "delivery_address",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )
    op.add_column(
        "orders",
        sa.Column(
            "shipping_method",
            sa.String(length=30),
            nullable=False,
            server_default="standard",
        ),
    )
    op.add_column(
        "orders",
        sa.Column(
            "idempotency_key",
            sa.String(length=100),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_orders_idempotency_key",
        "orders",
        ["idempotency_key"],
        unique=True,
    )
    op.alter_column("orders", "idempotency_key", nullable=False)
    op.alter_column("orders", "delivery_address", server_default=None)
    op.alter_column("orders", "shipping_method", server_default=None)


def downgrade() -> None:
    op.drop_index("ix_orders_idempotency_key", table_name="orders")
    op.drop_column("orders", "idempotency_key")
    op.drop_column("orders", "shipping_method")
    op.drop_column("orders", "delivery_address")
