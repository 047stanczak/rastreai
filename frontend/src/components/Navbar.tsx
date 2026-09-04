import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export function Navbar() {
  const { logout } = useAuth();

  return (
    <div className="navbar">
      <strong>RastreiaAi</strong>
      <nav>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/encomendas">Encomendas</Link>
        <Link to="/mensagens">Mensagens</Link>
        <button className="secondary" onClick={logout}>
          Sair
        </button>
      </nav>
    </div>
  );
}
