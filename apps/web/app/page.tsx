import TaxForm from "../components/TaxForm";
import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight sm:text-5xl">
          Leyes Como Código <span className="text-indigo-600">México</span>
        </h1>
        <p className="mt-4 text-lg text-gray-600">
          Un motor de reglas fiscales abierto, verificable y ejecutable.
        </p>

        <div className="mt-6 flex gap-4 justify-center">
          <Link
            href="/laws"
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors shadow-lg"
          >
            📚 Explorar Leyes Federales
          </Link>
        </div>
      </div>

      <div className="w-full max-w-lg">
        <TaxForm />
      </div>

      <footer className="mt-12 text-sm text-gray-500">
        <p>Powered by OpenFisca & Catala</p>
      </footer>
    </main>
  );
}
