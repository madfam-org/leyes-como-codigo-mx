// Law metadata for the viewer
export interface Law {
    id: string;
    name: string;
    fullName: string;
    articles: number;
    transitorios: number;
    grade: 'A' | 'B' | 'C';
    score: number;
    priority: 1 | 2;
    tier: string;
    file: string;
}

export const laws: Law[] = [
    {
        id: 'amparo',
        name: 'Ley de Amparo',
        fullName: 'Ley de Amparo, Reglamentaria de los Artículos 103 y 107 de la Constitución',
        articles: 285,
        transitorios: 8,
        grade: 'A',
        score: 99.0,
        priority: 1,
        tier: 'constitutional',
        file: 'mx-fed-amparo-v2.xml'
    },
    {
        id: 'iva',
        name: 'Ley del IVA',
        fullName: 'Ley del Impuesto al Valor Agregado',
        articles: 94,
        transitorios: 27,
        grade: 'A',
        score: 96.6,
        priority: 1,
        tier: 'fiscal',
        file: 'mx-fed-iva-v2.xml'
    },
    {
        id: 'cpeum',
        name: 'Constitución Política',
        fullName: 'Constitución Política de los Estados Unidos Mexicanos',
        articles: 205,
        transitorios: 206,
        grade: 'A',
        score: 98.1,
        priority: 1,
        tier: 'constitutional',
        file: 'mx-fed-cpeum-v2.xml'
    },
    {
        id: 'lisr',
        name: 'Ley del ISR',
        fullName: 'Ley del Impuesto Sobre la Renta',
        articles: 322,
        transitorios: 0,
        grade: 'B',
        score: 92.1,
        priority: 1,
        tier: 'fiscal',
        file: 'mx-fed-lisr-v2.xml'
    },
    {
        id: 'ccf',
        name: 'Código Civil Federal',
        fullName: 'Código Civil Federal',
        articles: 3156,
        transitorios: 50,
        grade: 'A',
        score: 99.8,
        priority: 2,
        tier: 'civil',
        file: 'mx-fed-ccf-v2.xml'
    },
    {
        id: 'lft',
        name: 'Ley Federal del Trabajo',
        fullName: 'Ley Federal del Trabajo',
        articles: 1363,
        transitorios: 33,
        grade: 'A',
        score: 98.1,
        priority: 1,
        tier: 'labor',
        file: 'mx-fed-lft-v2.xml'
    },
    {
        id: 'lic',
        name: 'Ley de Instituciones de Crédito',
        fullName: 'Ley de Instituciones de Crédito',
        articles: 560,
        transitorios: 39,
        grade: 'A',
        score: 98.1,
        priority: 2,
        tier: 'financial',
        file: 'mx-fed-lic-v2.xml'
    },
    {
        id: 'lfpc',
        name: 'Ley de Protección al Consumidor',
        fullName: 'Ley Federal de Protección al Consumidor',
        articles: 227,
        transitorios: 242,
        grade: 'A',
        score: 98.1,
        priority: 2,
        tier: 'consumer',
        file: 'mx-fed-lfpc-v2.xml'
    },
    {
        id: 'lgsm',
        name: 'Ley de Sociedades Mercantiles',
        fullName: 'Ley General de Sociedades Mercantiles',
        articles: 297,
        transitorios: 8,
        grade: 'B',
        score: 91.5,
        priority: 2,
        tier: 'commercial',
        file: 'mx-fed-lgsm-v2.xml'
    },
    {
        id: 'lgtoc',
        name: 'Ley de Títulos y Operaciones de Crédito',
        fullName: 'Ley General de Títulos y Operaciones de Crédito',
        articles: 479,
        transitorios: 26,
        grade: 'A',
        score: 98.1,
        priority: 2,
        tier: 'commercial',
        file: 'mx-fed-lgtoc-v2.xml'
    }
];

export function getLawById(id: string): Law | undefined {
    return laws.find(law => law.id === id);
}

export function getTotalArticles(): number {
    return laws.reduce((sum, law) => sum + law.articles, 0);
}

export function getAverageQuality(): number {
    const total = laws.reduce((sum, law) => sum + law.score, 0);
    return total / laws.length;
}

export function getGradeDistribution(): Record<string, number> {
    return laws.reduce((acc, law) => {
        acc[law.grade] = (acc[law.grade] || 0) + 1;
        return acc;
    }, {} as Record<string, number>);
}
