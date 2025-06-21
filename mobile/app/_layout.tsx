import AsyncStorage from "@react-native-async-storage/async-storage";
import {
  DarkTheme,
  DefaultTheme,
  ThemeProvider,
} from "@react-navigation/native";
import { useFonts } from "expo-font";
import { Stack } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import { StatusBar } from "expo-status-bar";
import { useEffect, useState } from "react";
import "react-native-reanimated";

import { AuthProvider } from "../contexts/AuthContext";
import { OnboardingProvider } from "../contexts/OnboardingContext";
import { useColorScheme } from "../hooks/useColorScheme";

// Prevent the splash screen from auto-hiding before asset loading is complete.
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const [loaded] = useFonts({
    SpaceMono: require("../assets/fonts/SpaceMono-Regular.ttf"),
  });
  const [initialRoute, setInitialRoute] = useState<string | null>(null);

  useEffect(() => {
    async function checkOnboardingStatus() {
      try {
        const onboardingCompleted = await AsyncStorage.getItem(
          "onboardingCompleted"
        );
        setInitialRoute(
          onboardingCompleted === "true" ? "index" : "onboarding"
        );
      } catch (error) {
        console.error("Error checking onboarding status:", error);
        setInitialRoute("onboarding");
      }
    }

    if (loaded) {
      checkOnboardingStatus();
      SplashScreen.hideAsync();
    }
  }, [loaded]);

  if (!loaded || initialRoute === null) {
    return null;
  }

  return (
    <AuthProvider>
      <OnboardingProvider>
        <ThemeProvider
          value={colorScheme === "dark" ? DarkTheme : DefaultTheme}
        >
          {initialRoute === "onboarding" ? (
            // Show only the onboarding stack when needed
            <Stack
              initialRouteName="onboarding"
              screenOptions={{ headerShown: false }}
            >
              <Stack.Screen
                name="onboarding"
                options={{
                  headerShown: false,
                  headerTitle: "",
                }}
              />
            </Stack>
          ) : (
            // Show the main app stack
            <Stack
              initialRouteName="login"
              screenOptions={{ headerShown: false }}
            >
              <Stack.Screen name="login" />
              <Stack.Screen name="signup" />
              <Stack.Screen name="(tabs)" />
              <Stack.Screen name="+not-found" />
            </Stack>
          )}
          <StatusBar style="auto" />
        </ThemeProvider>
      </OnboardingProvider>
    </AuthProvider>
  );
}
