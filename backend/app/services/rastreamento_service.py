import hashlib
from datetime import datetime, timezone
from typing import List

from dateutil import parser as date_parser

from app.integrations.linketrack import LinkeTrackClient, EventoRastreio
from app.models.encomenda import Encomenda
from app.models.mensagem import Mensagem
from app.models.movimentacao import Movimentacao
from app.repositories.encomenda_repository import EncomendaRepository
from app.repositories.mensagem_repository import MensagemRepository
from app.repositories.movimentacao_repository import MovimentacaoRepository


class RastreamentoService:
    def __init__(
        self,
        encomenda_repository: EncomendaRepository,
        movimentacao_repository: MovimentacaoRepository,
        mensagem_repository: MensagemRepository,
        linketrack_client: LinkeTrackClient,
    ):
        self.encomenda_repository = encomenda_repository
        self.movimentacao_repository = movimentacao_repository
        self.mensagem_repository = mensagem_repository
        self.linketrack_client = linketrack_client

    def _dedup_hash(self, codigo_rastreio: str, evento: EventoRastreio) -> str:
        chave = (
            codigo_rastreio
            + evento["data_evento"]
            + evento["status"]
            + evento["descricao"]
            + evento["local"]
        )
        return hashlib.sha256(chave.encode()).hexdigest()

    def _parse_data(self, valor: str):
        if not valor:
            return None
        try:
            return date_parser.parse(valor)
        except (ValueError, TypeError):
            return None

    def atualizar_encomenda(self, encomenda: Encomenda) -> List[Movimentacao]:
        """Consulta a Link&Track, persiste apenas movimentações novas e gera mensagens."""
        eventos = self.linketrack_client.consultar(encomenda.codigo_rastreio)
        hashes_existentes = self.movimentacao_repository.get_hashes_existentes(encomenda.id)

        novas: List[Movimentacao] = []
        for evento in eventos:
            dedup_hash = self._dedup_hash(encomenda.codigo_rastreio, evento)
            if dedup_hash in hashes_existentes:
                continue

            movimentacao = Movimentacao(
                encomenda_id=encomenda.id,
                status=evento["status"],
                descricao=evento["descricao"],
                local=evento["local"],
                data_evento=self._parse_data(evento["data_evento"]),
                dedup_hash=dedup_hash,
            )
            movimentacao = self.movimentacao_repository.create(movimentacao)
            novas.append(movimentacao)
            self._criar_mensagem(encomenda, movimentacao)

        if eventos:
            encomenda.status_atual = eventos[-1]["status"]
        encomenda.ultima_consulta = datetime.now(timezone.utc)
        self.encomenda_repository.save(encomenda)

        return novas

    def _criar_mensagem(self, encomenda: Encomenda, movimentacao: Movimentacao) -> Mensagem:
        conteudo = (
            f"Sua encomenda {encomenda.codigo_rastreio} teve uma nova movimentação.\n\n"
            f"{movimentacao.status}.\n\n"
            f"Local: {movimentacao.local or 'não informado'}\n"
            f"Data: {movimentacao.data_evento.strftime('%d/%m/%Y %H:%M') if movimentacao.data_evento else 'não informada'}"
        )
        mensagem = Mensagem(
            cliente_id=encomenda.cliente_id,
            encomenda_id=encomenda.id,
            movimentacao_id=movimentacao.id,
            tipo="SISTEMA",
            status="ENVIADA",
            conteudo=conteudo,
            enviada_em=datetime.now(timezone.utc),
        )
        return self.mensagem_repository.create(mensagem)
