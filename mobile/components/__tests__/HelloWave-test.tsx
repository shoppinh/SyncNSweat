import * as React from 'react';
import { render } from '@testing-library/react-native';
import renderer from 'react-test-renderer';

import { HelloWave } from '../HelloWave';

// Mock react-native-reanimated
jest.mock('react-native-reanimated', () => {
  const Reanimated = require('react-native-reanimated/mock');
  // The mock for `call` immediately calls the callback which is incorrect
  // So we override it with a no-op
  Reanimated.default.call = () => {};
  return Reanimated;
});

// Mock the useThemeColor hook
jest.mock('@/hooks/useThemeColor', () => ({
  useThemeColor: jest.fn().mockReturnValue('#000000'),
}));

describe('<HelloWave />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(<HelloWave />).toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('contains the wave emoji', () => {
    const { getByText } = render(<HelloWave />);
    expect(getByText('👋')).toBeTruthy();
  });

  it('starts the animation on mount', () => {
    // Create a spy on useEffect
    const useEffectSpy = jest.spyOn(React, 'useEffect');
    
    render(<HelloWave />);
    
    // Verify useEffect was called
    expect(useEffectSpy).toHaveBeenCalled();
    
    // Clean up
    useEffectSpy.mockRestore();
  });
});
