import { afterEach, describe, expect, it, jest } from '@jest/globals';
import { fireEvent, render } from '@testing-library/react-native';
import { openBrowserAsync } from 'expo-web-browser';
import * as React from 'react';
import { Platform } from 'react-native';

import { ExternalLink } from '../ExternalLink';

// Mock the expo-web-browser module
jest.mock('expo-web-browser', () => ({
  openBrowserAsync: jest.fn(),
}));

// Mock the Platform module
const originalPlatform = Platform.OS;

describe('<ExternalLink />', () => {
  afterEach(() => {
    jest.clearAllMocks();
    // Reset Platform.OS to its original value
    Platform.OS = originalPlatform;
  });

  it('renders correctly with children', () => {
    const { getByText } = render(
      <ExternalLink href="https://example.com">Test Link</ExternalLink>
    );
    
    expect(getByText('Test Link')).toBeTruthy();
  });

  it('opens the link in an in-app browser on native platforms', () => {
    // Mock Platform.OS to be 'ios'
    Platform.OS = 'ios';
    
    const { getByText } = render(
      <ExternalLink href="https://example.com">Test Link</ExternalLink>
    );
    
    fireEvent.press(getByText('Test Link'));
    
    expect(openBrowserAsync).toHaveBeenCalledWith('https://example.com');
  });

  it('does not call openBrowserAsync on web platform', () => {
    // Mock Platform.OS to be 'web'
    Platform.OS = 'web';
    
    const { getByText } = render(
      <ExternalLink href="https://example.com">Test Link</ExternalLink>
    );
    
    fireEvent.press(getByText('Test Link'));
    
    expect(openBrowserAsync).not.toHaveBeenCalled();
  });
});
