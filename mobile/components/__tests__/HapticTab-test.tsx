import * as React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import * as Haptics from 'expo-haptics';
import { beforeEach, describe, expect, it, jest } from '@jest/globals';

import { HapticTab } from '../HapticTab';

// Mock expo-haptics
jest.mock('expo-haptics', () => ({
  impactAsync: jest.fn(),
  ImpactFeedbackStyle: {
    Light: 'light',
    Medium: 'medium',
    Heavy: 'heavy',
  },
}));

describe('<HapticTab />', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
  });

  it('renders correctly with children', () => {
    const { getByTestId } = render(
      <HapticTab testID="haptic-tab">
        <div>Tab Content</div>
      </HapticTab>
    );
    
    expect(getByTestId('haptic-tab')).toBeTruthy();
  });

  it('triggers haptic feedback on iOS when pressed', () => {
    // Mock process.env.EXPO_OS to be 'ios'
    process.env.EXPO_OS = 'ios';
    
    const { getByTestId } = render(
      <HapticTab testID="haptic-tab">
        <div>Tab Content</div>
      </HapticTab>
    );
    
    fireEvent(getByTestId('haptic-tab'), 'pressIn');
    
    expect(Haptics.impactAsync).toHaveBeenCalledWith(Haptics.ImpactFeedbackStyle.Light);
  });

  it('does not trigger haptic feedback on Android when pressed', () => {
    // Mock process.env.EXPO_OS to be 'android'
    process.env.EXPO_OS = 'android';
    
    const { getByTestId } = render(
      <HapticTab testID="haptic-tab">
        <div>Tab Content</div>
      </HapticTab>
    );
    
    fireEvent(getByTestId('haptic-tab'), 'pressIn');
    
    expect(Haptics.impactAsync).not.toHaveBeenCalled();
  });

  it('calls the original onPressIn handler if provided', () => {
    const mockOnPressIn = jest.fn();
    
    const { getByTestId } = render(
      <HapticTab testID="haptic-tab" onPressIn={mockOnPressIn}>
        <div>Tab Content</div>
      </HapticTab>
    );
    
    fireEvent(getByTestId('haptic-tab'), 'pressIn');
    
    expect(mockOnPressIn).toHaveBeenCalled();
  });
});
