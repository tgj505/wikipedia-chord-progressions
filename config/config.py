from pathlib import Path
import os

ROOT_PATH = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
DATA_PATH = ROOT_PATH / 'data'
SRC_PATH = ROOT_PATH / 'src'
VISUALIZATION_PATH = ROOT_PATH / 'visualizations'