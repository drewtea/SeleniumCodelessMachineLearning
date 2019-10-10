import os
from pathlib import Path
current_dir = Path.cwd()
home_dir = Path.home()
g = Path.cwd().parents[1]/ 'reports' / 'logs'
print(current_dir)
print(home_dir)
print(g)