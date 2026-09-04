export interface Cliente {
  id: string;
  nome: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface Encomenda {
  id: string;
  cliente_id: string;
  codigo_rastreio: string;
  transportadora: string | null;
  status_atual: string | null;
  ultima_consulta: string | null;
  ativa: boolean;
  created_at: string;
  updated_at: string;
}

export interface Movimentacao {
  id: string;
  encomenda_id: string;
  status: string;
  descricao: string | null;
  local: string | null;
  data_evento: string | null;
  created_at: string;
}

export interface Mensagem {
  id: string;
  cliente_id: string;
  encomenda_id: string;
  movimentacao_id: string;
  tipo: string;
  status: string;
  conteudo: string;
  created_at: string;
  enviada_em: string | null;
}
