import { describe, expect, it, jest } from '@jest/globals';
import { render } from '@testing-library/react-native';
import * as React from 'react';
import renderer from 'react-test-renderer';

import { IconSymbol } from '../ui/IconSymbol';

// Mock MaterialIcons
jest.mock('@expo/vector-icons/MaterialIcons', () => 'MaterialIcons');

describe('<IconSymbol />', () => {
  it('renders correctly with required props', () => {
    const tree = renderer.create(
      <IconSymbol name="house.fill" color="#000000" />
    ).toJSON();
    
    expect(tree).toMatchSnapshot();
  });

  it('applies custom size', () => {
    const { getByTestId } = render(
      <IconSymbol 
        name="house.fill" 
        color="#000000" 
        size={32} 
        testId="icon-symbol"
      />
    );
    
    const icon = getByTestId('icon-symbol');
    expect(icon.props.size).toBe(32);
  });

  it('applies custom style', () => {
    const customStyle = { margin: 10 };
    
    const { getByTestId } = render(
      <IconSymbol 
        name="house.fill" 
        color="#000000" 
        style={customStyle} 
        testId="icon-symbol"
      />
    );
    
    const icon = getByTestId('icon-symbol');
    expect(icon.props.style).toEqual(customStyle);
  });

  it('maps SFSymbol names to MaterialIcons names', () => {
    const { getByTestId } = render(
      <IconSymbol 
        name="house.fill" 
        color="#000000" 
        testId="icon-symbol"
      />
    );
    
    const icon = getByTestId('icon-symbol');
    // house.fill should map to 'home' for MaterialIcons
    expect(icon.props.name).toBe('home');
  });
});
