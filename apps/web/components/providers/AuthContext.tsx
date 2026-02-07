'use client';

import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';

export type UserTier = 'anon' | 'free' | 'premium';

interface AuthState {
    isAuthenticated: boolean;
    tier: UserTier;
    loginUrl: string;
}

const DEFAULT_LOGIN_URL = process.env.NEXT_PUBLIC_JANUA_LOGIN_URL || '/auth/login';

const defaultState: AuthState = {
    isAuthenticated: false,
    tier: 'anon',
    loginUrl: DEFAULT_LOGIN_URL,
};

const AuthContext = createContext<AuthState>(defaultState);

/**
 * Lightweight auth provider that checks for a Janua JWT in cookies/localStorage.
 * Does NOT manage the auth flow — Janua handles that.
 * Used by ExportDropdown to conditionally show format access.
 */
export function AuthProvider({ children }: { children: ReactNode }) {
    const [state, setState] = useState<AuthState>(defaultState);

    useEffect(() => {
        // Check for JWT in cookie or localStorage
        const token = getToken();
        if (!token) {
            setState(defaultState);
            return;
        }

        // Decode payload (no verification — server handles that)
        const claims = decodeJwtPayload(token);
        if (!claims) {
            setState(defaultState);
            return;
        }

        const tier = (claims.tier || claims.plan || 'free') as UserTier;
        const validTier = ['anon', 'free', 'premium'].includes(tier) ? tier : 'free';

        setState({
            isAuthenticated: true,
            tier: validTier as UserTier,
            loginUrl: DEFAULT_LOGIN_URL,
        });
    }, []);

    return <AuthContext.Provider value={state}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
    return useContext(AuthContext);
}

function getToken(): string | null {
    // Check cookie first
    if (typeof document !== 'undefined') {
        const match = document.cookie.match(/(?:^|;\s*)janua_token=([^;]*)/);
        if (match) return decodeURIComponent(match[1]);
    }
    // Fall back to localStorage
    if (typeof localStorage !== 'undefined') {
        return localStorage.getItem('janua_token');
    }
    return null;
}

function decodeJwtPayload(token: string): Record<string, unknown> | null {
    try {
        const parts = token.split('.');
        if (parts.length !== 3) return null;
        const payload = atob(parts[1].replace(/-/g, '+').replace(/_/g, '/'));
        return JSON.parse(payload);
    } catch {
        return null;
    }
}
