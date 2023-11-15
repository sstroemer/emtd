1. run `black emtd/`
2. commit & push everything
3. `poetry version ___` (major, minor, patch)
4. change the version in `emtd/__init__.py`
5. Update CHANGELOG.md
6. commit & push "prep for v_._._"
7. `poetry build`
8. `poetry publish`
9. (optional) tag the final commit in the repo, with the "v_._._" tag

Remember to follow [Semantic Versioning](https://semver.org/) and
[keep a changelog](https://keepachangelog.com/en/1.1.0/).