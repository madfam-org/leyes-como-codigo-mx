const TYPE_LABELS: Record<string, string> = {
  dead_link: 'Dead Link',
  missing_source: 'Sin Fuente',
  low_count: 'Conteo Bajo',
  not_scraped: 'No Scrapeado',
  parse_failure: 'Error de Parseo',
  site_redesign: 'Sitio Rediseñado',
};

interface GapTypeCardProps {
  type: string;
  count: number;
}

export function GapTypeCard({ type, count }: GapTypeCardProps) {
  return (
    <div className="flex items-center justify-between p-2 rounded-lg bg-muted/50">
      <span className="text-xs text-muted-foreground">{TYPE_LABELS[type] ?? type}</span>
      <span className="text-sm font-semibold tabular-nums">{count}</span>
    </div>
  );
}
