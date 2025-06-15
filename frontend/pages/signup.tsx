import { signup } from '../api';
import { useRouter } from 'next/router';
import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';

export default function Signup() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password || !confirm) {
      setError('Please fill all fields.');
      return;
    }
    if (password !== confirm) {
      setError('Passwords do not match.');
      return;
    }
    setError('');
    try {
      const data = await signup(email, password);
      localStorage.setItem('token', data.access_token ?? data.token);
      router.push('/example');
    } catch (err: any) {
      setError(err.message ?? 'Signup failed');
    }
  };

  return (
    <>
      <Head>
        <title>Sign Up | Sync & Sweat</title>
      </Head>
      <main style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 80 }}>
        <h1>Sign Up</h1>
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
          <input
            type="password"
            placeholder="Confirm Password"
            value={confirm}
            onChange={e => setConfirm(e.target.value)}
            style={{ marginBottom: 12, padding: 8 }}
            required
          />
          {error && <span style={{ color: 'red', marginBottom: 8 }}>{error}</span>}
          <button type="submit" style={{ padding: 10 }}>Sign Up</button>
        </form>
        <p style={{ marginTop: 16 }}>
          Already have an account? <Link href="/login">Login</Link>
        </p>
      </main>
    </>
  );
}
