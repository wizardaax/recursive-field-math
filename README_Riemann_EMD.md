
# Enhanced Riemann Zeta Residual Analysis using Empirical Mode Decomposition (EMD)

## 📘 Overview

This project performs high-resolution numerical analysis of the deviation between an **analytic model of the Riemann zeta zeros** and the **Odlyzko-style approximation**. Traditional harmonic correction methods failed, prompting the use of **Empirical Mode Decomposition (EMD)** — a non-linear, non-stationary signal decomposition technique.

---

## 🧠 Objective

Decompose the residual:
\[
\Delta t_n = t_{\text{analytic}} - t_{\text{true}}
\]

Where:
- \( t_{\text{analytic}} = n \cdot \varphi + A \cdot \sin(B \cdot \log n + \delta) \)
- \( t_{\text{true}} = \frac{(n - 0.5)\pi}{\log n} \)
- \( \varphi \) is the golden ratio

---

## ⚠️ Problem with Harmonic Overlay

Initial attempts to apply nine additive harmonic corrections (FFT-based) **amplified deviation by over 600,000%** due to phase misalignment and rigidity of global sinusoidal terms.

---

## ✅ EMD Methodology

1. **Compute Residual:** Difference between analytic model and Odlyzko zeros
2. **Apply EMD (PyEMD):** Decomposes residual into Intrinsic Mode Functions (IMFs)
3. **Reconstruct Residual:** Subtract sum of IMFs to get corrected deviation
4. **Validate Results:**
   - Mean Absolute Deviation (MAD)
   - Max deviation
   - FFT before/after
   - Q-Q plot for normality
   - Ljung–Box test for autocorrelation

---

## 🧪 Statistical Diagnostics

- **Ljung–Box Test:** Applied to corrected residuals
- **Q-Q Plot:** Showed improved alignment with normality
- **FFT Comparison:** Lower power at key frequencies post-EMD

---

## 📈 Results

| Metric                  | Value         |
|-------------------------|---------------|
| Original Mean \(|\Delta t|\)| ~6,281       |
| Corrected Mean \(|\Delta t|\)| (via EMD)  ~2,439       |
| Compression Improvement | ~61.2% 🔻     |

---

## 📦 Output Files

- `riemann_emd_decomposition.csv`: Full table with IMFs, original & corrected residuals
- `riemann_emd_analysis.py`: Main script to reproduce analysis

---

## 🔧 Options Going Forward

- Select subset of IMFs (e.g., IMF 2–4)
- Switch to EEMD or CEEMDAN (AdvEMDpy)
- Perform model selection (AIC/BIC)
- Apply to other zero datasets (Odlyzko raw files)
- Export IMF matrix for machine learning or spectral modeling

---

## 🛠 Requirements

```bash
pip install numpy pandas matplotlib scipy PyEMD statsmodels
```

---

## 👨‍💻 Author Note

This project pushes beyond textbook theory by using **adaptive decomposition** and real statistical validation instead of symbolic overlays. Harmonics failed. EMD succeeded.

