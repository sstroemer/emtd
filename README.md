# Energy Modeling Technology Data

This tool provides a slim Python wrapper to access the
["technology-data"](https://github.com/PyPSA/technology-data) data set /
[Snakemake](https://snakemake.readthedocs.io/en/stable/) workflow, maintained by the [PyPSA](https://github.com/PyPSA)
team.

> 🚨 🚨 Please check the license of the [`technology-data` repo](https://github.com/PyPSA/technology-data), especially
regarding the applicable licences of various input (and therefore output) data files. Additional info can be found
starting at [74](https://github.com/PyPSA/technology-data/issues/74) and
[87](https://github.com/PyPSA/technology-data/pull/87). Be aware that this wrapper can in no way guarantee that the data
being pulled from the repository, or the way that is being processed, or the code retrieved from the repository, or any
related information is in accordance with applicable licenses.

## Getting Started

The following example assumes that you are using `conda` to create your environment, and `poetry` to manage your
dependencies. Other ways should work in a similar fashion.

Create an environment (skip if adding to an existing one; choose whatever Python version you want to use), installing
`poetry` (skip if using a global installation or if you are already using `poetry`), initializing your `pyproject.toml`
(consider also using `poetry new` instead of `poetry init` when starting a project), and then add `emtd` to your
dependencies.

```shell
(base) $ conda create -n yourenvname python=3.11 -y
(base) $ conda activate yourenvname

(yourenvname) $ pip install poetry
(yourenvname) $ poetry init
(yourenvname) $ poetry add emtd
```

Now you can run the following examplatory code:

```python
from emtd import EMTD

# Use `./tmpdir` to store intermediate results.
data = EMTD(target_dir="tmpdir")

# Get all available parameters for the technology "solar" in 2030.
data.parameters(2030, "solar")

# Get the "lifetime" of "solar" in 2030.
res = data.get(2030, "solar", "lifetime")

# Try out:
res["value"]
res["unit"]
res["source"]
```

## Reproducability
To make sure everyone using your code will get the same results from `emtd`, it is advised to fix the data set to a 
specific version. Consult the [release page](https://github.com/PyPSA/technology-data/releases) for available versions,
then make sure to initialize using (e.g.):

```python
data = EMTD(target_dir="tmpdir", version="v0.6.2")
```

Make sure to include the `v` in the version string. Passing `"latest"` will put you on the current latest version of the
technology data repository. Be aware that this can change anytime, and the next time you initialize `emtd`, it will try
to update.

## Configuring the Snakemake workflow
To change parameters in the [Snakemake](https://snakemake.readthedocs.io/en/stable/) workflow, pass a `dict` to `EMTD`:

```python
data = EMTD(target_dir="tmpdir", params={"rate_inflation": 0.03})
```

This overwrites the defaults set by ["technology-data"](https://github.com/PyPSA/technology-data), or adds to it if the
respective setting is not specified there. Consult
[technology-data/config.yaml](https://github.com/PyPSA/technology-data/blob/master/config.yaml) for the current settings
or hints at what can be changed. Also, consult their [documentation](https://technology-data.readthedocs.io/en/latest/).

## Common Errors

```
The current project's supported Python range (>=3.9,<4.0) is not compatible with some of the required packages Python requirement:
  - scipy requires Python <3.13,>=3.9, so it will not be satisfied for Python >=3.13,<4.0
```

This, or similar errors, can occur if the `pyproject.toml` (or similar) specifies a too broad range of Python versions,
like:

```toml
[tool.poetry.dependencies]
python = "^3.9"
```

Changing that based on the proposed range (here `<3.13,>=3.9` from `scipy`) to:

```toml
[tool.poetry.dependencies]
python = ">=3.9,<3.13"
```

will fix that.

---

```
subprocess.CalledProcessError: Command '['git', '-C', PosixPath('tmpdir'), 'pull']' returned non-zero exit status 1.
```

This error indicates an error during executing `git pull`. If you've previously used a `target_dir = "tmpdir` and
pulled, e.g., `version="v0.6.1"`, and are now using `EMTD(target_dir="tmpdir")` (without version), the pull will fail;
make sure to stick to one version, or use a different `target_dir` for managing different versions.
