import { Navigate, Route, Routes } from "react-router-dom";
import { ProtectedRoute } from "../components/ProtectedRoute";
import Login from "../pages/Login";
import Register from "../pages/Register";
import Dashboard from "../pages/Dashboard";
import Encomendas from "../pages/Encomendas";
import EncomendaDetalhe from "../pages/EncomendaDetalhe";
import Mensagens from "../pages/Mensagens";

export function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/encomendas" element={<Encomendas />} />
        <Route path="/encomendas/:id" element={<EncomendaDetalhe />} />
        <Route path="/mensagens" element={<Mensagens />} />
      </Route>

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
