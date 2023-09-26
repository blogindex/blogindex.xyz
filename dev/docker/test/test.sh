#!/usb/bin/env bash
cd /blogindex.xyz/
source venv/bin/activate
pip install -r requirements.txt
pytest
