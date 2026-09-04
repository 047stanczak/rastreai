def test_cadastro_cliente(client):
    response = client.post(
        "/api/auth/register",
        json={"nome": "João", "email": "joao@teste.com", "senha": "senha123"},
    )
    assert response.status_code == 201
    assert response.json()["email"] == "joao@teste.com"


def test_cadastro_email_duplicado(client):
    client.post(
        "/api/auth/register",
        json={"nome": "João", "email": "joao@teste.com", "senha": "senha123"},
    )
    response = client.post(
        "/api/auth/register",
        json={"nome": "João 2", "email": "joao@teste.com", "senha": "outrasenha"},
    )
    assert response.status_code == 400


def test_login_sucesso(client):
    client.post(
        "/api/auth/register",
        json={"nome": "João", "email": "joao@teste.com", "senha": "senha123"},
    )
    response = client.post(
        "/api/auth/login", json={"email": "joao@teste.com", "senha": "senha123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_credenciais_invalidas(client):
    response = client.post(
        "/api/auth/login", json={"email": "naoexiste@teste.com", "senha": "x"}
    )
    assert response.status_code == 401


def test_acesso_sem_token(client):
    response = client.get("/api/clientes/me")
    assert response.status_code == 403
