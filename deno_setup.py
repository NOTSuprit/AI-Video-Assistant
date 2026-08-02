import os
import stat
import zipfile
import io
import requests

DENO_PATH = "/tmp/deno"

def ensure_deno():
    if os.path.exists(DENO_PATH):
        return DENO_PATH

    url = "https://github.com/denoland/deno/releases/latest/download/deno-x86_64-unknown-linux-gnu.zip"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        z.extract("deno", "/tmp")

    st = os.stat(DENO_PATH)
    os.chmod(DENO_PATH, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    return DENO_PATH