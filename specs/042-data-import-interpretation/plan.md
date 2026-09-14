# Implementation Plan: Data Import & Geophysical Interpretation Pipeline

**Branch**: `042-data-import-interpretation` | **Date**: 2026-09-14 | **Spec**: [spec.md](./spec.md)

---

## Summary

Build a reproducible pipeline that imports Schlumberger VES sounding data (s1, s2, s3), runs 1D gradient-method inversion or curve fitting, interprets layer parameters (ρ, h), assigns lithology based on resistivity ranges, performs QA, and produces tabulated + PDF outputs for the Varzaghan region study. **Phase 1** focuses on electrical-only interpretation.

**Key architectural decisions**:
- Python-based pipeline (NumPy/SciPy for inversion, Matplotlib for plots, WeasyPrint for bilingual PDF generation).
- Data-first design: raw VES TXT files → DataFrame → inversion → LayerModel → table/report.
- Bilingual (EN/FA) output headers and lithology labels using Unicode UTF-8.
- Reference data stored in `knowledge-base/Geoelectric/` mirror of knowledge base.

**P1/P2/P3 breakdown**:
- **P1 (MVP)**: Import, 1D interpretation, layer table, QA detection, basic report.
- **P2 (Important)**: Cross-section generation, QA automation, enhanced lithology model.
- **P3 (Nice-to-have)**: PDF report with Vazirmatn fonts, cross-section publication figure, ERT module placeholder.

---

## Technical Context

- **Language/Version**: Python 3.11+, GNU General Public License-compatible libraries only.
- **Primary Dependencies**:
  - numpy, scipy (inversion algorithms)
  - pandas (data I/O)
  - matplotlib (plots)
  - weasyprint (PDF), Vazirmatn font files
- **Storage**: CSV/TSV for raw data and outputs; MD for reports; JPG/PNG for figures.
- **Target Platform**: Linux (CI/CD via GitHub Actions optional).
- **Performance Goals**: <5 min end-to-end for 3 soundings, 20 points each.
- **Constraints**: Deterministic results (no stochastic inversion params); open formats only.
- **Scale/Scope**: 3–10 VES points initially; scalable to 100+ in future.

---

## Constitution Check

Since this is a new project (no existing constitution), the following project principles are declared:

| Principle | Status | Justification |
|---|---|---|
| Simplicity over complexity | ✅ PASS | Direct 1D inversion — no ML, no complex stacking for Phase 1. |
| Open formats only | ✅ PASS | CSV, MD, PNG outputs — no proprietary formats. |
| Reproducibility | ✅ PASS | Fixed random seeds where applicable; deterministic inversion params. |
| Bilingual support | ✅ PASS | All labels output in EN + FA (UTF-8). |
| Data as source of truth | ✅ PASS | Raw VES data is never modified — copies stored in knowledge-base/Geoelectric/. |

---

## Project Structure

```
varzaghan-int/
├── knowledge-base/
│   └── Geoelectric/
│       ├── s1.TXT
│       ├── s2.TXT
│       ├── s3.TXT
│       ├── varzaghn13.pdf
│       ├── peiri1-copy.jpg
│       ├── peiri2.jpg
│       └── README.md
├── specs/
│   └── 042-data-import-interpretation/
│       ├── spec.md
│       ├── plan.md
│       └── checklists/
│           └── requirements.md
├── src/                         # (future in Step 3)
│   ├── __init__.py
│   ├── loader.py
│   ├── interpreter.py
│   ├── qa_checker.py
│   └── report_gen.py
├── output/                      # Generated results
│   ├── data/
│   ├── figures/
│   └── reports/
├── docs/
│   └── lithology_table.md
├── tests/
│   └── test_pipeline.py
├── README.md
├── requirements.txt
└── .github/
    └── workflows/
        └── ci.yml               # (future)
```

---

## Complexity Tracking

No constitution violations expected in Phase 1. All decisions justified under "Simplicity over complexity."

---

## Implementation Checklist

### Step 1 — Project Skeleton & Data Loader (1 day)

**Goal**: Project structure with README, requirements.txt, and a Python loader that reads TXT VES files.

