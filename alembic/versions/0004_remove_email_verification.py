"""Remove email ownership verification columns.

Revision ID: 0004_remove_email_verification
Revises: 0003_checkout_order_details
"""

from alembic import op


revision = "0004_remove_email_verification"
down_revision = "0003_checkout_order_details"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "DROP INDEX IF EXISTS ix_users_email_verification_token_hash"
    )
    op.execute(
        "ALTER TABLE users DROP COLUMN IF EXISTS email_verification_expires_at"
    )
    op.execute(
        "ALTER TABLE users DROP COLUMN IF EXISTS email_verification_token_hash"
    )
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS email_verified")


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS email_verified BOOLEAN NOT NULL DEFAULT FALSE
        """
    )
    op.execute(
        """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS email_verification_token_hash VARCHAR(64)
        """
    )
    op.execute(
        """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS email_verification_expires_at TIMESTAMPTZ
        """
    )
    op.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS
        ix_users_email_verification_token_hash
        ON users(email_verification_token_hash)
        WHERE email_verification_token_hash IS NOT NULL
        """
    )
