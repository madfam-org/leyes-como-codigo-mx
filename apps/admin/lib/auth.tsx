"use client";

import React from "react";

// Flag indicating whether real auth is available
let isAuthConfigured = false;

// Stub components used when @janua/nextjs is not installed
function StubJanuaProvider({ children }: { children: React.ReactNode }) {
    return (
        <>
            <div className="bg-destructive/10 border-b border-destructive/20 px-4 py-2 text-center text-sm text-destructive">
                Authentication is not configured. Set up @janua/nextjs for production use.
            </div>
            {children}
        </>
    );
}

function StubUserButton() {
    return (
        <div className="h-8 w-8 rounded-full bg-muted flex items-center justify-center text-xs font-medium text-muted-foreground">
            ?
        </div>
    );
}

function StubSignInForm() {
    return (
        <div className="rounded-lg border border-destructive/20 bg-card p-6 text-center text-sm text-muted-foreground">
            <p className="font-medium text-destructive mb-2">Authentication Not Configured</p>
            <p>Install and configure <code className="bg-muted px-1 rounded">@janua/nextjs</code> to enable authentication for the admin console.</p>
        </div>
    );
}

// Try to load real Janua; fall back to stubs if unavailable
let JanuaProvider: React.ComponentType<{ children: React.ReactNode }> = StubJanuaProvider;
let UserButton: React.ComponentType<{ showName?: boolean; afterSignOutUrl?: string }> = StubUserButton;
let SignInForm: React.ComponentType<{ redirectUrl?: string }> = StubSignInForm;

try {
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    const janua = require("@janua/nextjs");
    if (janua.JanuaProvider) JanuaProvider = janua.JanuaProvider;
    if (janua.UserButton) UserButton = janua.UserButton;
    if (janua.SignInForm) SignInForm = janua.SignInForm;
    isAuthConfigured = true;
} catch {
    // @janua/nextjs not installed — stubs are already set
}

export { JanuaProvider, UserButton, SignInForm, isAuthConfigured };
