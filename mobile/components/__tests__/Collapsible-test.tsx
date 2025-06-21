import * as React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { beforeEach, describe, expect, it, jest } from '@jest/globals';

import { Collapsible } from '../Collapsible';

// Mock the dependencies
jest.mock('@/hooks/useColorScheme', () => ({
  __esModule: true,
  default: jest.fn(),
  useColorScheme: jest.fn().mockReturnValue('light'),
}));

jest.mock('@/hooks/useThemeColor', () => ({
  useThemeColor: jest.fn().mockReturnValue('#FFFFFF'),
}));

jest.mock('@/components/ui/IconSymbol', () => ({
  IconSymbol: () => 'IconSymbol',
}));

describe('<Collapsible />', () => {
  it('renders with a title', () => {
    const { getByText } = render(
      <Collapsible title="Test Section">
        <div>Content</div>
      </Collapsible>
    );
    
    expect(getByText('Test Section')).toBeTruthy();
  });

  it('does not show content initially', () => {
    const { queryByText } = render(
      <Collapsible title="Test Section">
        <div>Hidden Content</div>
      </Collapsible>
    );
    
    expect(queryByText('Hidden Content')).toBeNull();
  });

  it('shows content when pressed', () => {
    const { getByText, queryByText } = render(
      <Collapsible title="Test Section">
        <div>Hidden Content</div>
      </Collapsible>
    );
    
    // Content should be hidden initially
    expect(queryByText('Hidden Content')).toBeNull();
    
    // Press the title to expand
    fireEvent.press(getByText('Test Section'));
    
    // Content should now be visible
    expect(queryByText('Hidden Content')).toBeTruthy();
  });

  it('toggles content visibility when pressed multiple times', () => {
    const { getByText, queryByText } = render(
      <Collapsible title="Test Section">
        <div>Toggle Content</div>
      </Collapsible>
    );
    
    // Initially hidden
    expect(queryByText('Toggle Content')).toBeNull();
    
    // First press - show content
    fireEvent.press(getByText('Test Section'));
    expect(queryByText('Toggle Content')).toBeTruthy();
    
    // Second press - hide content
    fireEvent.press(getByText('Test Section'));
    expect(queryByText('Toggle Content')).toBeNull();
  });
});
