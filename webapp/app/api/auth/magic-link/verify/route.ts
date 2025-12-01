import { NextRequest, NextResponse } from 'next/server';

export const dynamic = 'force-dynamic'; // ⚠️ Force le mode dynamique pour éviter le cache Vercel

export async function GET(request: NextRequest) {
  const token = request.nextUrl.searchParams.get('token');

  // 1. Validation du token
  if (!token) {
    return NextResponse.json({ detail: 'Token manquant dans l\'URL' }, { status: 400 });
  }

  // 2. Définition de l'URL (Hardcodée pour être sûr à 100%)
  const RAILWAY_URL = "https://ava-startup-production.up.railway.app";
  const targetUrl = `${RAILWAY_URL}/api/v1/auth/magic-link/verify?token=${encodeURIComponent(token)}`;

  console.log(`🕵️‍♂️ DEBUG: Tentative de connexion vers -> ${targetUrl}`);

  try {
    // 3. Appel au Backend
    const response = await fetch(targetUrl, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store'
    });

    console.log(`🕵️‍♂️ DEBUG: Réponse Backend Status -> ${response.status}`);

    // 4. Lecture sécurisée de la réponse (Texte d'abord, JSON ensuite)
    const responseText = await response.text();
    console.log(`🕵️‍♂️ DEBUG: Réponse Backend Body -> ${responseText.substring(0, 200)}...`);

    try {
      const data = JSON.parse(responseText);
      // Si c'est du JSON valide, on le renvoie
      return NextResponse.json(data, { status: response.status });
    } catch (jsonError) {
      // Si ce n'est pas du JSON (ex: page d'erreur HTML de Railway), on l'affiche
      console.error('🔥 ERREUR JSON:', jsonError);
      return NextResponse.json(
        { 
          detail: 'Le backend a répondu mais pas en JSON (Erreur HTML probable)', 
          raw_response: responseText,
          target_url: targetUrl
        },
        { status: 502 } // Bad Gateway
      );
    }

  } catch (error: any) {
    // 5. Erreur Réseau (Vercel n'arrive même pas à toucher Railway)
    console.error('🔥 ERREUR RESEAU:', error);
    return NextResponse.json(
      { 
        detail: 'Echec de connexion Vercel -> Railway', 
        error_message: error.message,
        target_url: targetUrl
      },
      { status: 500 }
    );
  }
}
