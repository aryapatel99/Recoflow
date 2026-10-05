# AWS account setup

Use IAM Identity Center/SSO or a short-lived assumed role for operators.
Workloads should use ECS task roles. Static access keys must not be stored in
the repository or injected into container images.

Required operator capabilities are documented in
`iam/README.md`. Restrict them to the deployment account and region.

