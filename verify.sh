#!/usr/bin/env bash
# Verify a VM/laptop is ready for the High-Performance Python labs.
# Usage:  bash verify.sh
set -u
pass=0; fail=0
ok()  { echo "  [PASS] $1"; pass=$((pass+1)); }
bad() { echo "  [FAIL] $1"; fail=$((fail+1)); }

echo "== System =="
uname -srm
python3 --version 2>/dev/null && ok "python3 present" || bad "python3 not found"
python3 -m pip --version >/dev/null 2>&1 && ok "pip present" || bad "pip missing (install python3-pip)"

echo "== Python packages =="
for mod in numpy matplotlib IPython Cython; do
  if python3 -c "import $mod" 2>/dev/null; then
    ver=$(python3 -c "import $mod; print(getattr($mod,'__version__','?'))" 2>/dev/null)
    ok "$mod $ver"
  else
    bad "$mod missing (pip install -r requirements.txt)"
  fi
done

echo "== C compiler + Python headers =="
command -v gcc >/dev/null 2>&1 && ok "gcc $(gcc -dumpversion)" || bad "gcc missing (install build-essential)"
python3 -c "import os,sysconfig; exit(0 if os.path.exists(os.path.join(sysconfig.get_path('include'),'Python.h')) else 1)" \
  && ok "Python.h present" || bad "Python headers missing (install python3-dev)"

echo "== Matplotlib renders headless =="
if python3 - <<'PY' 2>/dev/null
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.plot([1, 2, 3]); plt.savefig("/tmp/_mpl_test.png")
PY
then ok "matplotlib savefig works"; else bad "matplotlib savefig failed"; fi

echo "== Cython end-to-end build (the real compiler test) =="
tmp=$(mktemp -d)
cat > "$tmp/hello.pyx" <<'PYX'
def add(int a, int b):
    return a + b
PYX
cat > "$tmp/setup.py" <<'PY'
from setuptools import setup
from Cython.Build import cythonize
setup(ext_modules=cythonize("hello.pyx"))
PY
if ( cd "$tmp" && python3 setup.py build_ext --inplace >/tmp/_cy.log 2>&1 \
     && python3 -c "import hello; assert hello.add(2,3)==5" ); then
  ok "Cython compiles and imports (gcc + headers + cython all OK)"
else
  bad "Cython build failed -- see /tmp/_cy.log"
fi
rm -rf "$tmp"

echo
echo "== Summary: $pass passed, $fail failed =="
if [ "$fail" -eq 0 ]; then
  echo "VM is READY for the labs."
else
  echo "VM is NOT ready -- fix the [FAIL] items above."; exit 1
fi