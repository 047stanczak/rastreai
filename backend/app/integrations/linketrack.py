from typing import List, TypedDict

import httpx

from app.config import settings


class EventoRastreio(TypedDict):
    status: str
    descricao: str
    local: str
    data_evento: str


def _mapear_evento(evento: dict) -> EventoRastreio:
    return {
        "status": evento.get("descricao", ""),
        "descricao": evento.get("detalhe", ""),
        "local": evento.get("local", ""),
        "data_evento": evento.get("data", ""),
    }


class LinkeTrackClient:
    """Isola toda comunicação com a API externa de rastreamento (seurastreio.com.br)."""

    def __init__(self):
        self.base_url = settings.LINKE_TRACK_BASE_URL
        self.token = settings.LINKE_TRACK_TOKEN

    def consultar(self, codigo_rastreio: str) -> List[EventoRastreio]:
        response = httpx.get(
            f"{self.base_url}/api/public/rastreio/{codigo_rastreio}",
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("success"):
            return []

        # Plano pago retorna "historico" (mais recente primeiro); plano gratuito
        # retorna somente "eventoMaisRecente". Normalizamos para ordem cronológica
        # (mais antigo primeiro), que é o que o RastreamentoService espera.
        if "historico" in data:
            eventos_brutos = list(reversed(data["historico"]))
        elif data.get("eventoMaisRecente"):
            eventos_brutos = [data["eventoMaisRecente"]]
        else:
            eventos_brutos = []

        return [_mapear_evento(evento) for evento in eventos_brutos]

