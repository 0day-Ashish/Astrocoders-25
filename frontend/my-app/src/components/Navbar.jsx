import { useAuth } from '../contexts/AuthContext';
import LogoutButton from './Auth/LogoutButton';


export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-gray-800 text-white p-4 flex flex-col md:flex-row justify-end gap-4">
      {user && (
        <>
          <span className="text-sm opacity-80 self-center">
            Connected as: <span className="font-mono">{user.publicKey}</span>
          </span>
          <button
            onClick={() => {
              if (window.confirm('Are you sure you want to log out?')) {
                logout();
              }
            }}
            className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded transition-colors"
          >
            Logout
          </button>
        </>
      )}
    </nav>
  );
}