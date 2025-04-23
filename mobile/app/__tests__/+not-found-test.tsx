import { describe, expect, it, jest } from "@jest/globals";
import { render } from "@testing-library/react-native";
import React from "react";

import NotFoundScreen from "../+not-found";

// Mock expo-router
jest.mock("expo-router", () => ({
  Link: ({ href, style, children, onPress }: any) => (
    <div href={href} style={style} onPress={onPress}>
      {children}
    </div>
  ),
  Stack: {
    Screen: ({ options }) => <div>{JSON.stringify(options)}</div>,
  },
}));

// Mock the ThemedText and ThemedView components
jest.mock("@/components/ThemedText", () => ({
  ThemedText: ({ children, type }) => <div data-type={type}>{children}</div>,
}));

jest.mock("@/components/ThemedView", () => ({
  ThemedView: ({ children, style }) => <div style={style}>{children}</div>,
}));

describe("NotFoundScreen", () => {
  it("renders correctly", () => {
    const { getByText } = render(<NotFoundScreen />);

    expect(getByText("This screen doesn't exist.")).toBeTruthy();
    expect(getByText("Go to home screen!")).toBeTruthy();
  });

  it("has a link to the home screen", () => {
    const { getByText } = render(<NotFoundScreen />);

    const link = getByText("Go to home screen!");
    expect(link.props.href).toBe("/");
  });

  it("sets the correct screen title", () => {
    const { getByText } = render(<NotFoundScreen />);

    // Check if the Stack.Screen has the correct title option
    expect(getByText('{"title":"Oops!"}')).toBeTruthy();
  });
});
