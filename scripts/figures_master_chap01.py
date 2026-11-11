from pathlib import Path
from notebook_source import run_notebook, write_values, save_figure
import numpy as np
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / 'textbook' / 'figures'
OUT.mkdir(parents=True, exist_ok=True)

from figure_layouts import OI, export_quadrature_diagrams

# Preserve the existing numeric-figure typography; only the geometry panels
# use their own temporary rc_context in figure_layouts.py.
plt.rcParams.update({'font.size': 10, 'axes.labelsize': 10, 'axes.titlesize': 10, 'legend.fontsize': 9, 'xtick.labelsize': 9, 'ytick.labelsize': 9, 'pdf.fonttype': 42, 'ps.fonttype': 42})

# These four panels explain geometry only. The numerical examples below still
# come exclusively from the distributed Notebook 1.
export_quadrature_diagrams(save_figure)

# Notebook 1 cell IDs used for textbook exports.
# If a notebook cell is recreated by copy/paste, Jupyter may assign a new ID;
# update only these named constants rather than searching the export logic.
CELL_PLUMMER_PLOTS = '20078d44'      # Density and dM/dr figures (two outputs)
CELL_CONVERGENCE = 'a3e78261'        # Four-rule convergence figure
CELL_MASS_PROFILE = '6cd01623'       # Enclosed-mass profile
CELL_CIRCULAR_SPEED = 'ec8682fb'     # Circular-speed curve
CELL_MASS_MODELS = 'dad70a4b'        # Hernquist/NFW comparison

# Numerical figures and values come from exactly the shipped Notebook 1.
run = run_notebook(1, {
    (CELL_PLUMMER_PLOTS,0): 'ch01_plummer_density.pdf',
    (CELL_PLUMMER_PLOTS,1): 'ch01_mass_integrand.pdf',
    (CELL_CONVERGENCE,0): 'ch01_convergence.pdf',
    (CELL_MASS_PROFILE,0): 'ch01_enclosed_mass.pdf',
    (CELL_CIRCULAR_SPEED,0): 'ch01_circular_speed.pdf',
    (CELL_MASS_MODELS,0): 'ch01_mass_models.pdf',
})
s = run.state
err_round = np.array(s['err_large'])
positive = err_round > 0
fig,ax = plt.subplots(figsize=(6.0,4.0))
ax.loglog(s['N_large'][positive], err_round[positive], 'o-', color=OI['purple'], label='Measured nonzero error')
ax.set(xlabel='Number of intervals',ylabel='Absolute mass error',title='Round-off and Simpson integration')
ax.grid(alpha=0.25,which='both'); ax.legend()
save_figure(fig,'ch01_roundoff.pdf')
v = {}
for tag,key in [('MExactA','m_exact_eval'),('LeftNForty','m_left'),('MidNForty','m_mid'),('TrapNForty','m_trap'),('SimpsonNForty','m_simp')]:
    v['chone'+tag]=(s[key],'.12f',key)
for tag,key in [('Left','m_left'),('Mid','m_mid'),('Trap','m_trap'),('Simpson','m_simp')]:
    v['chone'+tag+'ErrNForty']=(abs(s[key]-s['m_exact_eval']),'.3e',key+' - m_exact_eval')
for tag,key in [('Left','Left rectangle'),('Mid','Midpoint'),('Trap','Trapezoidal'),('Simpson','Simpson')]:
    v['choneOrder'+tag]=(s['orders'][key],'.3f','orders['+key+']')
v.update({
 'choneMachineEps':(np.finfo(float).eps,'.3e','numpy float epsilon'),
 'choneMassRmaxTwentyNum':(s['m_num'][-1],'.12f','m_num[-1]'),
 'choneMassRmaxTwentyExact':(s['m_exact'][-1],'.12f','m_exact[-1]'),
 'choneVcPeakRadiusNumerical':(s['r'][s['i_peak']]/s['a'],'.6f','r[i_peak]/a'),
 'choneVcPeakNumerical':(s['vc_num'][s['i_peak']],'.6f','vc_num[i_peak]'),
 'choneVcPeakRadiusAnalytic':(np.sqrt(2.0),'.6f','analytic sqrt(2)'),
 'choneVcPeakAnalytic':(np.sqrt(2/(3*np.sqrt(3))),'.6f','analytic normalized maximum'),
})
write_values(1,run,v)
