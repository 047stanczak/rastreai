import { FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { encomendaService } from "../services/domain";
import { Encomenda } from "../types";
import { ApiError } from "../services/api";

export default function Encomendas() {
  const navigate = useNavigate();
  const [encomendas, setEncomendas] = useState<Encomenda[]>([]);
  const [loading, setLoading] = useState(true);
  const [codigo, setCodigo] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [criando, setCriando] = useState(false);

  function carregar() {
    setLoading(true);
    encomendaService
      .listar()
      .then(setEncomendas)
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    carregar();
  }, []);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setCriando(true);
    try {
      await encomendaService.criar(codigo);
      setCodigo("");
      carregar();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Não foi possível cadastrar a encomenda");
    } finally {
      setCriando(false);
    }
  }

  return (
    <div>
      <h2>Minhas encomendas</h2>

      <form className="form" style={{ flexDirection: "row", marginBottom: 24 }} onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Código de rastreio"
          value={codigo}
          onChange={(e) => setCodigo(e.target.value)}
          required
        />
        <button type="submit" disabled={criando}>
          {criando ? "Cadastrando..." : "Cadastrar"}
        </button>
      </form>
      {error && <span className="error">{error}</span>}

      {loading ? (
        <p className="muted">Carregando...</p>
      ) : encomendas.length === 0 ? (
        <div className="empty-state">Nenhuma encomenda cadastrada ainda.</div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Código</th>
              <th>Status</th>
              <th>Transportadora</th>
              <th>Última atualização</th>
            </tr>
          </thead>
          <tbody>
            {encomendas.map((enc) => (
              <tr key={enc.id} onClick={() => navigate(`/encomendas/${enc.id}`)}>
                <td>{enc.codigo_rastreio}</td>
                <td>
                  <span className="badge">{enc.status_atual || "Aguardando consulta"}</span>
                </td>
                <td>{enc.transportadora || "-"}</td>
                <td>
                  {enc.ultima_consulta
                    ? new Date(enc.ultima_consulta).toLocaleString("pt-BR")
                    : "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
