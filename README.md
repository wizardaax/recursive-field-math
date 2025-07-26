# Recursive Field: Mathematical Formulas

This repository contains mathematical models inspired by the **“Recursive Field”** scientific math song. The song describes a pattern reminiscent of phyllotaxis (the arrangement of leaves or seeds) where radii grow with the square root of the index and angles are rotated by the golden angle. We formalize these relationships and provide documentation and simple tools for exploration.

## Contents
- `recursive_field_formulas.md` – the original set of formulas derived from the song.
- `explicit_formulas.md` – detailed equations and a concise narrative explaining each term.
- `my_recursive_ai.py` – a simple rule‑based chatbot for answering questions about the formulas.
- `LICENSE` – open‑source license for this project.

## Formulas
The core relationships described in the song can be summarized as:

- **Radius growth**: \( r_n = a \sqrt{n} \), where `a = 3` sets the scale of the spiral.
- **Angular progression**: \( \theta_n = n \phi \), where \( \phi \) is the golden angle (\u2248 137.508\u00b0).
- **Base case**: at `n = 1`, \( r_1 = \sqrt{3} \).
- **Full rotation cycle**: the pattern aligns at \(\pi\), \(2\pi\) and \(3\pi\).

See [`explicit_formulas.md`](explicit_formulas.md) for the full set of equations and an accompanying explanation.

## Getting Started
If you’d like to explore these formulas programmatically, run the `my_recursive_ai.py` script with Python to interact with a basic rule‑based chatbot. The script responds to keywords related to the radius, angle, base case and rotation cycles.

```bash
python my_recursive_ai.py
```

## License
This project is licensed under the MIT License; see [`LICENSE`](LICENSE) for details.
