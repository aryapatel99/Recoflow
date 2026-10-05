# IAM minimum roles

- **Deployment operator**: ECR push, ECS service update/describe, CloudWatch
  log read, and `sts:GetCallerIdentity`; scope resources to the deployment
  account and region.
- **ECS task execution role**: pull from the two ECR repositories and write
  stdout/stderr to the configured CloudWatch log groups.
- **Backend task role**: read only the named Secrets Manager secrets. Add S3
  access only if the application later uploads objects.
- **Frontend task role**: normally no AWS permissions.

Do not grant `AdministratorAccess` to runtime tasks.

