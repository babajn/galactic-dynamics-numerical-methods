"""Use trusted full-implementation notebooks as the numerical source.

Figure scripts execute notebook code in a fresh namespace (without a Jupyter
kernel), export selected figures at plt.show(), and format values from that same
execution. No physical solver is reimplemented here. Only trusted local notebooks under notebooks/complete should be executed.
"""
from pathlib import Path
from dataclasses import dataclass
import contextlib, hashlib, io, json, os, re
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
import nbformat
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import QuadMesh

REPO_ROOT = Path(__file__).resolve().parents[2]
BOOK_ROOT = REPO_ROOT / 'textbook'
FIG = BOOK_ROOT / 'figures'
FIG.mkdir(exist_ok=True)
PREFIX = {1:'ryden_ch6_notebook1_', 2:'ryden_ch6_notebook2_', 3:'ryden_ch7_notebook3_', 'C':'ryden_notebookC_', 'B':'ryden_notebookB_', 'A':'ryden_notebookA_'}

@dataclass
class NotebookRun:
    path: Path
    state: dict
    snapshots: dict
    stdout: str
    source_sha256: str

def notebook_path(number: int | str) -> Path:
    """Locate the single distributed notebook for a chapter.

    Notebook filenames may carry any revision suffix (or none).  The chapter
    prefix is the stable identifier; version strings are deliberately ignored.
    Complete notebooks are stored under notebooks/complete/. Student notebooks
    (notebooks/student/) are intentionally excluded because they contain
    unfilled code cells and cannot be used to regenerate figures.
    """
    if number not in PREFIX:
        raise ValueError(f'Unknown notebook number: {number}')

    pattern = PREFIX[number] + '*.ipynb'
    searched = []
    for directory in (REPO_ROOT/'notebooks'/'complete',):
        searched.append(str(directory))
        if not directory.exists():
            continue
        matches = sorted(directory.glob(pattern))
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            names = ', '.join(p.name for p in matches)
            raise RuntimeError(
                f'Multiple notebooks match chapter {number} in {directory}: {names}. '
                'Keep exactly one distributed notebook for each chapter prefix.'
            )

    raise FileNotFoundError(
        f'Notebook {number} not found. Expected one file matching {pattern!r} '
        f'in one of: {", ".join(searched)}. The complete notebooks are required for figure generation.'
    )

def save_figure(fig, name: str):
    """Export vector text/lines with rasterized color meshes to avoid PDF seams.

    Only QuadMesh artists (including a colorbar's mesh) are rasterized. Their
    arrays, coordinates, normalization and colormap are not modified.
    """
    for mesh in fig.findobj(match=lambda artist: isinstance(artist, QuadMesh)):
        mesh.set_rasterized(True)
        mesh.set_edgecolor('none')
        mesh.set_linewidth(0.0)
        mesh.set_antialiased(False)
    fig.tight_layout()
    fig.savefig(FIG/name, dpi=400, bbox_inches='tight', metadata={'Creator':'Notebook-backed master figure script', 'CreationDate':None, 'ModDate':None})
    plt.close(fig)

def require_snapshot(run: NotebookRun, cell_id: str, label: str) -> dict:
    """Return a saved notebook namespace with a diagnostic if a cell ID changed."""
    try:
        return run.snapshots[cell_id]
    except KeyError:
        available = ', '.join(run.snapshots.keys())
        raise RuntimeError(
            f"Required notebook cell {label!r} (id={cell_id}) was not found in "
            f"{run.path.name}. The cell may have been copied, recreated, or otherwise "
            f"assigned a new Jupyter cell ID. Update the CELL_* constant in the "
            f"corresponding figures_master_chapXX.py file. Available code-cell IDs: "
            f"{available}"
        ) from None

def run_notebook(number: int | str, exports: dict | None = None, overrides: dict | None = None) -> NotebookRun:
    """Run code cells; optional overrides map cell IDs to variable-value mappings."""
    path=notebook_path(number)
    nb=nbformat.read(path,as_version=4)
    exports={} if exports is None else exports
    overrides={} if overrides is None else overrides
    ns={'__name__':f'notebook{number}_reference', '__file__':str(path)}
    snapshots={}; source=[]; buffer=io.StringIO(); saved=set()
    old_show=plt.show
    try:
        with contextlib.redirect_stdout(buffer):
            for c in nb.cells:
                if c.cell_type != 'code':
                    continue
                source.append((c.id,c.source))
                output_index=[0]
                def show(*args, **kwargs):
                    key=(c.id,output_index[0]); output_index[0]+=1
                    if key in exports:
                        save_figure(plt.gcf(),exports[key]); saved.add(key)
                    else:
                        plt.close('all')
                plt.show=show
                exec(compile(c.source,f'{path.name}:{c.id}','exec'),ns)
                # Overrides after a setup cell simulate editing that cell and rerunning.
                if c.id in overrides:
                    ns.update(overrides[c.id])
                snapshots[c.id]=ns.copy()
        missing=set(exports)-saved
        if missing:
            raise RuntimeError(f'Unexported notebook figures: {missing}')
    finally:
        plt.show=old_show
        plt.close('all')
    digest=hashlib.sha256(json.dumps(source,ensure_ascii=False).encode()).hexdigest()
    return NotebookRun(path,ns,snapshots,buffer.getvalue(),digest)

def tex_number(value: float, fmt: str = '.6e') -> str:
    if not np.isfinite(value):
        raise ValueError(f'Non-finite value: {value}')
    text=format(float(value),fmt)
    if 'e' in text.lower():
        mantissa,exponent=text.lower().split('e')
        text=mantissa+r'\times 10^{'+str(int(exponent))+'}'
    return r'\ensuremath{'+text+'}'

def write_values(chapter: int | str, run: NotebookRun, values: dict):
    """values maps macro names to (value, format, source description)."""
    folder = f'chap{chapter:02d}' if isinstance(chapter, int) else {'B':'appendixB', 'C':'appendixC', 'A':'appendixA'}[chapter]
    gen=BOOK_ROOT/'generated'/folder; gen.mkdir(parents=True,exist_ok=True)
    lines=['% Auto-generated from the distributed notebook. Do not hand-edit.']
    raw={}; origins={}
    for macro,(value,fmt,origin) in values.items():
        lines.append('\\newcommand{\\'+macro+'}{'+tex_number(value,fmt)+'}')
        raw[macro]=float(value); origins[macro]=origin
    (gen/'values.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (gen/'values.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (gen/'provenance.json').write_text(json.dumps({'notebook':run.path.name,'code_sha256':run.source_sha256,'value_sources':origins},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (gen/'notebook_output.txt').write_text(run.stdout,encoding='utf-8')
    print(f'Chapter {chapter}: {len(values)} values from {run.path.name}')
