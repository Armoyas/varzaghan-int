# Feature Specification: Data Import & Geophysical Interpretation Pipeline

**Feature Branch**: `042-data-import-interpretation`
**Created**: 2026-09-14
**Status**: Draft
**Input**: User request — create a structured pipeline to import VES/ERT and supporting geophysical reference data for the Varzaghan region and run electrical interpretation (layer modeling, lithology inference, aquifer/bedrock delineation).

---

## User Scenarios & Testing

### User Story 1 — Import Raw VES Data (Priority: P1)

As a geophysicist, I need to import raw Vertical Electrical Sounding (VES) data (AB/2, MN, apparent resistivity) from standardized text files so that I can begin interpretation without manual re-formatting.

**Why this priority**: VES curves are the primary dataset; all interpretation depends on having clean, usable sounding data loaded correctly.

**Independent Test**: Load s1.TXT, s2.TXT, s3.TXT — verify column count = 3, non-negative ρₐ values, monotonic AB/2 spacing.

**Acceptance Scenarios**:
1. **Given** a Schlumberger VES TXT file with columns AB/2, MN, Ro_a, **When** the import script runs, **Then** a structured table (depth, apparent resistivity, spacing) is created with all rows loaded.
2. **Given** a file contains negative or null resistivity values, **When** the import script runs, **Then** those rows are flagged and excluded from computation (logged in QA report).
3. **Given** a Schlumberger curve where AB/2 increases monotonically, **When** imported, **Then** a sounding curve object is available for 1D inversion.

### User Story 2 — Interpret VES Sounding Curves (Priority: P1)

As a geophysicist, I need automatic 1D interpretation of VES curves (layer resistivities ρ₁, ρ₂, ρ₃ and thicknesses h₁, h₂) so that I can identify geological horizons (clay cover, saturated sand, bedrock, aquifer) without hand-fitting every curve.

**Why this priority**: Direct interpretation converts raw measurements into actionable geological models — this is the core value of the project.

**Independent Test**: Run interpretation on s1/s2/s3 — verify 3-layer model outputs ρ and h values fall within physically plausible ranges (ρ: 1–50000 Ω·m, h: 0.5–500 m).

**Acceptance Scenarios**:
1. **Given** a sounding curve with clear middle-layer flattening, **When** interpreted with gradient method (Routhgaris) or software, **Then** a 3-layer model is produced with ρ₁ (clay/cover), ρ₂ (saturated sand/gravel), ρ₃ (bedrock/deep).
2. **Given** interpreted ρ₂ value falls within 1–50 Ω·m, **When** cross-checked with regional geology, **Then** a saturated/alluvial aquifer is inferred.
3. **Given** ρ₃ > 1000 Ω·m, **When** classified, **Then** bedrock/competent rock horizon is flagged.

### User Story 3 — Generate Layer Interpretation Table (Priority: P1)

As a geophysicist, I need a structured table (depth range | resistivity | inferred lithology | confidence) for each sounding point so that I can present findings clearly to stakeholders and decision-makers.

**Why this priority**: A tabular summary is required for reports, cross-section drafting, and borehole correlation.

**Acceptance Scenarios**:
1. **Given** VES interpretation produces ρ₁, h₁, ρ₂, h₂, ρ₃ values, **When** layer table is generated, **Then** each row has depth range, ρ (Ω·m), lithology label, confidence level (Hi/Mid/Lo).
2. **Given** water table is shallower than h₁ + h₂, **When** layer table is generated, **Then** a "Water Table" or "Saturated Zone" row is present between h₁ and h₁+h₂.

### User Story 4 — QA Raw Field Data (Priority: P2)

As a field engineer, I need automated QA checks on imported VES data (negative ρₐ, erratic values, contact resistance issues, data gaps) so that poor-quality data is flagged before interpretation.

**Why this priority**: Garbage-in/garbage-out is a major source of misinterpretation in electrical methods.

**Acceptance Scenarios**:
1. **Given** imported data has ρₐ < 0 or null, **When** QA runs, **Then** those records are removed and logged with timestamp.
2. **Given** consecutive ρₐ values differ by >500%, **When** QA runs, **Then** the points are flagged as "erratic — check electrode contact."
3. **Given** AB/2 spacing has gaps >50% between measurements, **When** QA runs, **Then** the gap is reported in QA log.

