# Secrets handling

Local development may use an untracked `.env`. Production must use Secrets
Manager or ECS secret references for `DATABASE_URL` and `JWT_SECRET_KEY`.
Generate the JWT secret with a password manager or a cryptographically secure
random generator. Never put it in Dockerfiles, shell history, logs, or Git.

