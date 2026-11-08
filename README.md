# Double-Slit Simulation

An interactive 3D desktop application that illustrates the wave/particle duality of light
through the double-slit experiment. All mathematics (complex numbers, vectors, numerical
integration, random sampling) is implemented from scratch in `mathlib/`.

## Architecture

Simple layered architecture: each layer only depends on the layers below it.

```
app/        GUI (PyQt6 + pyqtgraph). Reads user input, validates it, shows results.
  │
physics/    Business logic: wave model (Huygens–Fresnel) and photon sampler.
  │
mathlib/    From-scratch math frameworks: Complex, Vec3, integration, sampling.
```

`mathlib` and `physics` contain no GUI code and are fully unit-tested.

## Setup

```bash
git clone <repo-url>
cd double-slit
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Running the tests

```bash
pytest
```

Coverage is measured automatically; the run fails if coverage of `mathlib` and
`physics` drops below 99%.

## Generating the documentation

```bash
pdoc mathlib physics -o docs
```

Open `docs/index.html` in a browser.

## Running the app

```bash
python -m app
```

*(The app layer is not built yet.)*
