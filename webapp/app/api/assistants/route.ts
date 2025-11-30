import { NextRequest, NextResponse } from 'next/server';

/**
 * GET /api/assistants
 * Proxie la requête vers le backend FastAPI pour récupérer la liste des assistants Vapi
 */
export async function GET(request: NextRequest) {
  try {
    // Récupérer le token d'authentification depuis le header
    const authHeader = request.headers.get('Authorization');
    
    if (!authHeader) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Forward vers backend FastAPI
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/assistants`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': authHeader,
      },
    });

    const data = await response.json();
    
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Error fetching assistants:', error);
    return NextResponse.json(
      { error: 'Failed to fetch assistants' },
      { status: 500 }
    );
  }
}
