import { redirect } from "next/navigation";

interface OnboardingDefaultProps {
  params: Promise<{ locale: string }>;
}

export default async function OnboardingDefault({ params }: OnboardingDefaultProps) {
  const { locale } = await params;
  redirect(`/${locale}/onboarding/welcome`);
}

