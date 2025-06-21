import { login } from '../api';
import { useRouter } from 'next/router';
import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const data = await login(email, password);
      localStorage.setItem('token', data.access_token ?? data.token);
      router.push('/example');
    } catch (err: any) {
      setError(err.message ?? 'Login failed');
    }
  };

  return (
    <>
      <Head>
        <title>Login | Sync & Sweat</title>
      </Head>
      <main style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 80 }}>
        <h1>Login</h1>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', width: 300 }}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            style={{ marginBottom: 12, padding: 8 }}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            style={{ marginBottom: 12, padding: 8 }}
            required
          />
          {error && <span style={{ color: 'red', marginBottom: 8 }}>{error}</span>}
          <button type="submit" style={{ padding: 10 }}>Login</button>
        </form>
        <p style={{ marginTop: 16 }}>
          Don't have an account? <Link href="/signup">Sign Up</Link>
        </p>
      </main>
    </>
  );
}
