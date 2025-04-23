import { useThemeColor } from '../useThemeColor';
import { Colors } from '@/constants/Colors';

// Mock the useColorScheme hook
jest.mock('../useColorScheme', () => ({
  useColorScheme: jest.fn().mockReturnValue('light'),
}));

describe('useThemeColor basic test', () => {
  it('returns the color from Colors if no prop is provided', () => {
    const result = useThemeColor({}, 'text');
    expect(result).toBe(Colors.light.text);
  });
});
