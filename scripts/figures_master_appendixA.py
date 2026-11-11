from notebook_source import run_notebook, write_values, save_figure, require_snapshot
import matplotlib.pyplot as plt

run = run_notebook('A', {
 ('1a994d8a', 0): 'appA_mass_profile.pdf',
 ('563e8661', 0): 'appA_mass_convergence.pdf',
 ('79aab8da', 0): 'appA_rotation_curve.pdf',
})
s = run.state
p = require_snapshot(run, 'd4899c75', 'exponential-disk profile arrays')
OI = s['OI']
fig, ax = plt.subplots(figsize=(6.0, 4.0))
ax.plot(p['R_plot']/p['Rd'], p['Sigma_plot']/p['Sigma0'], color=OI['blue'], label=r'$\Sigma/\Sigma_0$')
ax.plot(p['R_plot']/p['Rd'], p['dMdR_plot']/(p['Md']/p['Rd']), '--', color=OI['vermillion'], label=r'$(dM/dR)/(M_d/R_d)$')
ax.set(xlabel=r'$R/R_d$', ylabel='Normalized profile', title='Exponential disk')
ax.legend(); ax.grid(alpha=.25); save_figure(fig, 'appA_exponential_profiles.pdf')
v = {}
for macro, key in [('MassRmaxNum', 'M_num'), ('MassRmaxExact', 'M_exact')]:
    v['appA' + macro] = (s[key][-1] / s['Md'], '.10f', key + '[-1]/Md')
v['appAMassOrder'] = (s['order_mass'], '.3f', 'order_mass')
for macro, key in [('DiskPeakR', 'Rpeak_disk'), ('SphPeakR', 'Rpeak_sph')]:
    v['appA' + macro] = (s[key] / s['Rd'], '.3f', key + '/Rd')
for macro, key in [('DiskPeakVTwo', 'vc2peak_disk'), ('SphPeakVTwo', 'vc2peak_sph')]:
    v['appA' + macro] = (s[key] / s['scale_v2'], '.4f', key + '/scale_v2')
write_values('A', run, v)
