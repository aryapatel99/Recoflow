# AWS services and rationale

| Service | Purpose | Why |
|---|---|---|
| ECS/Fargate | Backend and SSR frontend | No server management and fits two long-running HTTP services. |
| ECR | Container images | Native private image registry for ECS. |
| RDS PostgreSQL | Primary database | Managed backups, patching, and PostgreSQL compatibility. |
| Application Load Balancer | Public HTTPS routing | Health checks and separate frontend/API target groups. |
| Secrets Manager | Runtime secrets | Avoids credentials in images and Git. |
| CloudWatch Logs | Container logs and alarms | Native ECS observability. |
| IAM | Operator/task permissions | Short-lived operator auth and least-privilege workloads. |

SageMaker, S3, CloudFront, Redis, Celery, Kafka, and Kubernetes are not
selected for this initial deployment because they are not required by the
current code path.

