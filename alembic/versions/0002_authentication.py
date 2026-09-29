"""add authentication and email verification fields

Revision ID: 0002_authentication
Revises: 0001_initial_schema
Create Date: 2026-09-29
"""

from alembic import op


revision = "0002_authentication"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS email_verified BOOLEAN NOT NULL DEFAULT FALSE
        """
    )

    op.execute(
        """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS
        email_verification_token_hash VARCHAR(64)
        """
    )

    op.execute(
        """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS
        email_verification_expires_at TIMESTAMPTZ
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


def downgrade() -> None:
    op.execute(
        """
        DROP INDEX IF EXISTS
        ix_users_email_verification_token_hash
        """
    )

    op.execute(
        """
        ALTER TABLE users
        DROP COLUMN IF EXISTS email_verification_expires_at
        """
    )

    op.execute(
        """
        ALTER TABLE users
        DROP COLUMN IF EXISTS email_verification_token_hash
        """
    )

    op.execute(
        """
        ALTER TABLE users
        DROP COLUMN IF EXISTS email_verified
        """
    )