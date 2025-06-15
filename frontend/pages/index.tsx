import Head from 'next/head';
import Link from 'next/link';

export default function Home() {
  return (
    <>
      <Head>
        <title>Sync & Sweat</title>
        <meta name="description" content="Personalized fitness companion" />
      </Head>
      <main style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 80 }}>
        <h1>Welcome to Sync & Sweat</h1>
        <p>Your personalized fitness companion for dynamic workouts and curated playlists.</p>
        <div style={{ marginTop: 32 }}>
          <Link href="/login">Login</Link> | <Link href="/signup">Sign Up</Link>
        </div>
      </main>
    </>
  );
}
