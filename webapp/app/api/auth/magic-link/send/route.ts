import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { email } = await request.json();
    
    // 🚨 FIX: Adresse en dur pour garantir la connexion
    const backendUrl = "https://ava-startup-production.up.railway.app";
    
    console.log(`🚀 Sending magic link request to: ${backendUrl}`);

    const response = await fetch(`${backendUrl}/api/v1/auth/magic-link/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email }),
    });
    
    const data = await response.json();
    
    // Si le backend renvoie une erreur, on la renvoie au front
    if (!response.ok) {
      return NextResponse.json(data, { status: response.status });
    }
    
    return NextResponse.json(data, { status: 200 });
    
  } catch (error) {
    console.error('🔥 Magic link proxy error:', error);
    return NextResponse.json(
      { detail: 'Internal connection error' },
      { status: 500 }
    );
  }
}
