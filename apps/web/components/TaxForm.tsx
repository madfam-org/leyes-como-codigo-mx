"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { CheckCircle2, AlertCircle } from "lucide-react";

export default function TaxForm() {
    const [incomeCash, setIncomeCash] = useState<number>(0);
    const [incomeGoods, setIncomeGoods] = useState<number>(0);
    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setResult(null);

        try {
            const res = await fetch("http://localhost:8000/api/v1/calculate/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    period: "2024-01",
                    income_cash: incomeCash,
                    income_goods: incomeGoods,
                    is_resident: true,
                }),
            });

            if (!res.ok) {
                throw new Error("Calculation failed");
            }

            const data = await res.json();
            setResult(data);
        } catch (err) {
            setError("Error connecting to the tax engine.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Card className="max-w-md mx-auto shadow-lg">
            <CardHeader>
                <CardTitle>Calculadora de Impuestos</CardTitle>
                <CardDescription>Régimen General de Personas Físicas (LISR)</CardDescription>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="incomeCash">Ingreso Efectivo (MXN)</Label>
                        <Input
                            id="incomeCash"
                            type="number"
                            placeholder="0.00"
                            value={incomeCash}
                            onChange={(e) => setIncomeCash(parseFloat(e.target.value) || 0)}
                        />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="incomeGoods">Ingreso en Bienes (MXN)</Label>
                        <Input
                            id="incomeGoods"
                            type="number"
                            placeholder="0.00"
                            value={incomeGoods}
                            onChange={(e) => setIncomeGoods(parseFloat(e.target.value) || 0)}
                        />
                    </div>

                    <Button type="submit" className="w-full" disabled={loading}>
                        {loading ? "Calculando..." : "Calcular Impuestos"}
                    </Button>
                </form>

                {error && (
                    <Alert variant="destructive" className="mt-4">
                        <AlertCircle className="h-4 w-4" />
                        <AlertTitle>Error</AlertTitle>
                        <AlertDescription>{error}</AlertDescription>
                    </Alert>
                )}

                {result && (
                    <div className="mt-6 p-4 bg-green-50 rounded-lg border border-green-100">
                        <div className="flex items-center gap-2 mb-2">
                            <CheckCircle2 className="h-5 w-5 text-green-600" />
                            <h3 className="font-semibold text-green-800">Cálculo Completado</h3>
                        </div>
                        <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                            <dt className="text-gray-600">Ingreso Bruto:</dt>
                            <dd className="font-bold text-gray-900">${result.gross_income.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</dd>

                            <dt className="text-gray-600">Obligación ISR:</dt>
                            <dd className={`font-bold ${result.isr_obligation ? 'text-red-600' : 'text-green-600'}`}>
                                {result.isr_obligation ? "SÍ PAGA" : "EXENTO"}
                            </dd>
                        </dl>
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
