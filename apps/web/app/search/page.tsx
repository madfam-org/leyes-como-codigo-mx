import SearchExperience from '@/components/SearchExperience';

export default function SearchPage() {
    return (
        <main className="min-h-screen bg-background py-12">
            <div className="container mx-auto px-4">
                <h1 className="text-4xl font-bold text-center mb-8 text-foreground tracking-tight">
                    Leyes Como Código <span className="text-primary">Buscador</span>
                </h1>
                <SearchExperience />
            </div>
        </main>
    );
}
