"""付録Dの行列を読み、前進消去前後の非零パターンを描く。式の係数は別管理しない。"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import hashlib
import json
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

REPO_ROOT = Path(__file__).resolve().parents[2]
BOOK_ROOT = REPO_ROOT / "textbook"
SOURCE = BOOK_ROOT / "appendices/appendixD_linear_systems.tex"
OUT = BOOK_ROOT / "figures/appD_sparse_elimination_fillin.pdf"
REPORT = BOOK_ROOT / "generated/appendixD/figure_checks.json"


def source_matrix(text: str, label: str) -> list[list[Fraction]]:
    """指定ラベルの式から最初の整数成分のpmatrixを読む。"""
    equations = re.findall(r"\\begin\{equation\}(.*?)\\end\{equation\}", text, re.S)
    matches = [eq for eq in equations if rf"\label{{{label}}}" in eq]
    if len(matches) != 1:
        raise ValueError(f"Equation label is not unique: {label}")
    matrix = re.search(r"\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}", matches[0], re.S)
    if matrix is None:
        raise ValueError(f"No pmatrix in {label}")
    rows = [[Fraction(v.strip()) for v in row.split("&")] for row in matrix[1].split(r"\\") if row.strip()]
    if not rows or any(len(row) != len(rows) for row in rows):
        raise ValueError(f"Expected a square matrix in {label}")
    return rows


def eliminate(matrix: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[list[Fraction]]]:
    """行交換なしの前進消去。UだけでなくLも計算して厳密に検算する。"""
    n = len(matrix)
    upper = [row.copy() for row in matrix]
    lower = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for k in range(n - 1):
        if upper[k][k] == 0:
            raise ArithmeticError("Zero pivot: this illustration assumes no row swaps.")
        for i in range(k + 1, n):
            if upper[i][k] == 0:
                continue
            lower[i][k] = upper[i][k] / upper[k][k]
            for j in range(k, n):
                upper[i][j] -= lower[i][k] * upper[k][j]
    product = [[sum(lower[i][k] * upper[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    if product != matrix:
        raise AssertionError("Exact LU verification failed.")
    return lower, upper


def nonzeros(matrix: list[list[Fraction]]) -> set[tuple[int, int]]:
    return {(i + 1, j + 1) for i, row in enumerate(matrix) for j, value in enumerate(row) if value != 0}


def draw_matrix(ax, x: float, title: str, original, current) -> None:
    """1始まりの行・列番号、非零位置だけを示す。マーカーの大きさは係数値に依存しない。"""
    n, size, top = len(current), 26.0, 54.0
    cell, bottom = size / n, top - size
    ax.text(x + size / 2, 66, title, ha="center", va="center", fontsize=9.0)
    for k in range(n + 1):
        ax.plot([x, x + size], [bottom + k * cell] * 2, color="0.78", lw=0.4, zorder=0)
        ax.plot([x + k * cell] * 2, [bottom, top], color="0.78", lw=0.4, zorder=0)
    for i in range(n):
        ax.text(x - 2.0, top - (i + 0.5) * cell, str(i + 1), ha="right", va="center", fontsize=8.3)
        ax.text(x + (i + 0.5) * cell, top + 2.3, str(i + 1), ha="center", va="center", fontsize=8.3)
        for j in range(n):
            if current[i][j] == 0:
                continue
            xc, yc = x + (j + 0.5) * cell, top - (i + 0.5) * cell
            if original[i][j] == 0:
                ax.add_patch(Circle((xc, yc), 1.5, facecolor="white", edgecolor="#D55E00", lw=1.7, zorder=3))
            else:
                ax.add_patch(Rectangle((xc - 1.25, yc - 1.25), 2.5, 2.5, facecolor="black", edgecolor="black", lw=0.5, zorder=2))


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    A = source_matrix(text, "eq:appD-example")
    B = source_matrix(text, "eq:appD-sparse2d-example")
    LA, UA = eliminate(A)
    LB, UB = eliminate(B)
    fill_A, fill_B = nonzeros(UA) - nonzeros(A), nonzeros(UB) - nonzeros(B)
    assert not fill_A
    assert fill_B == {(2, 3)} and UB[1][2] == Fraction(-1, 4)
    assert len(nonzeros(A)) == 7 and len(nonzeros(UA)) == 5
    assert len(nonzeros(B)) == 12 and len(nonzeros(UB)) == 9

    plt.rcParams.update({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans", "pdf.fonttype": 42, "ps.fonttype": 42})
    fig = plt.figure(figsize=(161 / 25.4, 78 / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 161), ylim=(0, 78))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(38, 75, "(a) Tridiagonal", ha="center", va="center", fontsize=10, fontweight="bold")
    ax.text(122, 75, "(b) Sparse 2D example", ha="center", va="center", fontsize=10, fontweight="bold")
    ax.plot([81, 81], [22, 76.5], color="0.78", lw=0.5)
    draw_matrix(ax, 5, r"Before: $A$", A, A)
    draw_matrix(ax, 46, r"After: $U$", A, UA)
    draw_matrix(ax, 89, r"Before: $B$", B, B)
    draw_matrix(ax, 130, r"After: $U_B$", B, UB)
    for x1, x2 in [(33, 41), (117, 125)]:
        ax.add_patch(FancyArrowPatch((x1, 41), (x2, 41), arrowstyle="-|>", mutation_scale=11, lw=1.1, color="black"))
    ax.text(38, 21, "No fill-in", ha="center", va="center", fontsize=9.0)
    ax.text(122, 21, r"Row 2, column 3: $0\;\to\;-1/4$", ha="center", va="center", fontsize=9.0, color="#D55E00")
    ax.add_patch(Rectangle((8.5, 10.7), 2.5, 2.5, facecolor="black", edgecolor="black", lw=0.5))
    ax.text(14, 12, "Original nonzero position", ha="left", va="center", fontsize=8.3)
    ax.add_patch(Circle((91, 12), 1.5, facecolor="white", edgecolor="#D55E00", lw=1.7))
    ax.text(95, 12, "Fill-in (originally zero)", ha="left", va="center", fontsize=8.3)
    ax.text(80.5, 3.5, "Blank cells = zero. Gauss elimination without row swaps.", ha="center", va="center", fontsize=8.0)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, metadata={"Title": "Sparse elimination and fill-in", "Creator": "Exact-rational matrix figure", "CreationDate": None, "ModDate": None})
    plt.close(fig)
    report = {
        "matrix_source": str(SOURCE.relative_to(REPO_ROOT)),
        "matrix_labels": ["eq:appD-example", "eq:appD-sparse2d-example"],
        "elimination": "exact rational arithmetic; natural ordering; no row swaps",
        "A": [[str(x) for x in row] for row in A],
        "U": [[str(x) for x in row] for row in UA],
        "B": [[str(x) for x in row] for row in B],
        "U_B": [[str(x) for x in row] for row in UB],
        "LU_identity": "passed for both matrices",
        "nonzero_counts": {"A": len(nonzeros(A)), "U": len(nonzeros(UA)), "B": len(nonzeros(B)), "U_B": len(nonzeros(UB))},
        "fill_in_U": sorted(fill_A),
        "fill_in_U_B": sorted(fill_B),
        "fill_in_value": str(UB[1][2]),
        "figure_sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
