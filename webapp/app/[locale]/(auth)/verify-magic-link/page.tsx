'use client';

import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function VerifyMagicLinkPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const token = searchParams.get('token');

    if (!token) {
      setStatus('error');
      setMessage('Lien invalide');
      return;
    }

    // Vérifier le token
    verifyToken(token);
  }, [searchParams]);

  const verifyToken = async (token: string) => {
    try {
      const response = await fetch(`/api/auth/magic-link/verify?token=${encodeURIComponent(token)}`);
      const data = await response.json();

      if (response.ok) {
        // Sauvegarder les tokens
        if (typeof window !== 'undefined') {
          localStorage.setItem('access_token', data.access_token);
          localStorage.setItem('refresh_token', data.refresh_token);
        }
        
        setStatus('success');
        setMessage('Connexion réussie ! Redirection...');
        
        // Rediriger vers le dashboard après 1s
        setTimeout(() => {
          // Check if onboarding is completed
          const onboardingCompleted = data.user?.onboarding_completed;
          if (onboardingCompleted) {
            router.push('/dashboard');
          } else {
            router.push('/onboarding');
          }
        }, 1000);
      } else {
        setStatus('error');
        setMessage(data.detail || 'Lien invalide ou expiré');
      }
    } catch (error) {
      console.error('Verify error:', error);
      setStatus('error');
      setMessage('Erreur de connexion. Réessayez.');
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-background via-background to-secondary/5">
      <div className="absolute inset-0 bg-grid-white/[0.02] bg-[size:50px_50px]" />
      
      <div className="relative w-full max-w-md space-y-8 p-8 text-center">
        {status === 'loading' && (
          <>
            <Loader2 className="mx-auto h-16 w-16 animate-spin text-primary" />
            <h1 className="text-2xl font-bold">Vérification en cours...</h1>
            <p className="text-muted-foreground">Veuillez patienter</p>
          </>
        )}

        {status === 'success' && (
          <div className="space-y-6">
            <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/20">
              <svg className="h-12 w-12 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold">Connexion réussie !</h1>
            <p className="text-lg text-muted-foreground">{message}</p>
          </div>
        )}

        {status === 'error' && (
          <div className="space-y-6">
            <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/20">
              <svg className="h-12 w-12 text-red-600 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold">Erreur</h1>
            <p className="text-lg text-muted-foreground">{message}</p>
            <Button
              onClick={() => router.push('/login')}
              className="mt-4"
            >
              Retour à la connexion
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}

