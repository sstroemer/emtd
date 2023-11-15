import os
import re
import logging
from typing import Optional

from pathlib import Path
import subprocess
import tempfile

import yaml
import pandas as pd


class EMTD:
    """
    The EMTD (Energy Modeling Technology Data) class is designed for managing and processing technology data
    for energy modeling. It provides functionalities for cloning the "technology data" repository of the PyPSA team,
    https://github.com/PyPSA/technology-data, running snakemake workflows, and retrieving specific technology parameters
    for given years.

    Methods:
        EMTD(target_dir: Optional[str], params: Optional[dict], version: str): Initializes the EMTD object.

        technologies(self, year: int):
                Retrieves the unique technologies available for a given year.
        parameters(self, year: int, tech: str):
                Retrieves the unique parameters for a given technology in a specific year.
        get(self, year: int, tech: str, param: str):
                Retrieves detailed data for a specific technology parameter in a given year.

    Example Usage:
        ```python
        from emtd import EMTD

        # Use `./tmpdir` to store intermediate results.
        data = EMTD("tmpdir")

        # Get all available parameters for the technology "solar" in 2030.
        data.parameters(2030, "solar")

        # Get the "lifetime" of "solar" in 2030.
        res = data.get(2030, "solar", "lifetime")

        # Try out:
        res["value"]
        res["unit"]
        res["source"]
        ```
    """

    def __init__(
        self, target_dir: Optional[str] = None, params: Optional[dict] = None, version: str = "latest"
    ) -> None:
        """
        Initializes the EMTD object with an optional target directory and parameters.

        Args:
            target_dir (Optional[str]): The directory to store and manage the downloaded technology data.
            params (Optional[dict]): Parameters to be used in the snakemake workflow, overwriting the defaults.
            version (str):
                The data set version to use (e.g. "v0.6.2"); "latest" (the default) uses the most up-to-date version,
                but may result in different data each time you call it. Consider fixing to a specific version!
        """
        self._logger = logging.getLogger("emtd")
        self._results = dict()

        if version == "latest":
            self._logger.warning(
                "Consider binding to a specific version of the 'technology-data'; consult 'Reproducability' in the README.md"
            )

        if target_dir is None:
            self._logger.warning("Consider specifying 'target_dir' to properly re-use previous work during snakemake")
        self._prepare(Path(target_dir or tempfile.TemporaryDirectory().name), params or dict(), version)

    def technologies(self, year: int) -> list:
        """
        Retrieves a list of unique technologies available for a given year.

        Args:
            year (int): The year for which to retrieve technology data.

        Returns:
            List[str]: A list of unique technology names,  or an empty list on error.
        """
        if year not in self._results:
            self._logger.error("No results for year %d", year)
            return list()
        return list(self._results[year].technology.unique())

    def parameters(self, year: int, tech: str) -> list:
        """
        Retrieves a list of unique parameters for a given technology and year.

        Args:
            year (int): The year for which to retrieve parameter data.
            tech (str): The technology for which to retrieve parameter data.

        Returns:
            List[str]: A list of unique parameter names, or an empty list on error.
        """
        if year not in self._results:
            self._logger.error("No results for [year=%d, tech=%s]", year, tech)
            return list()

        ret = self._results[year]
        ret = ret.loc[ret.technology == tech]
        return list(ret.parameter.unique())

    def get(self, year: int, tech: str, param: str) -> dict:
        """
        Retrieves detailed data for a specific technology parameter in a given year.

        Args:
            year (int): The year for which to retrieve the data.
            tech (str): The technology for which to retrieve the data.
            param (str): The specific parameter to retrieve.

        Returns:
            dict: A dictionary containing the "value", "unit", "source", and "further description" of the parameter.
                  Returns an empty dict on error.
        """
        if (tech not in self.technologies(year)) or (param not in self.parameters(year, tech)):
            self._logger.error("No results for [year=%d, tech=%s, param=%s]", year, tech, param)
            return dict()

        ret = self._results[year]
        ret = ret.loc[
            (ret.technology == tech) & (ret.parameter == param), ["value", "unit", "source", "further description"]
        ]
        if len(ret) == 0:
            self._logger.error("Zero (0) results for [year=%d, tech=%s, param=%s]", year, tech, param)
            return dict()
        if len(ret) > 1:
            self._logger.error("Ambiguous results for [year=%d, tech=%s, param=%s]", year, tech, param)
            return dict()

        return ret.iloc[0].to_dict()

    def _prepare(self, target_dir: Path, params: dict, version: str) -> None:
        self._logger.info("Using temporary directory '%s' to manage 'technology-data'", target_dir)

        self._clone_repository("https://github.com/PyPSA/technology-data.git", target_dir, version)

        with open(target_dir / "__config.yaml", "w") as f:
            yaml.dump(params, f)

        self._run_snakemake(target_dir)

        self._logger.info("Cleaning up temporary config file")
        os.remove(target_dir / "__config.yaml")
        self._logger.warning("The temporary directoy is not being deleted and could take up significant space")

        self._logger.info("Parsing resulting outputs of snakemake workflow")
        self._results = {
            y: pd.read_csv(target_dir / "outputs" / f"costs_{y}.csv") for y in self._list_results(target_dir, "costs")
        }

    def _clone_repository(self, repo_url: str, target_dir: str, version: str) -> None:
        if not os.path.exists(target_dir):
            self._logger.info("Cloning 'technology-data")
            os.makedirs(target_dir)
            if version == "latest":
                subprocess.run(["git", "clone", repo_url, target_dir], check=True, capture_output=True, text=True)
            else:
                subprocess.run(
                    ["git", "clone", repo_url, "--branch", version, target_dir],
                    check=True,
                    capture_output=True,
                    text=True,
                )
        else:
            self._logger.info("Updating 'technology-data'")
            if version == "latest":
                subprocess.run(["git", "-C", target_dir, "pull"], check=True, capture_output=True, text=True)
            else:
                subprocess.run(
                    ["git", "-C", target_dir, "pull", repo_url, version], check=True, capture_output=True, text=True
                )

    def _run_snakemake(self, target_dir: Path) -> None:
        self._logger.info("Starting snakemake workflow")
        current_working_directory = os.getcwd()
        os.chdir(target_dir)
        subprocess.run(["snakemake", "-j1", "--configfile", "__config.yaml"], capture_output=True, text=True)
        os.chdir(current_working_directory)
        self._logger.info("Snakemake workflow done")

    def _list_results(self, target_dir: Path, prefix: str) -> list:
        years = []
        for filename in os.listdir(target_dir / "outputs"):
            match = re.findall(rf"{prefix}_(\d{{4}}).csv", filename)
            if match:
                years.append(int(match[0]))
        self._logger.info("Found a total of %d applicable output files", len(years))
        return years
