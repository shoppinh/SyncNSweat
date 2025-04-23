import { Colors } from "@/constants/Colors";
import { describe, expect, it, jest } from "@jest/globals";
import { useThemeColor } from "../useThemeColor";

// Mock the useColorScheme hook
jest.mock("../useColorScheme", () => ({
  useColorScheme: jest.fn().mockReturnValue("light"),
}));

describe("useThemeColor basic test", () => {
  it("returns the color from Colors if no prop is provided", () => {
    const result = useThemeColor({}, "text");
    expect(result).toBe(Colors.light.text);
  });
});
