import { renderHook } from '@testing-library/react-native';
import { useThemeColor } from '../useThemeColor';
import { useColorScheme } from '../useColorScheme';
import { Colors } from '@/constants/Colors';

// Mock the useColorScheme hook
jest.mock('../useColorScheme', () => ({
  useColorScheme: jest.fn(),
}));

describe('useThemeColor', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('returns the color from props if available for the current theme', () => {
    // Mock useColorScheme to return 'light'
    (useColorScheme as jest.Mock).mockReturnValue('light');

    const props = { light: '#CUSTOM_LIGHT', dark: '#CUSTOM_DARK' };
    const { result } = renderHook(() => useThemeColor(props, 'text'));

    expect(result.current).toBe('#CUSTOM_LIGHT');
  });

  it('returns the color from Colors if no prop is provided for the current theme', () => {
    // Mock useColorScheme to return 'dark'
    (useColorScheme as jest.Mock).mockReturnValue('dark');

    const props = {}; // No custom colors
    const { result } = renderHook(() => useThemeColor(props, 'text'));

    expect(result.current).toBe(Colors.dark.text);
  });

  it('defaults to light theme if useColorScheme returns null', () => {
    // Mock useColorScheme to return null
    (useColorScheme as jest.Mock).mockReturnValue(null);

    const props = { light: '#CUSTOM_LIGHT', dark: '#CUSTOM_DARK' };
    const { result } = renderHook(() => useThemeColor(props, 'text'));

    expect(result.current).toBe('#CUSTOM_LIGHT');
  });

  it('returns the correct color for different color names', () => {
    // Mock useColorScheme to return 'light'
    (useColorScheme as jest.Mock).mockReturnValue('light');

    // Test with 'background' color
    const { result: backgroundResult } = renderHook(() =>
      useThemeColor({}, 'background')
    );
    expect(backgroundResult.current).toBe(Colors.light.background);

    // Test with 'tint' color
    const { result: tintResult } = renderHook(() =>
      useThemeColor({}, 'tint')
    );
    expect(tintResult.current).toBe(Colors.light.tint);
  });
});