- [ ] Initialize repo files (README.md, requirements.txt, .gitignore).
- [ ] Copy knowledge-base/Geoelectric/ reference data into repo.
- [ ] Create `src/loader.py`: reads Schlumberger VES TXT with columns AB/2, MN, Ro_a.
- [ ] Add data validation: reject rows where ρₐ ≤ 0 or null; raise warning for gaps.
- [ ] **Test**: Load s1, s2, s3 — verify 16, 15, 16 rows respectively (correct count check).

**Files created/modified**:
- `README.md` (initial)
- `requirements.txt`
- `.gitignore`
- `knowledge-base/Geoelectric/` (copied)
- `src/loader.py`
- `tests/test_loader.py`

### Step 2 — 1D VES Interpretation (1 day)

**Goal**: Implement gradient method (Routhgaris) or least-squares 3-layer curve fitting.

- [ ] Create `src/interpreter.py`: Schlumberger 1D forward modeling function (K-factor + geometric factor).
- [ ] Implement gradient-descent or least-squares inversion for ρ₁, h₁, ρ₂, h₂, ρ₃ (up to 3 layers).
- [ ] Add parameter bounds (ρ: 1–50000 Ω·m, h: 0.5–500 m).
- [ ] Apply to s1, s2, s3 — capture layer parameters.
- [ ] **Test**: Verify layer resistivities and thicknesses are within physical bounds.

**Files created/modified**:
- `src/interpreter.py`
- `tests/test_interpreter.py`

### Step 3 — Lithology Inference & QA (1 day)

**Goal**: Assign lithology layers; run QA checks; generate initial layer table.

- [ ] Create `docs/lithology_table.md` — standard resistivity ranges (clay, sand, gravel, aquifer, bedrock) with regional Varzaghan notes.
- [ ] Create `src/lithology.py`: map ρ ranges → lithology labels (EN + FA).
- [ ] Create `src/qa_checker.py`: detect negative ρₐ, erratic jumps, data gaps.
- [ ] Generate layer interpretation table for s1, s2, s3 (CSV + Markdown).
- [ ] **Test**: Layer table has no nulls; QA catches injected errors in test data.

**Files created/modified**:
- `docs/lithology_table.md`
- `src/lithology.py`
- `src/qa_checker.py`
- `output/data/layer_table_s1.csv` (example)
- `output/data/layer_table_s1.md` (example)

### Step 4 — Reporting & Cross-Section (1 day)

**Goal**: Generate bilingual PDF report; create cross-section from multiple VES points.

- [ ] Create `src/report_gen.py`: gather tables, plots, QA summary → HTML → PDF via WeasyPrint (with Vazirmatn font).
- [ ] Create cross-section figure from s1, s2, s3 interpreted bedrock tops.
- [ ] Draft report in Persian with English translation side-by-side (key sections).
- [ ] **Test**: PDF renders correctly; section figures clearly show layer tops.

**Files created/modified**:
- `src/report_gen.py`
- `output/reports/varzaghan_geoelectric_report.pdf`
- `output/figures/cross_section.png`

### Step 5 — Hardening & Documentation (1 day)

**Goal**: Code review; README update; exit criteria verification.

- [ ] All P1 user stories passing.
- [ ] Performance check: full pipeline <5 min.
- [ ] README.md updated with usage instructions.
- [ ] `requirements.txt` finalized with pinned versions.
- [ ] **Test**: Fresh checkout → `pip install -r requirements.txt` → `python main.py` → PDF output.

**Files created/modified**:
- `README.md` (final)
- `requirements.txt` (final)
- Exit criteria validated.

---

## Exit Criteria

- All P1 user stories have independent tests passing.
- Pipeline runs end-to-end in <5 minutes on reference data.
- Output PDF and CSV/Markdown files are open-format and readable without proprietary tools.
- Layer interpretation table populated for s1, s2, s3 with depth | ρ (Ω·m) | lithology | confidence.
- QA flags all known issues in reference data.
- No unexplained variance between run-to-run outputs (determinism verified).

---

## Quick Reference

| Key | Value |
|---|---|
| Repo URL | https://github.com/Armoyas/varzaghan-int |
| Spec Branch | `042-data-import-interpretation` |
| Input Data | `knowledge-base/Geoelectric/s[1-3].TXT` |
| Output Dir | `output/` |
| Report | `output/reports/varzaghan_geoelectric_report.pdf` |
| Lithology Doc | `docs/lithology_table.md` |
| Stack | Python 3.11+, NumPy/SciPy, pandas, matplotlib, WeasyPrint |
