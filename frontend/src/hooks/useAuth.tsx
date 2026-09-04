import { createContext, useContext, useState, ReactNode } from "react";
import { authService } from "../services/domain";

interface AuthContextValue {
  isAuthenticated: boolean;
  login: (email: string, senha: string) => Promise<void>;
  register: (nome: string, email: string, senha: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem("token"));

  async function login(email: string, senha: string) {
    const { access_token } = await authService.login(email, senha);
    localStorage.setItem("token", access_token);
    setIsAuthenticated(true);
  }

  async function register(nome: string, email: string, senha: string) {
    await authService.register(nome, email, senha);
    await login(email, senha);
  }

  function logout() {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth deve ser usado dentro de AuthProvider");
  return context;
}
