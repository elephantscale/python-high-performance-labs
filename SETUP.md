# Lab Environment Setup

Requirements for the **Writing High-Performance Python Code** labs.
One environment per student (VM, container, or laptop).

## Base

- **OS:** Linux (Ubuntu recommended — the labs were built and verified there).
  macOS works too; Windows works with the appropriate C compiler (see below).
- Modest CPU/RAM — the benchmarks are lightweight.

## System packages

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-dev build-essential git
```

- `build-essential` (gcc) **and** `python3-dev` are required for the **Cython lab**,
  which compiles a C extension (`python setup.py build_ext --inplace`). Without a
  C compiler and the Python headers, that lab will not build.
- On **macOS**: install the Xcode command-line tools (`xcode-select --install`).
- On **Windows**: install the Microsoft C++ Build Tools.

## Python packages

```bash
pip install -r requirements.txt
```

Installs: `numpy`, `matplotlib`, `ipython`, `cython`, `setuptools`.

Tested with Python 3.12 (any 3.10+ is fine).

## Notes

- **Plotting:** the NumPy lab's `plot_benchmark.py` saves charts to PNG and runs
  headless (it falls back to a non-GUI backend when there is no display, so it
  works over SSH). If you want plot windows to pop up interactively, the VM needs
  a desktop/GUI; otherwise students view the saved `.png` files.
- **Browser:** a modern browser (Chrome) for the slides / any notebook use.
- **Not required:** `py-spy`, `Scalene`, `memray`, `pyprof2calltree`, `kcachegrind`
  are mentioned in the slides but are not needed to run the labs.

## Quick sanity check

Run the included verifier — it checks every dependency and actually compiles a
Cython module (the real test of the compiler).

**Any OS (recommended):**

```bash
python verify.py       # Windows
python3 verify.py      # macOS / Linux
```

**Linux/macOS bash alternative:**

```bash
bash verify.sh
```

Either prints a PASS/FAIL line per check and ends with **"...READY for the labs."**
when everything is in place.

### Windows note

The **Cython lab** needs a C compiler. On Windows that is the
**Microsoft C++ Build Tools** (Visual Studio Build Tools → "Desktop development
with C++"), not gcc. `verify.py` will tell you if it is missing. The other seven
labs are pure Python and run on Windows without it.