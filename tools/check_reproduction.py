#!/usr/bin/env python3
"""Check the reproducible *derived* claims, not authenticity of upstream source rasters."""
import json,math
from pathlib import Path
d=json.loads(Path('results/reproduced_summary.json').read_text())
n=d['ioda_plot_proxy']['central_divergence_percentage_points']
p=d['origin_concentration']['prefix_hhi']
a=d['origin_concentration']['address_space_hhi']
assert math.isclose(n,50.8144,abs_tol=.02),n
assert math.isclose(p,.623822,abs_tol=.00002),p
assert math.isclose(a,.920747,abs_tol=.00002),a
assert d['ioda_plot_proxy']['sensitivity']['n_valid_combinations']==20250
print('PASS: derived evidence reproduction; not a native-data validation')
