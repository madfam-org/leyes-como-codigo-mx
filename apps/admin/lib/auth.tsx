"use client";

import React from "react";

// Stub components used when @janua/nextjs is not installed (e.g. CI builds)
function StubJanuaProvider({ children }: { children: React.ReactNode }) {
    return <>{children}</>;
}

function StubUserButton() {
    return (
        <div className="h-8 w-8 rounded-full bg-muted flex items-center justify-center text-xs font-medium text-muted-foreground">
            A
        </div>
    );
}

function StubSignInForm() {
    return (
        <div className="rounded-lg border bg-card p-6 text-center text-sm text-muted-foreground">
            Authentication is not configured. Set up @janua/nextjs for production.
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
} catch {
    // @janua/nextjs not installed — stubs are already set
}

export { JanuaProvider, UserButton, SignInForm };
