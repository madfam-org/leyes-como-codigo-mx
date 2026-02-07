'use client';

import { useState, useEffect } from 'react';

export function ReadingProgressBar() {
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        const handleScroll = () => {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            if (docHeight > 0) {
                setProgress(Math.min((scrollTop / docHeight) * 100, 100));
            }
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    if (progress === 0) return null;

    return (
        <div
            className="fixed top-0 left-0 z-50 h-[3px] bg-primary transition-[width] duration-75"
            style={{ width: `${progress}%`, willChange: 'width' }}
            role="progressbar"
            aria-label="Progreso de lectura"
            aria-valuenow={Math.round(progress)}
            aria-valuemin={0}
            aria-valuemax={100}
        />
    );
}
