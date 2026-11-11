# Validation record: v1.3

v1.3 release verification (2026-11-11)

- Local XeLaTeX compilation succeeded (3 passes), A4, 115 pages.
- All six complete notebooks match the user-uploaded originals byte for byte (Git blob SHA-1 checked).
- Student notebook code cells and saved outputs remain unchanged; only the Markdown links to the released PDF are updated.
- The first three chapters and appendices A--D have not changed relative to the earlier TeX version; appendices E/F were added after D. Existing student input page references are therefore unchanged.
- GitHub Actions workflow is used to build and publish the PDF in docs/; verify its success before release.
