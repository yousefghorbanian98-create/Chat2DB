import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import Login from './Login';

const login = vi.fn();
const memberLogin = vi.fn();
vi.mock('../auth/useAuth', () => ({ useAuth: () => ({ login, memberLogin }) }));

describe('Login (dual-mode sign-in)', () => {
  beforeEach(() => {
    login.mockReset().mockResolvedValue(undefined);
    memberLogin.mockReset().mockResolvedValue(undefined);
  });

  it('defaults to staff mode and calls login', async () => {
    render(<Login />);
    expect(screen.getByText('ورود کارکنان — پین')).toBeTruthy();
    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'owner' } });
    fireEvent.change(screen.getByDisplayValue(''), { target: { value: '1111' } });
    fireEvent.click(screen.getByRole('button', { name: 'ورود' }));
    await waitFor(() => expect(login).toHaveBeenCalledWith('owner', '1111'));
  });

  it('member mode calls memberLogin with the membership code', async () => {
    render(<Login />);
    fireEvent.click(screen.getByTestId('mode-member'));
    expect(screen.getByText('ورود ورزشکار — کد عضویت و پین')).toBeTruthy();
    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'MP-DEMO-1' } });
    fireEvent.change(screen.getByDisplayValue(''), { target: { value: '1234' } });
    fireEvent.click(screen.getByRole('button', { name: 'ورود' }));
    await waitFor(() => expect(memberLogin).toHaveBeenCalledWith('MP-DEMO-1', '1234'));
  });

  it('blocks an empty submission', () => {
    render(<Login />);
    fireEvent.click(screen.getByRole('button', { name: 'ورود' }));
    expect(login).not.toHaveBeenCalled();
    expect(memberLogin).not.toHaveBeenCalled();
    expect(screen.getByRole('alert')).toBeTruthy();
  });
});
