import { describe, expect, it, jest } from '@jest/globals';
import { render } from '@testing-library/react-native';
import * as React from 'react';
import renderer from 'react-test-renderer';

import { ThemedView } from '../ThemedView';

// Mock the useThemeColor hook
jest.mock('@/hooks/useThemeColor', () => ({
  useThemeColor: jest.fn().mockReturnValue('#FFFFFF'),
}));

describe('<ThemedView />', () => {
  it('renders correctly', () => {
    const tree = renderer.create(<ThemedView />).toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('applies custom styles', () => {
    const { getByTestId } = render(
      <ThemedView style={{ padding: 20 }} testID="themed-view" />
    );
    
    const view = getByTestId('themed-view');
    expect(view).toHaveStyle({ backgroundColor: '#FFFFFF', padding: 20 });
  });

  it('passes other props to the underlying View', () => {
    const { getByTestId } = render(
      <ThemedView testID="themed-view" accessibilityLabel="Test View" />
    );
    
    const view = getByTestId('themed-view');
    expect(view.props.accessibilityLabel).toBe('Test View');
  });
});
