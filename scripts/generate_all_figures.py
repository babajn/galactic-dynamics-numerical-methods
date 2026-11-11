"""Regenerate all textbook figures and values from the bundled notebooks."""
from pathlib import Path
import os, runpy, sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
for chapter in range(1,4):
    name=f'figures_master_chap{chapter:02d}.py'
    print(f'=== {name} ===',flush=True)
    runpy.run_path(str(HERE/name),run_name='__main__')
for name in ['figures_master_appendixA.py', 'figures_master_appendixB.py', 'figures_master_appendixC.py']:
    print(f'=== {name} ===', flush=True)
    runpy.run_path(str(HERE/name), run_name='__main__')
print('=== figure_appendixD_fill_in.py ===', flush=True)
runpy.run_path(str(HERE/'figure_appendixD_fill_in.py'), run_name='__main__')
