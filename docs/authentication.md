# Authentication

RecoFlow validates email syntax with Pydantic's `EmailStr`, normalizes email
addresses to lowercase, and hashes passwords with bcrypt. A syntactically
valid email is sufficient to create an account; the application does not send
email, check mailbox ownership, or require SMTP configuration.

## Registration and login

`POST /auth/register` creates an active account. Duplicate email addresses
return a conflict response. `POST /auth/login` accepts the registered email
and password immediately and returns a JWT bearer token. `GET /auth/me` and
other protected routes resolve the user from that token.

The application does not determine whether an inbox exists. Users should
protect their account credentials and use an email address they control.
