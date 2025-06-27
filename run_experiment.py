#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "code" / "scraper"))

from main import main

if __name__ == "__main__":
    main()
