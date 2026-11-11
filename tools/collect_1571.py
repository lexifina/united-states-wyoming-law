"""Private bounded bulk entrypoint: official listing -> full volumes -> gated part candidates."""
import runpy
from pathlib import Path

if __name__=='__main__':
    root=Path(__file__).resolve().parent
    runpy.run_path(str(root/'collect_range_1571.py'),run_name='__main__')
    runpy.run_path(str(root/'parse_depth_1571.py'),run_name='__main__')
