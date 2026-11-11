from notebook_source import run_notebook, write_values, require_snapshot
import numpy as np

# Notebook 2 cell IDs used for figures and value extraction.
CELL_POTENTIAL = 'e5a8ba19'          # Main potential and potential-error figures
CELL_POISSON_CONV = 'e10fbd83'       # Poisson-solver convergence
CELL_DIFF_EXAMPLE = '71b59b90'       # Differentiation comparison
CELL_DIFF_CONV = 'ca83d994'          # Differentiation convergence
CELL_GRAVITY_COMPARE = '6a6eee6f'    # Gravity from two numerical paths
CELL_PIPELINE_CONV = '6e3eec9e'      # Full rho -> Phi -> g convergence
CELL_BOUNDARY = 'ce078fdb'           # Boundary-condition comparison
CELL_CUSP_CONV = '8cf03a36'          # Hernquist cusp convergence
CELL_MAIN_SOLVE = '7853af4d'         # Main N=200 Poisson solve namespace

run=run_notebook(2,{
 (CELL_POTENTIAL,0):'ch02_potential.pdf', (CELL_POTENTIAL,1):'ch02_potential_error.pdf',
 (CELL_POISSON_CONV,0):'ch02_poisson_convergence.pdf', (CELL_DIFF_EXAMPLE,0):'ch02_differentiation.pdf',
 (CELL_DIFF_CONV,0):'ch02_differentiation_convergence.pdf', (CELL_GRAVITY_COMPARE,0):'ch02_gravity_compare.pdf',
 (CELL_PIPELINE_CONV,0):'ch02_pipeline_convergence.pdf', (CELL_BOUNDARY,0):'ch02_pointmass_boundary.pdf',
 (CELL_CUSP_CONV,0):'ch02_cusp_convergence.pdf',
})
s=run.state; main=require_snapshot(run, CELL_MAIN_SOLVE, 'main N=200 Poisson solve'); v={}
v['chtwoDrNTwoHundred']=(main['r'][1]-main['r'][0],'.6f','main grid dr')
v['chtwoPhiErrNTwoHundred']=(np.max(np.abs(main['phi_num']-main['phi_exact'])),'.6e','max absolute potential error, main grid')
v['chtwoResidualNTwoHundred']=(np.max(np.abs(main['residual'])),'.6e','max absolute residual, main grid')
for macro,key in [('PoissonOrder','order_phi'),('ForwardOrder','order_forward'),('BackwardOrder','order_backward'),('CentralOrder','order_central'),('PipelineOrder','order_full'),('CuspOrder','order_cusp'),('MassFullOrder','order_mass_full'),('MassFixedOrder','order_mass_fixed')]:
    v['chtwo'+macro]=(s[key],'.3f',key)
v['chtwoGravityErrNTwoHundred']=(s['err_full'],'.6e','err_full')
v['chtwoMassGravityErrNTwoHundred']=(s['err_mass_all'],'.6e','err_mass_all')
v['chtwoMassGravityFixedErrNTwoHundred']=(s['err_mass_fixed'],'.6e','err_mass_fixed')
bc=require_snapshot(run, CELL_BOUNDARY, 'boundary-condition comparison'); scale=bc['G']*bc['M']/bc['a']
v['chtwoPointMassErrNTwoHundred']=(np.max(np.abs(bc['phi_pm']-bc['phi_pm_exact']))/scale,'.6e','point-mass boundary error on main grid')
v['chtwoBoundaryShift']=(bc['shift_boundary']/scale,'.6e','shift_boundary/(GM/a)')
v['chtwoBoundaryShiftResidual']=(np.max(np.abs(bc['delta_phi']-bc['shift_boundary']))/scale,'.3e','max deviation from constant boundary shift')
v['chtwoBoundaryForceChange']=(np.max(np.abs(bc['delta_g']))/(bc['G']*bc['M']/bc['a']**2),'.3e','max boundary-induced force difference')
words={50:'Fifty',100:'OneHundred',200:'TwoHundred',400:'FourHundred',800:'EightHundred'}
for N,err,radius in zip(s['N_full'],s['err_full_grid'],s['r_errmax']):
    tag=words[int(N)]
    v['chtwoFullErrN'+tag]=(err,'.6e',f'pipeline max error N={N}')
    v['chtwoFullRmaxN'+tag]=(radius/s['a'],'.3f',f'pipeline error location N={N}')
for N,err in zip(s['N_cusp'],s['err_cusp']):
    v['chtwoCuspErrN'+words[int(N)]]=(err,'.6e',f'cusp error N={N}')
for i,row in enumerate(s['boundary_records']):
    tag=['Five','Ten','Twenty','Forty'][i]
    v['chtwoShiftAt'+tag]=(row[2],'.6e',f'boundary_records[{i}].abs_shift')
    v['chtwoTotalAt'+tag]=(row[3],'.6e',f'boundary_records[{i}].total_error')
write_values(2,run,v)
