import { Keypair } from '@stellar/stellar-sdk';

export async function stellarAuth(secretKey) {
  const keypair = Keypair.fromSecret(secretKey);
  const challenge = "AstroCodersAuth123"; // Must match backend's AUTH_CHALLENGE
  
  try {
    const signature = keypair.sign(Buffer.from(challenge)).toString('base64');
    const response = await fetch('http://localhost:8000/auth/stellar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        public_key: keypair.publicKey(),
        signed_challenge: signature
      })
    });
    return await response.json();
  } catch (error) {
    console.error("Auth failed:", error);
    throw error;
  }
}

// Usage in React component
import { stellarAuth } from './utils/auth';

function LoginButton() {
  const handleLogin = async () => {
    try {
      const result = await stellarAuth('SBC...W5PJ'); // From user input
      localStorage.setItem('jwt', result.access_token);
      console.log("Authenticated!", result);
    } catch (err) {
      alert("Authentication failed");
    }
  };

  return <button onClick={handleLogin}>Connect Wallet</button>;
}