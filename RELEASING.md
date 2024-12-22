# Releasing

To release a new version of `emtd`, follow these steps:

1. Run `ruff format`
2. Commit & push everything
3. Update the package's version in `pyproject.toml`
4. Update CHANGELOG.md
5. Commit & push `prep for v_._._` (versio & changelog changes)
6. [Trigger a new release on GitHub](https://github.com/sstroemer/emtd/releases/new)

Remember to follow [Semantic Versioning](https://semver.org/) and
[keep a changelog](https://keepachangelog.com/en/1.1.0/).