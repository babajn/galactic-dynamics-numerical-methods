"""Textbook-only geometry diagrams; no physical solver is reimplemented here.

Each panel is exported as an independent vector figure. The sparse matrix is
supplied by the numerical solver defined in the distributed Notebook 3.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

OI = {'black': '#000000', 'blue': '#0072B2', 'green': '#009E73', 'orange': '#E69F00', 'purple': '#CC79A7', 'vermillion': '#D55E00'}


def quadrature_demo_function(x):
    """A positive, visibly nonquadratic function used only for the geometry panels."""
    return 0.65 + 0.16 * x + 0.65 * np.sin(np.pi * x / 2.0) + 0.12 * np.sin(np.pi * x)


def export_quadrature_diagrams(save):
    """Use exactly the same function, nodes and axis limits for all four rules."""
    f = quadrature_demo_function
    edges = np.arange(5, dtype=float)
    xx = np.linspace(0.0, 4.0, 801)
    panels = [('Left rectangle rule', 'blue', 'ch01_left_rule.pdf'), ('Midpoint rule', 'green', 'ch01_midpoint_rule.pdf'), ('Trapezoidal rule', 'orange', 'ch01_trapezoid_rule.pdf'), ('Simpson rule', 'purple', 'ch01_simpson_rule.pdf')]
    with plt.rc_context({'font.size': 12, 'axes.labelsize': 13, 'axes.titlesize': 13, 'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 10.5, 'pdf.fonttype': 42}):
        for method, key, name in panels:
            fig, ax = plt.subplots(figsize=(4.4, 3.35))
            color = OI[key]
            ax.plot(xx, f(xx), '--', color=OI['black'], lw=1.55, label=r'$f(x)$', zorder=4)
            if method in ('Left rectangle rule', 'Midpoint rule'):
                shift = 0.5 if method.startswith('Midpoint') else 0.0
                nodes = edges[:-1] + shift
                for left, node in zip(edges[:-1], nodes):
                    height = f(node)
                    ax.add_patch(Rectangle((left, 0.0), 1.0, height, facecolor=color, alpha=0.10, edgecolor='none', zorder=0))
                    ax.plot([left, left, left + 1.0, left + 1.0], [0.0, height, height, 0.0], color=color, lw=1.6, zorder=2)
                ax.plot(nodes, f(nodes), 'o', color=color, ms=5.0, markeredgecolor='white', markeredgewidth=0.5, zorder=6)
                ax.plot([], [], color=color, lw=1.8, label='Constant pieces')
            elif method == 'Trapezoidal rule':
                for left, right in zip(edges[:-1], edges[1:]):
                    ax.add_patch(Polygon([(left, 0), (left, f(left)), (right, f(right)), (right, 0)], facecolor=color, alpha=0.12, edgecolor='none', zorder=0))
                    ax.plot([left, left, right, right], [0.0, f(left), f(right), 0.0], color=color, lw=1.6, zorder=2)
                ax.plot(edges, f(edges), 'o', color=color, ms=5.0, markeredgecolor='white', markeredgewidth=0.5, zorder=6)
                ax.plot([], [], color=color, lw=1.8, label='Linear pieces')
            else:
                # Each parabola uses three nodes and spans exactly two intervals.
                for start, local_color, symbol in [(0.0, OI['purple'], r'$p_2^{(0)}$'), (2.0, OI['blue'], r'$p_2^{(1)}$')]:
                    nodes = start + np.arange(3, dtype=float)
                    coeff = np.polyfit(nodes, f(nodes), 2)
                    panel_x = np.linspace(start, start + 2.0, 201)
                    panel_y = np.polyval(coeff, panel_x)
                    ax.fill_between(panel_x, 0.0, panel_y, color=local_color, alpha=0.10, zorder=0)
                    ax.plot(panel_x, panel_y, color=local_color, lw=2.15, zorder=3)
                    ax.plot(nodes, f(nodes), 'o', color=local_color, ms=5.5, markeredgecolor='white', markeredgewidth=0.6, zorder=6)
                    ax.vlines([start, start + 2.0], 0.0, [f(start), f(start + 2.0)], color=local_color, lw=1.0, alpha=0.7, zorder=1)
                    ax.annotate('', (start + 2.0, 1.72), (start, 1.72), arrowprops={'arrowstyle': '|-|', 'color': local_color, 'lw': 1.15})
                    ax.text(start + 1.0, 1.77, r'$2h$', color=local_color, ha='center', va='bottom', fontsize=12)
                    ax.text(start + 0.92, 0.78 if start == 0.0 else 0.20, symbol, color=local_color, fontsize=13, ha='center')
                ax.plot([], [], color=OI['purple'], lw=2.0, label='Quadratic pieces')
            ax.set(xlim=(-0.08, 4.08), ylim=(-0.02, 1.99), xlabel=r'$x$', ylabel=r'$f(x)$', title=method)
            ax.set_xticks([0, 1, 2, 3, 4])
            ax.set_yticks([0.0, 0.5, 1.0, 1.5])
            ax.grid(alpha=0.16, zorder=-1)
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=False, handlelength=1.6, columnspacing=1.0, borderaxespad=0.0)
            save(fig, name)


def export_sparse_explanation(A, save, NR=4, NZ=5, selected=(1, 2)):
    """Link a small labelled grid to one row of its actual discrete Poisson matrix."""
    nz = NZ - 1
    n = NR * nz
    if A.shape != (n, n):
        raise ValueError(f'Expected a {(n, n)} matrix, got {A.shape}')
    i0, j0 = selected
    p = i0 * nz + j0 - 1
    neighbors = [(i0 - 1, j0), (i0, j0 - 1), (i0, j0), (i0, j0 + 1), (i0 + 1, j0)]
    columns = sorted(i * nz + j - 1 for i, j in neighbors)
    actual_columns = sorted(A.getrow(p).nonzero()[1].tolist())
    if actual_columns != columns:
        raise AssertionError(f'Row {p}: {actual_columns} != {columns}')
    with plt.rc_context({'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 12, 'xtick.labelsize': 10.5, 'ytick.labelsize': 10.5, 'pdf.fonttype': 42}):
        fig, ax = plt.subplots(figsize=(4.55, 4.65))
        for i in range(NR + 1):
            ax.plot([i, i], [0, NZ], color='0.82', lw=0.7, zorder=0)
        for j in range(NZ + 1):
            ax.plot([0, NR], [j, j], color='0.82', lw=0.7, zorder=0)
        for i in range(NR + 1):
            for j in range(NZ + 1):
                if i == NR or j in (0, NZ):
                    ax.plot(i, j, 'x', color='0.52', ms=6.5, mew=1.2, zorder=2)
                    continue
                k = i * nz + j - 1
                chosen = (i, j) == selected
                near = (i, j) in neighbors
                color = OI['vermillion'] if chosen else (OI['blue'] if near else '0.45')
                ax.scatter([i], [j], s=460, marker='s' if chosen else 'o', facecolors='white', edgecolors=color, linewidths=2.0 if near else 0.8, zorder=3)
                ax.text(i, j, str(k), color=color if near else '0.25', fontsize=12, weight='bold' if near else 'normal', ha='center', va='center', zorder=4)
        for i, j in neighbors:
            if (i, j) != selected:
                ax.plot([i0, i], [j0, j], color=OI['blue'], lw=2.0, zorder=1)
        ax.set(xlim=(-0.52, NR + 0.48), ylim=(-0.46, NZ + 0.55), xlabel=r'Radial index $i$', ylabel=r'Vertical index $j$', title=r'Grid: $p=4i+(j-1)$')
        ax.set_xticks(range(NR + 1)); ax.set_yticks(range(NZ + 1))
        ax.set_aspect('equal')
        ax.text(0.5, -0.20, r'$\times$: known boundary; numbers: unknowns', transform=ax.transAxes, fontsize=10.2, ha='center')
        save(fig, 'appB_grid_numbering.pdf')

        fig, ax = plt.subplots(figsize=(4.55, 4.65))
        rows, cols = A.nonzero()
        ax.add_patch(Rectangle((-0.5, p - 0.5), n, 1, facecolor=OI['orange'], alpha=0.15, edgecolor='none', zorder=0))
        ax.scatter(cols, rows, marker='s', s=16, color='0.45', zorder=2)
        other = [k for k in columns if k != p]
        ax.scatter(other, [p] * len(other), marker='o', s=75, color=OI['blue'], zorder=4)
        ax.scatter([p], [p], marker='s', s=85, color=OI['vermillion'], zorder=5)
        for edge in np.arange(nz - 0.5, n, nz):
            ax.axhline(edge, color='0.72', lw=0.8, zorder=1)
            ax.axvline(edge, color='0.72', lw=0.8, zorder=1)
        ax.set(xlim=(-0.5, n - 0.5), ylim=(n - 0.5, -0.5), xlabel=r'Unknown index (column)', ylabel=r'Equation index (row)', title=rf'Matrix: highlighted row $p={p}$')
        xticks = sorted(set([0, 4, 8, 12, 15] + columns))
        yticks = sorted(set([0, 4, 8, 12, 15, p]))
        ax.set_xticks(xticks); ax.set_yticks(yticks)
        ax.set_aspect('equal')
        for tick in ax.xaxis.get_ticklabels():
            k = int(tick.get_text())
            if k in columns:
                tick.set_color(OI['vermillion'] if k == p else OI['blue'])
                tick.set_weight('bold')
        ax.text(0.5, -0.23, r'Row 5: columns $1,\ 4,\ 5,\ 6,\ 9$', transform=ax.transAxes, fontsize=11, ha='center')
        save(fig, 'appB_sparse_pattern.pdf')
