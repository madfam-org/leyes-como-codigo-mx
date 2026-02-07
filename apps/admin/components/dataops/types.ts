// ── Coverage Dashboard API Response Types ────────────────────────────

export interface TierProgress {
  key: string;
  label: string;
  known_universe: number | null;
  scraped: number;
  in_db: number;
  permanent_gaps: number;
  coverage_pct: number;
  confidence: string;
  source_name: string;
  source_url: string;
}

export interface CoverageView {
  label: string;
  universe: number;
  captured: number;
  pct: number;
}

export interface StateCoverage {
  state: string;
  legislative_in_db: number;
  non_legislative_in_db: number;
  total_in_db: number;
  anomaly: string | null;
}

export interface TopGap {
  id: number;
  level: string;
  state: string;
  gap_type: string;
  description: string;
  status: string;
  priority: number;
  current_tier: number;
}

export interface GapSummary {
  total: number;
  by_status: Record<string, number>;
  by_tier: Record<string, number>;
  by_level: Record<string, number>;
  by_type: Record<string, number>;
  actionable: number;
  overdue: number;
  top_gaps: TopGap[];
}

export interface ExpansionPriority {
  rank: number;
  action: string;
  estimated_gain: number;
  effort: string;
  roi_score: number;
}

export interface HealthSource {
  id: number;
  name: string;
  source_type: string;
  level: string;
  status: string;
  last_check: string | null;
  last_success: string | null;
  response_time_ms: number | null;
}

export interface HealthStatus {
  summary: {
    total_sources: number;
    healthy: number;
    degraded: number;
    down: number;
    unknown: number;
    never_checked: number;
  };
  sources: HealthSource[];
}

export interface DashboardData {
  generated_at: string;
  tier_progress: TierProgress[];
  coverage_views: Record<string, CoverageView>;
  state_coverage: StateCoverage[];
  gap_summary: GapSummary;
  expansion_priorities: ExpansionPriority[];
  health_status: HealthStatus;
}

// ── Roadmap API Response Types ───────────────────────────────────────

export interface RoadmapItemData {
  id: number;
  title: string;
  description: string;
  category: string;
  status: string;
  estimated_laws: number;
  estimated_effort: string;
  priority: number;
  progress_pct: number;
  notes: string;
  started_at: string | null;
  completed_at: string | null;
}

export interface RoadmapPhase {
  phase: number;
  label: string;
  items: RoadmapItemData[];
  total: number;
  completed: number;
  in_progress: number;
  estimated_laws: number;
}

export interface RoadmapData {
  summary: {
    total_items: number;
    completed: number;
    in_progress: number;
    total_estimated_laws: number;
  };
  phases: RoadmapPhase[];
}
