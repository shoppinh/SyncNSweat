import { describe, expect, it, jest } from '@jest/globals';
import { render } from '@testing-library/react-native';
import * as React from 'react';

import { ThemedView } from '../ThemedView';

// Mock the useThemeColor hook
jest.mock('@/hooks/useThemeColor', () => ({
  useThemeColor: jest.fn().mockReturnValue('#FFFFFF'),
}));

describe('<ThemedView /> basic test', () => {
  it('renders correctly', () => {
    const { getByTestId } = render(
      <ThemedView testID="themed-view" />
    );
    
    expect(getByTestId('themed-view')).toBeTruthy();
  });
});
