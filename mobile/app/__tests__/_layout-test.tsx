import { render } from "@testing-library/react-native";
import { useFonts } from "expo-font";
import * as SplashScreen from "expo-splash-screen";
import React from "react";

import RootLayout from "../_layout";

// Mock the dependencies
jest.mock("expo-font", () => ({
  useFonts: jest.fn(),
}));

jest.mock("expo-splash-screen", () => ({
  preventAutoHideAsync: jest.fn(),
  hideAsync: jest.fn(),
}));

jest.mock("@/hooks/useColorScheme", () => ({
  useColorScheme: jest.fn(),
}));

jest.mock("expo-router", () => ({
  Stack: {
    Screen: ({ name, options }) => (
      <div data-name={name} data-options={JSON.stringify(options)} />
    ),
  },
}));

jest.mock("@react-navigation/native", () => ({
  DarkTheme: { colors: { background: "#000" } },
  DefaultTheme: { colors: { background: "#fff" } },
  ThemeProvider: ({ children }) => <div>{children}</div>,
}));

describe("RootLayout", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("prevents splash screen from auto-hiding", () => {
    // Mock useFonts to return [false]
    (useFonts as jest.Mock).mockReturnValue([false]);

    render(<RootLayout />);

    expect(SplashScreen.preventAutoHideAsync).toHaveBeenCalled();
  });

  it("returns null if fonts are not loaded", () => {
    // Mock useFonts to return [false]
    (useFonts as jest.Mock).mockReturnValue([false]);

    const { container } = render(<RootLayout />);

    // The component should return null
    expect(container.children.length).toBe(0);
  });

  it("hides splash screen when fonts are loaded", () => {
    // Mock useEffect to execute immediately
    jest.spyOn(React, "useEffect").mockImplementation((f) => f());

    // Mock useFonts to return [true]
    (useFonts as jest.Mock).mockReturnValue([true]);

    render(<RootLayout />);

    expect(SplashScreen.hideAsync).toHaveBeenCalled();
  });

  it("renders Stack screens with correct options", () => {
    // Mock useFonts to return [true]
    (useFonts as jest.Mock).mockReturnValue([true]);

    const { getAllByTestId } = render(<RootLayout />);

    // Check if all Stack.Screen components are rendered
    const screens = getAllByTestId(/data-name/);

    // Verify the screens have the correct names and options
    expect(
      screens.some((screen) => screen.props["data-name"] === "index")
    ).toBeTruthy();
    expect(
      screens.some((screen) => screen.props["data-name"] === "signup")
    ).toBeTruthy();
    expect(
      screens.some((screen) => screen.props["data-name"] === "(tabs)")
    ).toBeTruthy();
    expect(
      screens.some((screen) => screen.props["data-name"] === "+not-found")
    ).toBeTruthy();
  });
});
