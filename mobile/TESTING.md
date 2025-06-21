# Testing Guide for Sync & Sweat Mobile App

This document provides comprehensive instructions on how to run and write tests for the Sync & Sweat mobile application.

## Testing Framework

The mobile app uses the following testing tools:

- **Jest**: The main testing framework
- **React Test Renderer**: For snapshot testing
- **React Testing Library**: For component testing
- **Testing Library Jest Native**: For native component assertions

## Running Tests

### Basic Test Commands

```bash
# Run all tests
npm test

# Run tests in watch mode (recommended during development)
npm test -- --watch

# Run tests with coverage report
npm test -- --coverage

# Run a specific test file
npm test -- components/__tests__/ThemedText-test.tsx

# Run tests matching a specific pattern
npm test -- -t "ThemedView"
```

### Test Coverage

The coverage report will be generated in the `coverage` directory. Open `coverage/lcov-report/index.html` in a browser to view the detailed report.

## Test Structure

Tests are organized in `__tests__` directories:

- `components/__tests__/` - Tests for UI components
- `hooks/__tests__/` - Tests for custom hooks
- `app/__tests__/` - Tests for screens and navigation

## Writing Tests

### Component Tests

Component tests should verify:
1. The component renders correctly
2. Props are applied correctly
3. User interactions work as expected
4. State changes correctly

Example:

```tsx
import * as React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { MyComponent } from '../MyComponent';

describe('<MyComponent />', () => {
  it('renders correctly', () => {
    const { getByText } = render(<MyComponent title="Test" />);
    expect(getByText('Test')).toBeTruthy();
  });

  it('handles press events', () => {
    const onPressMock = jest.fn();
    const { getByText } = render(
      <MyComponent title="Press Me" onPress={onPressMock} />
    );
    
    fireEvent.press(getByText('Press Me'));
    expect(onPressMock).toHaveBeenCalled();
  });
});
```

### Hook Tests

Hook tests should verify:
1. The hook returns the expected values
2. The hook responds correctly to parameter changes
3. Side effects work as expected

Example:

```tsx
import { renderHook, act } from '@testing-library/react-hooks';
import { useMyHook } from '../useMyHook';

describe('useMyHook', () => {
  it('returns the initial value', () => {
    const { result } = renderHook(() => useMyHook('initial'));
    expect(result.current.value).toBe('initial');
  });

  it('updates the value when update is called', () => {
    const { result } = renderHook(() => useMyHook('initial'));
    
    act(() => {
      result.current.update('updated');
    });
    
    expect(result.current.value).toBe('updated');
  });
});
```

### Screen Tests

Screen tests should verify:
1. The screen renders correctly
2. Navigation works as expected
3. User interactions work as expected
4. Data is displayed correctly

Example:

```tsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { router } from 'expo-router';
import HomeScreen from '../HomeScreen';

// Mock expo-router
jest.mock('expo-router', () => ({
  router: {
    push: jest.fn(),
  },
}));

describe('HomeScreen', () => {
  it('renders correctly', () => {
    const { getByText } = render(<HomeScreen />);
    expect(getByText('Welcome')).toBeTruthy();
  });

  it('navigates to details screen when button is pressed', () => {
    const { getByText } = render(<HomeScreen />);
    
    fireEvent.press(getByText('View Details'));
    
    expect(router.push).toHaveBeenCalledWith('/details');
  });
});
```

## Mocking

### Mocking External Modules

For external modules, create a mock in the `__mocks__` directory or use Jest's `jest.mock()`:

```tsx
// Mock expo-router
jest.mock('expo-router', () => ({
  router: {
    push: jest.fn(),
    replace: jest.fn(),
  },
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
  }),
}));
```

### Mocking Hooks

For custom hooks, use Jest's `jest.mock()`:

```tsx
jest.mock('@/hooks/useThemeColor', () => ({
  useThemeColor: jest.fn().mockReturnValue('#FFFFFF'),
}));
```

## Troubleshooting

### Common Issues

1. **Test fails with "Unable to find node on an unmounted component"**
   - This usually happens when you're trying to interact with a component that has been unmounted. Make sure you're not unmounting the component before the test is complete.

2. **Test fails with "Element not found"**
   - Check if the element is actually rendered. You might need to use `queryByText` instead of `getByText` if the element might not be present.

3. **Snapshot test fails after a UI change**
   - If the UI change is intentional, update the snapshot with `npm test -- -u`.

4. **Test fails with "Cannot read property 'X' of undefined"**
   - Check if you're properly mocking all dependencies and that the component is receiving all required props.

### Debugging Tests

To debug tests, you can use:

```tsx
console.log(prettyDOM(container)); // Print the DOM
debug(); // From React Testing Library
```

Or run Jest in debug mode:

```bash
node --inspect-brk node_modules/.bin/jest --runInBand
```

Then open Chrome DevTools and navigate to chrome://inspect to connect to the debugger.

## Continuous Integration

Tests are automatically run in the CI pipeline defined in `.github/workflows/frontend.yml`. Make sure all tests pass before submitting a pull request.
