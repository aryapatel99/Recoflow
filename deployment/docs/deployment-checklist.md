# Deployment checklist

- [ ] AWS identity uses SSO or an assumed role.
- [ ] RDS is private and has backups enabled.
- [ ] ECS task roles use least privilege.
- [ ] Secrets Manager contains production database and JWT secrets.
- [ ] `DEBUG=false` and no localhost CORS origins are configured.
- [ ] ECR images are tagged immutably.
- [ ] Alembic is at the expected head.
- [ ] Migration task completed successfully.
- [ ] ALB HTTPS health checks pass.
- [ ] Backend `/health` and frontend routes respond.
- [ ] CloudWatch logs and alarms are configured.
- [ ] Previous ECS task definition and RDS snapshot are available for rollback.

