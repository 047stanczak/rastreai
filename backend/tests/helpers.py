def criar_e_autenticar(client, email="joao@teste.com"):
    client.post(
        "/api/auth/register",
        json={"nome": "João", "email": email, "senha": "senha123"},
    )
    response = client.post("/api/auth/login", json={"email": email, "senha": "senha123"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
