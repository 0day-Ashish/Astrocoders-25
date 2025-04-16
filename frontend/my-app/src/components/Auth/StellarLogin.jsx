// src/components/Auth/StellarLogin.jsx
import { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { stellarAuth } from '../../utils/auth';

export default function StellarLogin() {
  const [secretKey, setSecretKey] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth(); // Get login function from context

  const handleLogin = async () => {
    try {
      const { access_token, public_key } = await stellarAuth(secretKey);
      login(access_token, public_key); // Store token + user in context
    } catch (err) {
      setError('Authentication failed');
    }
  };

  return (
    <div>
      <input
        type="password"
        value={secretKey}
        onChange={(e) => setSecretKey(e.target.value)}
        placeholder="Enter Stellar secret key"
      />
      <button onClick={handleLogin}>Login</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}