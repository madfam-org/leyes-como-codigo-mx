'use client';

import { useState, useCallback, useSyncExternalStore } from 'react';

const SIZES = ['text-sm', 'text-base', 'text-lg'] as const;
type FontSize = (typeof SIZES)[number];
const STORAGE_KEY = 'preferred-font-size';

interface FontSizeControlProps {
    onChange: (size: FontSize) => void;
}

export type { FontSize };

function readStoredSize(): FontSize {
    if (typeof window === 'undefined') return 'text-base';
    const stored = localStorage.getItem(STORAGE_KEY) as FontSize | null;
    return stored && SIZES.includes(stored) ? stored : 'text-base';
}

export function FontSizeControl({ onChange }: FontSizeControlProps) {
    const subscribe = useCallback(() => () => {}, []);
    const size = useSyncExternalStore(subscribe, readStoredSize, () => 'text-base' as FontSize);
    const [, setTick] = useState(0);

    const handleChange = (newSize: FontSize) => {
        localStorage.setItem(STORAGE_KEY, newSize);
        setTick((t) => t + 1);
        onChange(newSize);
    };

    // Sync on first render (client only)
    if (typeof window !== 'undefined' && size !== 'text-base') {
        onChange(size);
    }

    return (
        <div className="inline-flex items-center rounded-md border border-border bg-muted/50 p-0.5" role="group" aria-label="Font size">
            <button
                onClick={() => handleChange('text-sm')}
                className={`px-2 py-1 text-xs rounded transition-colors ${
                    size === 'text-sm' ? 'bg-primary text-primary-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'
                }`}
                aria-label="Small text"
                aria-pressed={size === 'text-sm'}
            >
                A-
            </button>
            <button
                onClick={() => handleChange('text-base')}
                className={`px-2 py-1 text-sm rounded transition-colors ${
                    size === 'text-base' ? 'bg-primary text-primary-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'
                }`}
                aria-label="Normal text"
                aria-pressed={size === 'text-base'}
            >
                A
            </button>
            <button
                onClick={() => handleChange('text-lg')}
                className={`px-2 py-1 text-base rounded transition-colors ${
                    size === 'text-lg' ? 'bg-primary text-primary-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'
                }`}
                aria-label="Large text"
                aria-pressed={size === 'text-lg'}
            >
                A+
            </button>
        </div>
    );
}
