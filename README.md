# Varzaghan Geophysical Interpretation

Electrical methods (VES/ERT) data import, interpretation, and reporting for the Varzaghan region study.

## Project Overview

This project imports Vertical Electrical Sounding (VES) data from Schlumberger array surveys, performs 1D interpretation (gradient/least-squares layer inversion), and produces bilingual (EN/FA) reports for groundwater, geotechnical, and geological studies.

**Reference study**: Geophysical report on electrical resistivity in Varzaghan region (Summer 1393), by consulting engineer Mr. Piri, under Dr. Fazel Khalghi & Dr. Habib Rahimi.

## Dataset

### Reference Data (knowledge-base/Geoelectric/)

| File | Description |
|---|---|
| `s1.TXT` | VES Curve 1 — AB/2, MN, rho_a (16 points) |
| `s2.TXT` | VES Curve 2 — AB/2, MN, rho_a (15 points) |
| `s3.TXT` | VES Curve 3 — AB/2, MN, rho_a (16 points) |
| `varzaghn13.pdf` | Full geophysical report (Persian) |
| `peiri1-copy.jpg` | Field photo / section |
| `peiri2.jpg` | Field photo / section |

All data originally from the "Geoelctric" knowledge base (documents from Varzaghan).

## Quick Start

```bash
pip install -r requirements.txt
python src/main.py
# Output: output/
```

## Pipeline Steps

1. **Load** VES TXT files → DataFrame
2. **QA** data quality (negative rho, erratic values, gaps)
3. **Interpret** 1D layer model (gradient method)
4. **Classify** lithology per layer
5. **Report** — bilingual table + PDF

## Tech Stack

- Python 3.11+
- NumPy / SciPy (inversion)
- pandas (data)
- matplotlib (figures)
- WeasyPrint (PDF with Vazirmatn font)

## Lithology Resistivity Ranges (Typical)

| Lithology | Resistivity (ohm-m) | Notes |
|---|---|---|
| Clay / Wet clay | 1 – 20 | Low resistivity, aquitard |
| Saturated sand / Gravel | 10 – 100 | Aquifer candidate |
| Semi-dry sand | 50 – 500 | Transitional |
| Dry gravel / Sandstone | 500 – 5,000 | Moderate |
| Bedrock (fresh) | > 1,000 | Competent rock |
| Mineralized / Saline water | 1 – 50 | Depends on salinity |

> **Regional caveat**: Varzaghan alluvial context — resistivity ranges may shift ±30% based on groundwater salinity, temperature, and clay content (Kura-Araxes basin sediments).

## Folder Structure

```
knowledge-base/Geoelectric/   <- Reference data
specs/                          <- Spekit SDD specs
src/                            <- Source code
output/                         <- Generated results
docs/                           <- Documentation
tests/                          <- Tests
```

## License

Academic / research use. Data from Varzaghan geophysical survey (1393).