### User Story 5 — Create Geological Cross-Section (Priority: P3)

As a project lead, I want to convert multiple VES interpretations into a merged cross-section along the survey profile so that I can visualize the subsurface structure along the transect.

**Why this priority**: Cross-sections are required for final reports and groundwater mapping (project goal per varzaghn13.pdf).

**Acceptance Scenarios**:
1. **Given** at least 2 interpreted VES points with layer depths, **When** cross-section is generated, **Then** a depth-vs-distance plot shows layered subsurface structure.
2. **Given** multiple VES points, **When** bedrock top depths are compared, **Then** a depth contour or profile is created.

---

## Requirements

### Functional Requirements

- **FR-001**: Import script MUST accept Schlumberger VES TXT files with columns AB/2, MN, ρₐ (apparent resistivity in Ω·m).
- **FR-002**: Import script MUST output a structured data table (DataFrame or CSV) with columns: AB/2 (m), MN (m), ρₐ (Ω·m), log(AB/2), K (geometric factor).
- **FR-003**: 1D inversion (gradient method / software-equivalent) MUST produce layer resistivities and thicknesses for at least 3 layers.
- **FR-004**: Lithology assignment MUST use typical resistivity ranges (documented in code/README) and regional context.
- **FR-005**: QA module MUST detect and report: negative ρₐ, null values, erratic jumps (>500% between consecutive points), electrode contact failures.
- **FR-006**: Export layer interpretation table in CSV and Markdown formats.
- **FR-007**: System MUST support Persian/Farsi labels for lithology categories and report headers (bilingual EN/FA output).
- **FR-008**: All outputs MUST be reproducible from the same input data (deterministic inversion parameters).

### Key Entities (Data Models)

- **VESPoint**: {AB2 (float, m), MN (float, m), ρₐ (float, Ω·m), log_AB2 (float), K_factor (float)}
- **LayerModel**: {layer_index (int), ρ_top (float, Ω·m), ρ_bottom (float, Ω·m), thickness (float, m), depth_top (float, m), depth_bottom (float, m), lithology (str), confidence (str: Hi/Mid/Lo)}
- **SoundingCurve**: {station_id (str), points (List[VESPoint]), model (LayerModel), qa_flags (List[str])}
- **QAReport**: {station_id (str), total_points (int), rejected_points (int), issues (List[dict])}

---

## Success Criteria

- **SC-001**: All 3 VES soundings (s1, s2, s3) imported and interpreted with 3+ layers each within 1 hour of processing time.
- **SC-002**: Layer interpretation table contains zero null or missing values for ρ, depth, or lithology fields.
- **SC-003**: QA report identifies ≥95% of known data quality issues in the reference dataset.
- **SC-004**: Cross-section aligns with geological map of Varzaghan region (Varzaghan Formation — Tertiary volcaniclastic, alluvial deposits).
- **SC-005**: Output files are readable without proprietary software (all open formats: CSV, MD, PDF via WeasyPrint).

---

## Assumptions

1. VES data follows Schlumberger array geometry (AB/2 ≫ MN).
2. 1D inversion is adequate for initial interpretation; no 2D/3D inversion required for Phase 1.
3. Reference data (s1/s2/s3) are representative of the survey lines described in the Varzaghan geophysical report (summer 1393).
4. Archie's law parameters (m=2, n=2, a=1, φ_w) are not required for Phase 1 — resistivity-to-lithology mapping is empirical.
5. Local groundwater conditions follow alluvial/aeolian settings typical of Varzaghan (Kura-Araxes basin).
6. Farsi language support via Unicode UTF-8 is available throughout the pipeline.

---

## Dependencies

- **Python 3.10+** with NumPy/SciPy for numerical inversion.
- **Matplotlib** for VES curve and cross-section plotting.
- **WeasyPrint** (or wkhtmltopdf) for PDF report generation with Persian font support (Vazirmatn).
- **Varzaghan geophysical report (varzaghn13.pdf)** — reference for geological context and survey design.
- Geographical coordinates of s1, s2, s3 stations (from report Figure 3-5).

---

## Out of Scope

- 2D/3D ERT inversion (Phase 2 enhancement).
- Induced Polarization (IP) data interpretation.
- Full borehole integration for layer correlation.
- Real-time field data streaming.
- Automated borehole-log matching.
- Machine-learning-based lithology classification (Phase 3).
