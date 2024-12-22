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

### In an existing environment

Use the tool of your choice, for example `uv`, to add `emtd` to your environment:

```shell
uv add emtd
```

### In a new environment

The following example assumes that you are using `uv`. Other ways should work in a similar fashion.

First setup a new environment:

```shell
uv venv
```

Then activate it:

**Windows:**

```shell
.venv\Scripts\activate
```

**Linux:**

```shell
source .venv/bin/activate
```

And finally add `emtd` to your environment:

```shell
uv add emtd
```

### Basic usage

Now you can run the following examplatory code:

```python
from emtd import EMTD

# Use `./tmpdir` to store intermediate results.
data = EMTD(target_dir="tmpdir")

# Get all available technologies in 2030.
data.technologies(2030)

# Get all available parameters for the technology "solar" in 2030.
data.parameters(2030, "solar")

# Get the "lifetime" of "solar" in 2030.
res = data.get(2030, "solar", "lifetime")

# Try out:
res["value"]
res["unit"]
res["source"]
```

## Reproducibility

To make sure everyone using your code will get the same results from `emtd`, it is advised to fix the data set to a 
specific version. Consult the [release page](https://github.com/PyPSA/technology-data/releases) for available versions,
then make sure to initialize using (e.g.):

```python
data = EMTD(target_dir="tmpdir", version="v0.6.2")
```

Make sure to include the `v` in the version string. Passing `"latest"` will put you on the current latest version of the
technology data repository. Be aware that this can change anytime, and the next time you initialize `emtd`, it will try
to update.

## Logging

To get more information about what is happening, you can change the default logging level, by adding the following code:

```python
import logging

logging.basicConfig(level=logging.INFO)
```

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

```console
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

```console
subprocess.CalledProcessError: Command '['git', '-C', PosixPath('tmpdir'), 'pull']' returned non-zero exit status 1.
```

This error indicates an error during executing `git pull`. If you've previously used a `target_dir = "tmpdir` and
pulled, e.g., `version="v0.6.1"`, and are now using `EMTD(target_dir="tmpdir")` (without version), the pull will fail;
make sure to stick to one version, or use a different `target_dir` for managing different versions.

## Developing `emtd`

This is a rough outline of how to get started with developing `emtd`:

1. Clone this repository: `git clone https://github.com/sstroemer/emtd.git`.
2. Create a new environment: `uv venv`.
3. Activate the environment: `source .venv/bin/activate`.
4. Install the dependencies: `uv sync`.
5. If you are using VSCode, PyCharm, etc., select `.venv/bin/python` as the interpreter.

Depending on how you work with it, consider using `uv pip install -e .`.

### Updating packages

Currently the proposed way is:

```shell
uv lock --upgrade
uv sync
```
