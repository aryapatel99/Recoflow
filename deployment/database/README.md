# Database deployment

Use Amazon RDS for PostgreSQL in private subnets. Do not run PostgreSQL in an
application container. Restrict the RDS security group to the backend ECS
security group on port 5432.

Create a dedicated application database user with only the permissions needed
by the application. Store the full SQLAlchemy `DATABASE_URL` in Secrets
Manager.

