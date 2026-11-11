# Validation record: v1.3

2026-11-11.

## TeX and PDF

- The v1.3 TeX source adds appendices E and F after appendices A--D. The source of chapters 1--3 and appendices A--D is unchanged from v1.2.
- Local XeLaTeX compilation succeeded after three passes, producing an A4 PDF with 115 pages.
- GitHub Actions run [42940583242](https://github.com/babajn/galactic-dynamics-numerical-methods/actions/runs/42940583242) succeeded and published `docs/galactic_dynamics_numerical_methods_v1.3.pdf` to the release branch.
- The GitHub workflow checked that the PDF is nonempty, has 115 pages, and has no undefined reference or citation warnings in the final compilation log.
- A page-by-page visual comparison between the GitHub build and the local build has not been performed.

## Notebooks

- All six notebooks in `notebooks/complete/` are byte-identical to the uploaded complete versions (checked using Git blob SHA-1).
- All code cells in the six student notebooks are unchanged. Only Markdown references to the v1.3 PDF and version strings were edited.
- All 54 student notebook PDF links point to `docs/galactic_dynamics_numerical_methods_v1.3.pdf`; the referenced pages did not move because appendices E and F were appended after D.
- All six complete notebooks were re-executed successfully with nbclient 0.10.4 on Python 3.13.5 (NumPy 2.3.5, SciPy 1.17.0, Matplotlib 3.10.8). Each notebook executed every code cell without an error.
- Regeneration of textbook figures and numerical macros by the standalone scripts has not been retested.
