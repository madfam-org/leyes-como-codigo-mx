# Interactive Legal Map of Mexico - Design & Strategy

**Status**: Planned (Q3 2026)
**Objective**: Transform abstract legal data into a tangible, geographical visualization of Mexico's legislative landscape, enabling citizens and researchers to compare legal maturity across jurisdictions.

## 1. Core Concept

An interactive, multi-layered map component that serves as a high-level entry point to the platform. Users can visualize disparate legal metric across three administrative levels: Federal, State (32 entities), and Municipal (focus on major economic zones).

## 2. Statistical Data Layers

We will derive 6 key statistical dimensions from our scraping and analysis pipeline. These can be toggled as "Switchable Layers" on the map.

### A. Legislative Volume (Quantatative)
*   **Metric**: Total count of active regulations/laws per jurisdiction.
*   **Visualization**: Choropleth map (Color intensity: Light Blue → Deep Blue).
*   **Insight**: Shows regulatory density. "Which states are arguably 'over-regulated' vs 'under-regulated'?"

### B. Modernization Score (Temporal)
*   **Metric**: Median age of active legislation (or % of laws updated in the last 3 years).
*   **Visualization**: Diverging color scale (Red = Stagnant/Old, Green = Active/Modern).
*   **Insight**: Identifies jurisdictions with outdated legal frameworks.

### C. Harmonization Index (Qualitative/NLP)
*   **Metric**: Semantic similarity score of local laws to Federal "General Laws" (e.g., General Law of Transparency, Women's Access to a Life Free of Violence).
*   **Visualization**: Heatmap.
*   **Insight**: "Is Oaxaca's transparency law actually aligned with the Federal standard?"

### D. Digital Maturity / Transparency (Metadata)
*   **Metric**: Ratio of digital-native formats (HTML/XML) vs Legacy formats (Scanned PDFs).
*   **Visualization**: Traffic light system (Green = Machine Readable, Red = Scanned Images).
*   **Insight**: Direct measure of accessibility and transparency.

### E. Topical Intensity (Thematic)
*   **Metric**: Relative volume of laws per category (Civil, Environmental, Penal).
*   **Visualization**: Icon clusters or dominant color coding.
*   **Insight**: "Which states have the most robust Environmental protections?"

### F. Constitutional Alignment (Judicial) *(Advanced)*
*   **Metric**: Number of unconstitutional actions ("Acciones de Inconstitucionalidad") ruled against the state's laws by the SCJN.
*   **Visualization**: Bubble markers overlay.
*   **Insight**: Indicates quality of legislative drafting.

## 3. User Experience (UX)

### Navigation Levels
1.  **National View**: Comparative view of all 32 states.
2.  **Drill-Down**: Clicking a state zooms in to show its Municipalities (starting with Tier 1).
3.  **Context Panel**: Sidebar updates with detailed stats for the hovered/selected region.

### Interactive Features
*   **Time Machine Slider**: "Play" button to watch the map evolve over the last 10 years (requires historical data versioning).
*   **Compare Mode**: Select two states to open a side-by-side comparison view (using the existing Comparison Tool).
*   **Export**: Download the map view as PNG or the underlying data as CSV/JSON.

## 4. Technical Architecture

### Frontend
-   **Library**: `react-leaflet` or `react-simple-maps` (d3-geo based) for lightweight SVG rendering.
-   **Projection**: Mexican-centric projection.
-   **Performance**: GeoJSON simplification for fast loading on mobile.

### Backend / Data
-   **Aggregation Pipeline**: A nightly job (Celery/Redis) that pre-calculates the stats from the `laws` table and stores them in a optimized `stats_cache` table.
-   **Endpoints**:
    -   `GET /api/v1/stats/geo?layer=modernization&year=2024` -> Returns JSON with `{ state_id: value }`.

## 5. Implementation Roadmap

1.  **Data Preparation (Phase 1)**: Implement "Legislative Volume" and "Modernization Score" aggregators.
2.  **Prototype (Phase 2)**: Simple state-level map with one layer.
3.  **Advanced Analysis (Phase 3)**: Implement NLP pipeline for "Harmonization Index".
4.  **Full Release (Phase 4)**: Mobile optimization and Municipal drill-down.
