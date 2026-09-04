import { api } from "./api";
import { Cliente, Encomenda, Mensagem, Movimentacao } from "../types";

export const authService = {
  register: (nome: string, email: string, senha: string) =>
    api.post<Cliente>("/api/auth/register", { nome, email, senha }),
  login: (email: string, senha: string) =>
    api.post<{ access_token: string }>("/api/auth/login", { email, senha }),
};

export const clienteService = {
  me: () => api.get<Cliente>("/api/clientes/me"),
};

export const encomendaService = {
  listar: () => api.get<Encomenda[]>("/api/encomendas"),
  obter: (id: string) => api.get<Encomenda>(`/api/encomendas/${id}`),
  criar: (codigo_rastreio: string) =>
    api.post<Encomenda>("/api/encomendas", { codigo_rastreio }),
  remover: (id: string) => api.delete<void>(`/api/encomendas/${id}`),
  movimentacoes: (id: string) =>
    api.get<Movimentacao[]>(`/api/encomendas/${id}/movimentacoes`),
};

export const mensagemService = {
  listar: () => api.get<Mensagem[]>("/api/mensagens"),
};
