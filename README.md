# ast

Research notes for the antimicrobial susceptibility testing (AST) project.

## Building the docs

This research notebook is built on the [`sphinx`](https://www.sphinx-doc.org/en/master/) documentation generator. While you can read the `.rst` files directly (they are human readable), building
the research docs with `sphinx` makes them easy to read and searchable. To build this repository follow the instructions below:

1. Build the `conda` or `mamba` documentation environment.

```bash
$ mamba env create -f environment.yml
```

2. Activate the `ast` environment.

```bash
$ mamba activate ast
```

3. Build the docs.

```bash
$ cd docs/
$ make clean html
```

4. Open the `_build/html/index.html` file with any web browser.
