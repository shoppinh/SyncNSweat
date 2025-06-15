// Centralized onboarding context (stub for expansion)
import { createContext, useContext, useState, ReactNode } from 'react';

interface OnboardingContextType {
  step: number;
  setStep: (step: number) => void;
}

const OnboardingContext = createContext<OnboardingContextType | undefined>(undefined);

export function OnboardingProvider({ children }: { children: ReactNode }) {
  const [step, setStep] = useState(0);
  return (
    <OnboardingContext.Provider value={{ step, setStep }}>
      {children}
    </OnboardingContext.Provider>
  );
}

export function useOnboarding() {
  const context = useContext(OnboardingContext);
  if (!context) throw new Error('useOnboarding must be used within OnboardingProvider');
  return context;
}
