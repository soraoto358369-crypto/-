"""watch-copy.py — 台本.md を監視して、保存のたびに index.html へ自動反映する
使い方: python watch-copy.py <site_dir> [<台本.md>]
止め方: Ctrl+C
"""
import os, sys, time, subprocess
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    site = sys.argv[1].rstrip("/\\"); md = sys.argv[2] if len(sys.argv) > 2 else os.path.join(site + "-src", "台本.md")
    here = os.path.dirname(os.path.abspath(__file__)); apply = os.path.join(here, "apply-copy.py")
    print(f"監視中: {md} → {site}/index.html（保存すると反映。Ctrl+C で終了）", flush=True)
    last = 0
    while True:
        try: mt = os.path.getmtime(md)
        except OSError: mt = 0
        if mt and mt != last:
            last = mt
            r = subprocess.run([sys.executable, apply, site, md], capture_output=True, text=True, encoding="utf-8")
            print(time.strftime("%H:%M:%S"), (r.stdout or r.stderr).strip(), flush=True)
        time.sleep(1)

if __name__ == "__main__":
    main()
