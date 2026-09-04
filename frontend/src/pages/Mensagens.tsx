import { useEffect, useState } from "react";
import { mensagemService } from "../services/domain";
import { Mensagem } from "../types";

export default function Mensagens() {
  const [mensagens, setMensagens] = useState<Mensagem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    mensagemService
      .listar()
      .then(setMensagens)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="muted">Carregando...</p>;

  return (
    <div>
      <h2>Mensagens</h2>
      {mensagens.length === 0 ? (
        <div className="empty-state">Nenhuma mensagem recebida ainda.</div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {mensagens.map((m) => (
            <div className="card" key={m.id}>
              <p style={{ whiteSpace: "pre-line", margin: 0 }}>{m.conteudo}</p>
              <p className="muted" style={{ marginBottom: 0 }}>
                {m.enviada_em ? new Date(m.enviada_em).toLocaleString("pt-BR") : "-"}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
