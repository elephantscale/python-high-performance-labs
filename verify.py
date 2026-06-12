#!/usr/bin/env python3
"""Cross-platform readiness check for the High-Performance Python labs.

Run it with:

    python verify.py      (Windows)
    python3 verify.py     (macOS / Linux)

Works on Windows, macOS, and Linux. Checks Python, the lab packages,
headless matplotlib, and actually compiles a Cython module end-to-end
(the real test of the C compiler).
"""
import sys
import os
import platform
import subprocess
import tempfile
import textwrap

passed, failed = [], []


def ok(msg):
    passed.append(msg)
    print(f"  [PASS] {msg}")


def bad(msg):
    failed.append(msg)
    print(f"  [FAIL] {msg}")


print("== System ==")
print(f"  {platform.platform()}")
print(f"  Python {sys.version.split()[0]}  ({sys.executable})")
if sys.version_info >= (3, 10):
    ok("Python 3.10+")
else:
    bad(f"Python too old ({sys.version.split()[0]}); need 3.10+")

print("== Python packages ==")
for mod in ("numpy", "matplotlib", "IPython", "Cython"):
    try:
        m = __import__(mod)
        ok(f"{mod} {getattr(m, '__version__', '?')}")
    except ImportError:
        bad(f"{mod} missing  ->  pip install {mod.lower()}")

print("== Matplotlib renders headless ==")
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.plot([1, 2, 3])
    plt.savefig(os.path.join(tempfile.gettempdir(), "_mpl_test.png"))
    ok("matplotlib savefig works")
except Exception as e:
    bad(f"matplotlib savefig failed: {e}")

print("== Cython end-to-end build (mirrors the Cython lab) ==")
try:
    import Cython  # noqa: F401
    tmp = tempfile.mkdtemp()
    # Uses the same features as the lab: a typed memoryview, boundscheck off,
    # and numpy's include path -- so a PASS means the actual lab will build.
    with open(os.path.join(tmp, "lab_demo.pyx"), "w") as f:
        f.write(textwrap.dedent("""
            import cython

            @cython.boundscheck(False)
            @cython.wraparound(False)
            def csum(double[:] a):
                cdef double s = 0.0
                cdef int i
                for i in range(a.shape[0]):
                    s += a[i]
                return s
        """))
    with open(os.path.join(tmp, "setup.py"), "w") as f:
        f.write(textwrap.dedent("""
            from setuptools import setup
            from Cython.Build import cythonize
            import numpy as np
            setup(ext_modules=cythonize("lab_demo.pyx"),
                  include_dirs=[np.get_include()])
        """))
    build = subprocess.run(
        [sys.executable, "setup.py", "build_ext", "--inplace"],
        cwd=tmp, capture_output=True, text=True)
    if build.returncode == 0:
        chk = subprocess.run(
            [sys.executable, "-c",
             "import numpy as np, lab_demo; "
             "assert abs(lab_demo.csum(np.array([1.0, 2.0, 3.0])) - 6.0) < 1e-9"],
            cwd=tmp, capture_output=True, text=True)
        if chk.returncode == 0:
            ok("Cython lab-style build works (memoryviews + numpy + compiler)")
        else:
            bad("Cython built but run failed: " + chk.stderr.strip()[:200])
    else:
        if platform.system() == "Windows":
            hint = "install Microsoft C++ Build Tools"
        elif platform.system() == "Darwin":
            hint = "run: xcode-select --install"
        else:
            hint = "install build-essential and python3-dev"
        bad(f"Cython build failed  ->  {hint}")
        lines = (build.stderr or build.stdout).strip().splitlines()
        if lines:
            print("        last error: " + lines[-1][:200])
except ImportError:
    bad("Cython not installed  ->  pip install cython")

print()
print(f"== Summary: {len(passed)} passed, {len(failed)} failed ==")
if not failed:
    print("Environment is READY for the labs.")
    sys.exit(0)
else:
    print("Environment is NOT ready -- fix the [FAIL] items above.")
    sys.exit(1)
