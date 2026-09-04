import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { encomendaService } from "../services/domain";
import { Encomenda } from "../types";

export default function Dashboard() {
  const [encomendas, setEncomendas] = useState<Encomenda[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    encomendaService
      .listar()
      .then(setEncomendas)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="muted">Carregando...</p>;

  const entregues = encomendas.filter((e) => e.status_atual?.toLowerCase().includes("entregue"));
  const emTransito = encomendas.filter((e) => !e.status_atual?.toLowerCase().includes("entregue"));

  return (
    <div>
      <h2>Dashboard</h2>
      <div className="stats">
        <div className="card">
          <div className="stat-value">{encomendas.length}</div>
          <div className="muted">Encomendas</div>
        </div>
        <div className="card">
          <div className="stat-value">{emTransito.length}</div>
          <div className="muted">Em trânsito</div>
        </div>
        <div className="card">
          <div className="stat-value">{entregues.length}</div>
          <div className="muted">Entregues</div>
        </div>
      </div>

      <h3>Últimas encomendas</h3>
      {encomendas.length === 0 ? (
        <div className="empty-state">
          Nenhuma encomenda cadastrada ainda. <Link to="/encomendas">Cadastrar encomenda</Link>
        </div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Código</th>
              <th>Status</th>
              <th>Última consulta</th>
            </tr>
          </thead>
          <tbody>
            {encomendas.slice(0, 5).map((e) => (
              <tr key={e.id} onClick={() => (window.location.href = `/encomendas/${e.id}`)}>
                <td>{e.codigo_rastreio}</td>
                <td>{e.status_atual || "Aguardando primeira consulta"}</td>
                <td>{e.ultima_consulta ? new Date(e.ultima_consulta).toLocaleString("pt-BR") : "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
