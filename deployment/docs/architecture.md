# Selected architecture

The initial AWS topology is ECS/Fargate + RDS PostgreSQL + an ALB. FastAPI and
Next.js remain separate ECS services but the application remains a modular
monolith. This avoids Kubernetes, queues, caches, and ML infrastructure that
the current workload does not require.

The backend owns prices, orders, authentication, events, and recommendations.
The frontend is an SSR presentation layer and forwards browser requests to the
backend proxy.

