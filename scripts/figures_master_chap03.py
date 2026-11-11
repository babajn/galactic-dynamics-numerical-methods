from notebook_source import run_notebook, write_values

# Stable IDs retained from the source notebook; only document allocation changed.
run = run_notebook(3, {
 ('f9b95253', 0): 'ch03_circular_orbit.pdf',
 ('b703ab83', 0): 'ch03_convergence.pdf',
 ('cc846e87', 0): 'ch03_eccentric_orbit.pdf',
 ('5fb114f1', 0): 'ch03_energy_error.pdf',
 ('0ed402f9', 0): 'ch03_angular_momentum_error.pdf',
 ('980221c8', 0): 'ch03_long_term_energy.pdf',
})
s = run.state
v = {}
for macro, key in [('OmegaPlummer', 'Omega0'), ('VcPlummer', 'vc0'), ('PeriodPlummer', 'T0')]:
    v['chthree' + macro] = (s[key], '.8f', key)
for macro, key in [('Euler', 'Euler'), ('Leapfrog', 'Leapfrog'), ('RKFour', 'RK4')]:
    v['chthreeOrder' + macro] = (s['orders'][key], '.3f', 'orders[' + key + ']')
for macro, key in [('Leapfrog', 'Leapfrog'), ('RKFour', 'RK4')]:
    v['chthreeLongEnergy' + macro] = (s['long_results'][key][-1], '.6e', 'long_results[' + key + '][-1]')
for macro, key in [('Euler', 'Euler'), ('Leapfrog', 'Leapfrog'), ('RKFour', 'RK4')]:
    for quantity, field in [('Energy', 'energy'), ('Lz', 'Lz')]:
        v['chthreeShortMax' + quantity + macro] = (s['short_max_errors'][key][field], '.3e', f'short_max_errors[{key}][{field}]')
for macro, key in [('Leapfrog', 'Leapfrog'), ('RKFour', 'RK4')]:
    v['chthreeLongEarlyMax' + macro] = (s['long_max_errors'][key]['early'], '.3e', f'long_max_errors[{key}][early], same long run to 20T0')
    v['chthreeLongMax' + macro] = (s['long_max_errors'][key]['all'], '.3e', f'long_max_errors[{key}][all], same long run to 1000T0')
write_values(3, run, v)
