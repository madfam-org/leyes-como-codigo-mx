/**
 * Shared color maps and style utilities for admin components.
 */

export const statusColors: Record<string, string> = {
    planned: 'bg-muted text-muted-foreground',
    in_progress: 'bg-primary/10 text-primary',
    blocked: 'bg-destructive/10 text-destructive',
    completed: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
    deferred: 'bg-muted text-muted-foreground',
};

export const statusBorderColors: Record<string, string> = {
    healthy: 'border-green-500',
    degraded: 'border-yellow-500',
    unhealthy: 'border-red-500',
    unknown: 'border-muted',
};

export const statusBadgeVariants: Record<string, 'default' | 'secondary' | 'destructive' | 'outline'> = {
    healthy: 'default',
    degraded: 'secondary',
    unhealthy: 'destructive',
    unknown: 'outline',
};

export const effortColors: Record<string, string> = {
    low: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
    medium: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400',
    high: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
};

export const categoryColors: Record<string, string> = {
    scraping: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
    parsing: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
    indexing: 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400',
    infrastructure: 'bg-gray-100 text-gray-700 dark:bg-gray-900/30 dark:text-gray-400',
};

export const coverageColors = {
    high: 'bg-green-500',
    medium: 'bg-yellow-500',
    low: 'bg-orange-500',
    none: 'bg-muted',
} as const;

export function getCoverageColor(pct: number): string {
    if (pct >= 90) return coverageColors.high;
    if (pct >= 50) return coverageColors.medium;
    if (pct > 0) return coverageColors.low;
    return coverageColors.none;
}
