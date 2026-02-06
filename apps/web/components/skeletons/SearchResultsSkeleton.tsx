export function SearchResultsSkeleton() {
    return (
        <div className="animate-pulse space-y-4">
            <div className="h-4 w-40 rounded bg-muted mb-6" />
            {[...Array(5)].map((_, i) => (
                <div key={i} className="rounded-lg border bg-card p-6 space-y-3">
                    <div className="flex gap-2">
                        <div className="h-5 w-36 rounded bg-muted" />
                        <div className="h-5 w-16 rounded bg-muted" />
                    </div>
                    <div className="h-4 w-full rounded bg-muted" />
                    <div className="h-4 w-4/5 rounded bg-muted" />
                    <div className="h-3 w-32 rounded bg-muted" />
                </div>
            ))}
        </div>
    );
}
