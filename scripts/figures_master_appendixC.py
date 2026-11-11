from notebook_source import run_notebook, write_values
import numpy as np

run = run_notebook('C', {
 ('f5a76b52', 1): 'appC_radial_epicycle.pdf',
 ('f5a76b52', 2): 'appC_vertical_oscillation.pdf',
 ('23faa105', 0): 'appC_mn_orbit.pdf',
 ('a7198727', 0): 'appC_box_orbit.pdf',
 ('a7198727', 1): 'appC_loop_orbit.pdf',
 ('253fbcc7', 0): 'appC_nonaxisym_Lz.pdf',
})
s = run.state
v = {}
for macro, key in [('OmegaAxisym', 'Omega'), ('KappaAxisym', 'kappa'), ('NuAxisym', 'nu_z')]:
    v['appC' + macro] = (s[key], '.6f', key)
for macro, key in [('AxisymMaxEnergy', 'E_ax'), ('AxisymMaxLz', 'Lz_ax'), ('MNMaxEnergy', 'E_mn'), ('MNMaxLz', 'Lz_mn'), ('BoxMaxEnergy', 'E_box'), ('LoopMaxEnergy', 'E_loop')]:
    arr = s[key]
    v['appC' + macro] = (np.max(np.abs((arr - arr[0]) / abs(arr[0]))), '.3e', key + ' max normalized change')
for macro, key in [('MNEnergyInitial', 'E_mn'), ('BoxEnergy', 'E_box'), ('LoopEnergy', 'E_loop')]:
    v['appC' + macro] = (s[key][0], '.8f', key + '[0]')
for macro, key in [('Box', 'L_box'), ('Loop', 'L_loop')]:
    v['appC' + macro + 'LzMin'] = (s[key].min() / (s['rc_na'] * s['v0_na']), '.4f', key + '.min() / (rc_na * v0_na)')
    v['appC' + macro + 'LzMax'] = (s[key].max() / (s['rc_na'] * s['v0_na']), '.4f', key + '.max() / (rc_na * v0_na)')
# Additional checks introduced in rev49: same equations, fixed integration interval.
for i, suffix in enumerate(['One', 'Two', 'Three']):
    v['appCSelfDiff' + suffix] = (s['self_diffs'][i], '.3e', f'self_diffs[{i}]')
    if i < 2:
        v['appCSelfOrder' + suffix] = (s['p_self'][i], '.3f', f'p_self[{i}]')
    for col, axis in enumerate(['R', 'Z']):
        for tag, key in [('Coarse', 'amp_error_coarse'), ('Fine', 'amp_error_fine')]:
            v['appCAmp' + axis + tag + suffix] = (s[key][i, col], '.5f', f'{key}[{i}, {col}]')
write_values('C', run, v)
