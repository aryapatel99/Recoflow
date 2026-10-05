# RecoFlow AWS deployment

This package describes a small production deployment that preserves the
modular monolith:

- **ECS/Fargate** runs the FastAPI API and the Next.js SSR storefront as two
  services in one ECS cluster.
- **RDS PostgreSQL** stores application data.
- **Application Load Balancer** exposes the backend and frontend over HTTPS.
- **Secrets Manager** supplies `DATABASE_URL` and `JWT_SECRET_KEY` at runtime.
- **CloudWatch Logs** collects container logs.
- **ECR** stores the two container images.
- **IAM task roles** are used instead of static AWS access keys.

S3 and CloudFront are not required for the current application because product
images are external URLs and the storefront uses Next.js server rendering.
Add them only when assets or a CDN are actually needed.

## Prerequisites

Install and authenticate:

1. AWS CLI v2 (`aws configure sso` is preferred).
2. Docker Desktop.
3. PowerShell 7 or Windows PowerShell 5.1.
4. An AWS account with permission to create ECR, ECS, RDS, ALB, IAM, Secrets
   Manager, CloudWatch, and networking resources.
5. A VPC with private subnets for RDS and ECS tasks, public subnets for the
   ALB, and security groups allowing only ALB-to-task and task-to-RDS traffic.

Do not put access keys, database passwords, or JWT secrets in this directory.
Use an AWS IAM role or SSO locally and Secrets Manager at runtime.

## Deployment order

1. Create the VPC, security groups, RDS instance, ECS cluster, task execution
   role, task roles, ALB, and target groups.
2. Create ECR repositories and push images with
   `scripts/deploy-backend.ps1` and the corresponding frontend image process.
3. Store runtime secrets in Secrets Manager and wire them into ECS task
   definitions.
4. Run `alembic upgrade head` once against RDS using
   `scripts/health-check.ps1` only after the migration task is configured.
5. Deploy the backend and frontend services.
6. Set the frontend `NEXT_PUBLIC_API_URL` to the public backend URL at image
   build time, and set backend `CORS_ORIGINS` to the public storefront URL.
7. Configure HTTPS certificates in ACM and redirect HTTP to HTTPS at the ALB.

The scripts in this folder validate inputs and do not create or delete AWS
infrastructure automatically. Destructive operations require explicit manual
steps.

## Verification and rollback

Use `scripts/verify-aws.ps1` for AWS identity and resource checks, then
`scripts/health-check.ps1 -Url https://api.example.com/health` for the API.
Rollback by updating the ECS service to the previous immutable image tag.
Database migrations are forward-only; take an RDS snapshot before applying
irreversible schema changes.

See the focused documents under `docs/` and the service notes under
`backend/`, `frontend/`, and `database/`.

