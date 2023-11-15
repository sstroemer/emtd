1. run `black emtd/`
2. commit & push everything
3. `poetry version ___` (major, minor, patch)
4. change the version in `emtd/__init__.py`
5. commit & push "prep for v_._._"
6. `poetry build`
7. `poetry publish`