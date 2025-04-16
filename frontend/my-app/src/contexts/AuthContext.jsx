import { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null); // Stores Stellar publicKey + JWT

  // Called after successful Stellar auth
  const login = (token, publicKey) => {
    localStorage.setItem('jwt', token);
    setUser({ publicKey });
  };

  const logout = () => {
    localStorage.removeItem('jwt');
    setUser(null);
    toast.success("Logged out successfully");
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook for easy access
export function useAuth() {
  return useContext(AuthContext);
}