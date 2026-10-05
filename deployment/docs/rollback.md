# Rollback

Deploy immutable image tags, keep the previous ECS task definition revision,
and update the service back to the previous revision if health checks fail.
Do not automatically roll back database migrations. Restore from an RDS
snapshot or apply a reviewed forward migration after assessing data impact.

