"use client";

import { useQuery } from "@tanstack/react-query";
import { useTranslations } from "next-intl";
import { Sparkles, Phone, Calendar, Plus, ExternalLink } from "lucide-react";
import Link from "next/link";

import { GlassCard } from "@/components/ui/glass-card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";

interface VapiAssistant {
  id: string;
  name: string;
  model?: {
    model?: string;
    provider?: string;
  };
  voice?: {
    provider?: string;
    voiceId?: string;
  };
  firstMessage?: string;
  createdAt: string;
  updatedAt: string;
}

interface AssistantsResponse {
  success: boolean;
  assistants: VapiAssistant[];
}

async function fetchAssistants(): Promise<AssistantsResponse> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch("/api/assistants", {
    method: "GET",
    headers,
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.error ?? "Failed to load assistants");
  }

  return response.json() as Promise<AssistantsResponse>;
}

export function AssistantsList() {
  const t = useTranslations("assistantsPage");

  const assistantsQuery = useQuery<AssistantsResponse>({
    queryKey: ["assistants"],
    queryFn: fetchAssistants,
    staleTime: 30_000,
  });

  if (assistantsQuery.isLoading) {
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold">Vos Assistants</h2>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <GlassCard key={i} className="p-6">
              <Skeleton className="h-6 w-32 mb-4" />
              <Skeleton className="h-4 w-full mb-2" />
              <Skeleton className="h-4 w-3/4" />
            </GlassCard>
          ))}
        </div>
      </div>
    );
  }

  if (assistantsQuery.isError) {
    return (
      <GlassCard className="p-6">
        <div className="text-center space-y-2">
          <p className="text-destructive">
            ❌ Erreur lors du chargement des assistants
          </p>
          <p className="text-sm text-muted-foreground">
            {assistantsQuery.error instanceof Error
              ? assistantsQuery.error.message
              : "Erreur inconnue"}
          </p>
        </div>
      </GlassCard>
    );
  }

  const assistants = assistantsQuery.data?.assistants ?? [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <h2 className="text-2xl font-semibold tracking-tight">
            Vos Assistants IA
          </h2>
          <p className="text-sm text-muted-foreground">
            {assistants.length === 0
              ? "Aucun assistant pour le moment"
              : `${assistants.length} assistant${assistants.length > 1 ? "s" : ""} configuré${assistants.length > 1 ? "s" : ""}`}
          </p>
        </div>
        <Button asChild size="lg">
          <Link href="/fr/app/assistants/new">
            <Plus className="h-4 w-4 mr-2" />
            Créer un assistant
          </Link>
        </Button>
      </div>

      {assistants.length === 0 ? (
        <GlassCard className="p-12">
          <div className="text-center space-y-4 max-w-md mx-auto">
            <div className="mx-auto w-16 h-16 rounded-full bg-brand-500/10 flex items-center justify-center">
              <Sparkles className="h-8 w-8 text-brand-500" />
            </div>
            <div className="space-y-2">
              <h3 className="text-xl font-semibold">
                Créez votre premier assistant
              </h3>
              <p className="text-muted-foreground">
                Configurez un assistant IA pour répondre aux appels, prendre des rendez-vous et bien plus encore.
              </p>
            </div>
            <Button asChild size="lg" className="mt-4">
              <Link href="/fr/app/assistants/new">
                <Plus className="h-4 w-4 mr-2" />
                Commencer
              </Link>
            </Button>
          </div>
        </GlassCard>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {assistants.map((assistant) => (
            <GlassCard
              key={assistant.id}
              className="p-6 space-y-4 hover:border-brand-500/50 transition-colors cursor-pointer group"
            >
              <div className="flex items-start justify-between">
                <div className="space-y-1 flex-1">
                  <h3 className="font-semibold text-lg group-hover:text-brand-500 transition-colors">
                    {assistant.name}
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {assistant.model?.provider && (
                      <Badge variant="neutral" className="text-xs">
                        {assistant.model.provider === "openai" && "🤖"}
                        {assistant.model.provider === "anthropic" && "🧠"}
                        {assistant.model.provider === "google" && "🔍"}
                        {assistant.model.model ?? assistant.model.provider}
                      </Badge>
                    )}
                    {assistant.voice?.provider && (
                      <Badge variant="neutral" className="text-xs">
                        🎙️ {assistant.voice.voiceId ?? assistant.voice.provider}
                      </Badge>
                    )}
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  className="opacity-0 group-hover:opacity-100 transition-opacity"
                  asChild
                >
                  <Link href={`/fr/app/assistants/${assistant.id}`}>
                    <ExternalLink className="h-4 w-4" />
                  </Link>
                </Button>
              </div>

              {assistant.firstMessage && (
                <p className="text-sm text-muted-foreground line-clamp-2">
                  {assistant.firstMessage}
                </p>
              )}

              <div className="flex items-center gap-4 pt-4 border-t text-xs text-muted-foreground">
                <div className="flex items-center gap-1">
                  <Calendar className="h-3 w-3" />
                  {new Date(assistant.createdAt).toLocaleDateString("fr-FR")}
                </div>
              </div>

              <div className="flex gap-2">
                <Button asChild variant="outline" size="sm" className="flex-1">
                  <Link href={`/fr/app/assistants/${assistant.id}`}>
                    Voir
                  </Link>
                </Button>
                <Button asChild variant="default" size="sm" className="flex-1">
                  <Link href={`/fr/app/assistants/${assistant.id}/edit`}>
                    Modifier
                  </Link>
                </Button>
              </div>
            </GlassCard>
          ))}
        </div>
      )}
    </div>
  );
}
