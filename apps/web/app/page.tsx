import TaxForm from "../components/TaxForm";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-stone-50 via-white to-crimson-50 flex flex-col items-center justify-center p-4">
      <div className="text-center mb-8">
        <h1 className="text-5xl font-bold text-stone-900 tracking-tight sm:text-6xl">
          Leyes Como Código <span className="text-crimson-600">México</span>
        </h1>
        <p className="mt-4 text-xl text-stone-600 max-w-2xl">
          Un motor de reglas fiscales abierto, verificable y ejecutable.
          <br />
          <span className="text-forest-600 font-semibold">Legislación Federal en formato machine-readable</span>
        </p>

        <div className="mt-8 flex gap-4 justify-center">
          <Button asChild size="lg" className="px-8 py-6 text-lg bg-crimson-600 hover:bg-crimson-700 shadow-lg hover:shadow-xl transition-all hover:scale-105 active:scale-95">
            <Link href="/laws">
              📚 Explorar Leyes Federales
            </Link>
          </Button>
        </div>
      </div>

      <div className="w-full max-w-lg">
        <TaxForm />
      </div>

      <footer className="mt-12 text-sm text-stone-500">
        <p>Powered by <span className="font-semibold text-stone-700">OpenFisca</span> & <span className="font-semibold text-stone-700">Catala</span></p>
      </footer>
    </main>
  );
}

