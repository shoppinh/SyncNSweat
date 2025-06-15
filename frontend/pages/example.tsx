import Button from '../components/Button';
import { fetchUserProfile } from '../api';
import { useEffect, useState } from 'react';

export default function ExamplePage() {
  const [profile, setProfile] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    if (token) {
      fetchUserProfile(token)
        .then(setProfile)
        .catch((err) => setError(err.message));
    }
  }, []);

  if (error) return <div>Error: {error}</div>;
  if (!profile) return <div>Loading...</div>;
  return (
    <div style={{ padding: 32 }}>
      <h2>Reusable Button Example</h2>
      <Button onClick={() => alert('Clicked!')}>Click Me</Button>
      <h1>Welcome, {profile.username ?? profile.email}!</h1>
      {/* Render more profile info here */}
    </div>
  );
}
