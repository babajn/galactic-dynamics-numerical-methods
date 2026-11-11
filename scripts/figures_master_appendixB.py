from notebook_source import run_notebook, write_values, save_figure
from figure_layouts import export_sparse_explanation
import numpy as np

run = run_notebook('B', {
 ('800b2cf7', 0): 'appB_mn_density.pdf',
 ('5e15380e', 0): 'appB_mn_potential.pdf',
 ('5e15380e', 1): 'appB_mn_error.pdf',
 ('2fc1b808', 0): 'appB_poisson2d_convergence.pdf',
})
s = run.state
_, _, _, A_demo, _, _ = s['solve_mn_poisson'](NR=4, NZ=5, Rmax=5.0, Zmax=4.0, G=s['G'], M=s['Mmn'], a=s['amn'], b=s['bmn'])
export_sparse_explanation(A_demo, save_figure)
v = {
 'appBOrderTwoD': (s['order_2d'], '.3f', 'order_2d'),
 'appBNUnknown': (s['A_mn'].shape[0], '.0f', 'A_mn.shape[0]'),
 'appBNNZ': (s['A_mn'].nnz, '.0f', 'A_mn.nnz'),
 'appBMatrixDensity': (s['A_mn'].nnz / s['A_mn'].shape[0]**2, '.3e', 'A_mn.nnz / shape[0]**2'),
 'appBPhiError': (s['err_phi'], '.6e', 'err_phi'),
 'appBResidual': (np.max(np.abs(s['residual'])), '.6e', 'max(abs(residual))'),
}
write_values('B', run, v)
