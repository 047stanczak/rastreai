import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { encomendaService } from "../services/domain";
import { Encomenda, Movimentacao } from "../types";

export default function EncomendaDetalhe() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [encomenda, setEncomenda] = useState<Encomenda | null>(null);
  const [movimentacoes, setMovimentacoes] = useState<Movimentacao[]>([]);
  const [loading, setLoading] = useState(true);
  const [removendo, setRemovendo] = useState(false);

  useEffect(() => {
    if (!id) return;
    Promise.all([encomendaService.obter(id), encomendaService.movimentacoes(id)])
      .then(([enc, movs]) => {
        setEncomenda(enc);
        setMovimentacoes(movs);
      })
      .finally(() => setLoading(false));
  }, [id]);

  async function handleRemover() {
    if (!id) return;
    setRemovendo(true);
    try {
      await encomendaService.remover(id);
      navigate("/encomendas");
    } finally {
      setRemovendo(false);
    }
  }

  if (loading) return <p className="muted">Carregando...</p>;
  if (!encomenda) return <div className="empty-state">Encomenda não encontrada.</div>;

  return (
    <div>
      <h2>{encomenda.codigo_rastreio}</h2>
      <div className="card" style={{ marginBottom: 24 }}>
        <p>
          <strong>Status atual:</strong> {encomenda.status_atual || "Aguardando primeira consulta"}
        </p>
        <p>
          <strong>Transportadora:</strong> {encomenda.transportadora || "-"}
        </p>
        <p className="muted">
          Última consulta:{" "}
          {encomenda.ultima_consulta
            ? new Date(encomenda.ultima_consulta).toLocaleString("pt-BR")
            : "-"}
        </p>
        <button className="secondary" onClick={handleRemover} disabled={removendo}>
          {removendo ? "Removendo..." : "Remover encomenda"}
        </button>
      </div>

      <h3>Histórico</h3>
      {movimentacoes.length === 0 ? (
        <div className="empty-state">Nenhuma movimentação registrada ainda.</div>
      ) : (
        <div className="timeline">
          {[...movimentacoes].reverse().map((mov) => (
            <div className="timeline-item" key={mov.id}>
              <div className="timeline-dot" />
              <div>
                <div>{mov.status}</div>
                <div className="muted">
                  {mov.local || "Local não informado"}
                  {mov.data_evento && ` · ${new Date(mov.data_evento).toLocaleString("pt-BR")}`}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
