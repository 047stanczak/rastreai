# Infra

Infraestrutura mínima para desenvolvimento local via Docker Compose.

- `docker/`: reservado para configurações auxiliares de containers (vazio por enquanto — os Dockerfiles ficam junto de cada serviço em `backend/` e `frontend/`).

Não há Terraform, Kubernetes ou CI/CD nesta fase. O objetivo é apenas rodar tudo localmente com `docker compose up --build`, mantendo backend, frontend e banco desacoplados o suficiente para migrar para AWS depois (ECS/RDS/S3+CloudFront, por exemplo) sem alterar a lógica da aplicação.
