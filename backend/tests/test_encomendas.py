from tests.helpers import criar_e_autenticar

EVENTOS_MOCK_1 = [
    {"status": "Objeto postado", "descricao": "", "local": "Curitiba - PR", "data_evento": "2026-08-15T10:00:00"},
    {"status": "Objeto em trânsito", "descricao": "", "local": "São Paulo - SP", "data_evento": "2026-08-16T10:00:00"},
]

EVENTOS_MOCK_2 = EVENTOS_MOCK_1 + [
    {"status": "Objeto saiu para entrega", "descricao": "", "local": "São Paulo - SP", "data_evento": "2026-08-17T10:00:00"},
]


def test_criar_encomenda(client, mocker):
    mocker.patch(
        "app.integrations.linketrack.LinkeTrackClient.consultar",
        return_value=EVENTOS_MOCK_1,
    )
    headers = criar_e_autenticar(client)
    response = client.post(
        "/api/encomendas", json={"codigo_rastreio": "AA123456789BR"}, headers=headers
    )
    assert response.status_code == 201
    assert response.json()["codigo_rastreio"] == "AA123456789BR"
    assert response.json()["status_atual"] == "Objeto em trânsito"


def test_listar_encomendas(client, mocker):
    mocker.patch(
        "app.integrations.linketrack.LinkeTrackClient.consultar",
        return_value=EVENTOS_MOCK_1,
    )
    headers = criar_e_autenticar(client)
    client.post("/api/encomendas", json={"codigo_rastreio": "AA123456789BR"}, headers=headers)
    response = client.get("/api/encomendas", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_acesso_indevido_encomenda_de_outro_cliente(client, mocker):
    mocker.patch(
        "app.integrations.linketrack.LinkeTrackClient.consultar",
        return_value=EVENTOS_MOCK_1,
    )
    headers_a = criar_e_autenticar(client, email="a@teste.com")
    headers_b = criar_e_autenticar(client, email="b@teste.com")

    criada = client.post(
        "/api/encomendas", json={"codigo_rastreio": "AA123456789BR"}, headers=headers_a
    ).json()

    response = client.get(f"/api/encomendas/{criada['id']}", headers=headers_b)
    assert response.status_code == 404


def test_novas_movimentacoes_nao_duplicam(client, db_session, mocker):
    mock = mocker.patch("app.integrations.linketrack.LinkeTrackClient.consultar")
    mock.return_value = EVENTOS_MOCK_1
    headers = criar_e_autenticar(client)
    criada = client.post(
        "/api/encomendas", json={"codigo_rastreio": "AA123456789BR"}, headers=headers
    ).json()

    movs = client.get(f"/api/encomendas/{criada['id']}/movimentacoes", headers=headers).json()
    assert len(movs) == 2

    # segunda consulta: mesmos 2 eventos + 1 novo. Exercita o RastreamentoService
    # diretamente sobre a mesma encomenda, simulando o que o scheduler faria.
    from app.integrations.linketrack import LinkeTrackClient
    from app.repositories.encomenda_repository import EncomendaRepository
    from app.repositories.mensagem_repository import MensagemRepository
    from app.repositories.movimentacao_repository import MovimentacaoRepository
    from app.services.rastreamento_service import RastreamentoService

    mock.return_value = EVENTOS_MOCK_2
    encomenda_repository = EncomendaRepository(db_session)
    encomenda = encomenda_repository.get_by_id(criada["id"])
    rastreamento_service = RastreamentoService(
        encomenda_repository,
        MovimentacaoRepository(db_session),
        MensagemRepository(db_session),
        LinkeTrackClient(),
    )
    novas = rastreamento_service.atualizar_encomenda(encomenda)
    assert len(novas) == 1
    assert novas[0].status == "Objeto saiu para entrega"

    movs_final = client.get(
        f"/api/encomendas/{criada['id']}/movimentacoes", headers=headers
    ).json()
    assert len(movs_final) == 3


def test_criar_mensagem_ao_detectar_nova_movimentacao(client, mocker):
    mocker.patch(
        "app.integrations.linketrack.LinkeTrackClient.consultar",
        return_value=EVENTOS_MOCK_1,
    )
    headers = criar_e_autenticar(client)
    client.post("/api/encomendas", json={"codigo_rastreio": "AA123456789BR"}, headers=headers)

    mensagens = client.get("/api/mensagens", headers=headers).json()
    assert len(mensagens) == 2
    assert "AA123456789BR" in mensagens[0]["conteudo"]


def test_remover_encomenda(client, mocker):
    mocker.patch(
        "app.integrations.linketrack.LinkeTrackClient.consultar",
        return_value=EVENTOS_MOCK_1,
    )
    headers = criar_e_autenticar(client)
    criada = client.post(
        "/api/encomendas", json={"codigo_rastreio": "AA123456789BR"}, headers=headers
    ).json()

    response = client.delete(f"/api/encomendas/{criada['id']}", headers=headers)
    assert response.status_code == 204

    response = client.get(f"/api/encomendas/{criada['id']}", headers=headers)
    assert response.status_code == 404
