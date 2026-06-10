# Python High-Performance — Labs

Hands-on labs for the **Writing High-Performance Python Code** course.

## Verify your environment

Open this page in the browser **on your VM/laptop**, then copy the command below
into a terminal (the **Anaconda Prompt** if you use Anaconda):

```
python verify.py
```

Don't have the file yet? Get it one of these ways:

```
git clone https://github.com/elephantscale/python-high-performance-labs
cd python-high-performance-labs
python verify.py
```

No git? On this repo's page click **verify.py**, then the **Download raw file**
button, and run it from your Downloads folder:

```
cd %USERPROFILE%\Downloads        (Windows)
python verify.py
```

It prints PASS/FAIL per check and ends with **"READY for the labs."**

## Setup details

See **[SETUP.md](SETUP.md)** for the full requirements (Python 3.10+, numpy,
matplotlib, ipython, cython, and a C compiler for the Cython lab).

## Lab order

See **[lab-assembly.txt](lab-assembly.txt)** for the teaching sequence and which
labs are hands-on, demo, or optional.
