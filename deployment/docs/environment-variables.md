# Environment variables

## Backend runtime

`APP_ENV`, `DEBUG`, `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`,
`ACCESS_TOKEN_EXPIRE_MINUTES`, and `CORS_ORIGINS` are used by the backend.
`AWS_REGION` is deployment metadata only; the current backend does not call
AWS services directly.

## Frontend build

`NEXT_PUBLIC_API_URL` is required for the server-side proxy and is baked into
the Next.js build. It must be the public backend origin in production.

