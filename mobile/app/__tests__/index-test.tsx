import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { Alert } from 'react-native';
import { router } from 'expo-router';
import { beforeEach, describe, expect, it, jest } from '@jest/globals';

import LoginScreen from '../index';

// Mock expo-router
jest.mock('expo-router', () => ({
  router: {
    replace: jest.fn(),
  },
}));

// Mock Alert
jest.mock('react-native/Libraries/Alert/Alert', () => ({
  alert: jest.fn(),
}));

describe('LoginScreen', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders correctly', () => {
    const { getByText, getByPlaceholderText } = render(<LoginScreen />);
    
    expect(getByText('Sync & Sweat')).toBeTruthy();
    expect(getByText('Login to your account')).toBeTruthy();
    expect(getByPlaceholderText('Email')).toBeTruthy();
    expect(getByPlaceholderText('Password')).toBeTruthy();
    expect(getByText('Login')).toBeTruthy();
    expect(getByText("Don't have an account? Sign up")).toBeTruthy();
  });

  it('updates email and password state on input', () => {
    const { getByPlaceholderText } = render(<LoginScreen />);
    
    const emailInput = getByPlaceholderText('Email');
    const passwordInput = getByPlaceholderText('Password');
    
    fireEvent.changeText(emailInput, 'test@example.com');
    fireEvent.changeText(passwordInput, 'password123');
    
    expect(emailInput.props.value).toBe('test@example.com');
    expect(passwordInput.props.value).toBe('password123');
  });

  it('shows an alert when trying to login with empty fields', () => {
    const { getByText } = render(<LoginScreen />);
    
    // Try to login without entering email and password
    fireEvent.press(getByText('Login'));
    
    expect(Alert.alert).toHaveBeenCalledWith('Error', 'Please enter email and password');
    expect(router.replace).not.toHaveBeenCalled();
  });

  it('navigates to main app when login is successful', async () => {
    const { getByText, getByPlaceholderText } = render(<LoginScreen />);
    
    // Enter email and password
    fireEvent.changeText(getByPlaceholderText('Email'), 'test@example.com');
    fireEvent.changeText(getByPlaceholderText('Password'), 'password123');
    
    // Press login button
    fireEvent.press(getByText('Login'));
    
    await waitFor(() => {
      expect(router.replace).toHaveBeenCalledWith('/(tabs)/index');
    });
    
    expect(Alert.alert).not.toHaveBeenCalled();
  });

  it('navigates to signup screen when signup link is pressed', () => {
    const pushMock = jest.fn();
    router.push = pushMock;
    
    const { getByText } = render(<LoginScreen />);
    
    fireEvent.press(getByText("Don't have an account? Sign up"));
    
    expect(pushMock).toHaveBeenCalledWith('/signup');
  });
});
