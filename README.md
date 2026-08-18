# ICA-Analysis-of-Hyperspectral-Image-Data

# ICA Analysis of Hyperspectral Image Data

A dimensionality-reduction study applying **Independent Component Analysis (ICA)** to hyperspectral imagery, using the classic **Indian Pines** dataset. The project ranks independent components by their statistical independence (skewness + kurtosis) and visualizes the most informative ones.

# ICA Analysis of Hyperspectral Image Data

A dimensionality-reduction study applying **Independent Component Analysis (ICA)** to hyperspectral imagery, using the classic **Indian Pines** dataset. The project ranks independent components by their statistical independence (skewness + kurtosis) and visualizes the most informative ones.



## Overview

Hyperspectral images contain hundreds of spectral bands, producing very high-dimensional data. While PCA and MNF are common dimensionality-reduction tools, they rely on second-order statistics (variance) and can miss more complex, non-Gaussian structure in the data. This project explores **ICA-based dimensionality reduction**, which instead exploits statistical independence between components to capture richer structure.

Three ICA-based methods are discussed as motivation for this work:

| Method | Idea |
|---|---|
| **ICA-DR1** | Uses Virtual Dimensionality (VD) to pick the number of components, then ranks Independent Components (ICs) by skewness/kurtosis (higher-order statistics). |
| **ICA-DR2** | Runs FastICA multiple times and keeps only the ICs that consistently reappear across runs, improving stability. |
| **ICA-DR3** | Uses the Automatic Target Generation Process (ATGP) to build structured initial vectors instead of random ones, making FastICA more deterministic. |

This implementation follows **ICA-DR1**.

## Dataset

**Indian Pines** — AVIRIS sensor scene over north-western Indiana.

- Original size: 145 × 145 pixels, 224 spectral bands (0.4–2.5 μm)
- Water-absorption bands removed ([104–108], [150–163], 220) → **200 bands** used
- Ground truth: 16 (non-mutually-exclusive) land-cover classes
- Scene mostly agriculture (corn, soybean) and forest, with roads/highways and light housing
- Source: Purdue University MultiSpec site

## Method (ICA-DR1 pipeline)

1. **Load & reshape** the hyperspectral cube `(145, 145, 200)` into a 2D matrix of pixels × bands.
2. **Whiten** the data with PCA (`whiten=True`).
3. **Run FastICA** on the whitened data to extract independent components (ICs).
4. **Score each IC** using skewness and kurtosis; combine them as `|skewness| + |kurtosis|`.
5. **Rank & select** components — the highest-scoring ICs are treated as carrying the most non-Gaussian, information-rich structure.
6. **Visualize**: bar chart of the ranking, grayscale images of the top 20 ICs, their histograms, and a synthetic RGB composite built from the top 3 ICs.

## Requirements

```
numpy
matplotlib
scikit-learn
scipy
```

(The original script also imports `google.colab.files`, which is only needed if running on Google Colab and can be removed for local use.)

## Usage

1. Download the Indian Pines corrected dataset (`Indian_pines_corrected.mat`) from the Purdue MultiSpec site.
2. Place it in the working directory (or upload it if using Colab).
3. Run the script:

```bash
python ica_analysis.py
```

This will print a **Component Ranking Report** (top 20 ICs with mean, variance, skewness, kurtosis, and combined rank metric) and generate the following plots:

- `Ranking of Components Based on Skewness and Kurtosis` — bar chart of all components
- `Top 20 Independent Components Visualization` — grayscale maps of the leading ICs
- `Histograms of Top 20 Independent Components`
- `RGB Image from Top 3 ICs` — false-color composite from the three highest-ranked components

## Results (summary)

The top-ranked component (**IC 36**) dominates the ranking by a large margin (combined metric ≈ 3321), with kurtosis (≈ 3285) far exceeding the rest — suggesting it captures a small number of extreme, highly localized features (e.g. bright anomalous pixels) rather than broad spatial structure. Components ranked 2–20 show a steep drop-off and much more gradual decay afterward, visible in the ranking bar chart. The RGB composite from the top 3 ICs highlights a handful of sparse, spatially isolated bright spots against a uniform background, consistent with the components' high-kurtosis (heavy-tailed, outlier-driven) character.

## Project Structure

```
.
├── ica_analysis.py                  # Main analysis script
├── Indian_pines_corrected.mat       # Input dataset (not included — download separately)
└── README.md
```

## References

- Indian Pines dataset: Purdue University MultiSpec site
- ICA-DR1 / ICA-DR2 / ICA-DR3 methods adapted from literature on ICA-based dimensionality reduction for hyperspectral imagery, using Virtual Dimensionality (VD) and Automatic Target Generation Process (ATGP) concepts.

## Overview

Hyperspectral images contain hundreds of spectral bands, producing very high-dimensional data. While PCA and MNF are common dimensionality-reduction tools, they rely on second-order statistics (variance) and can miss more complex, non-Gaussian structure in the data. This project explores **ICA-based dimensionality reduction**, which instead exploits statistical independence between components to capture richer structure.

Three ICA-based methods are discussed as motivation for this work:

| Method | Idea |
|---|---|
| **ICA-DR1** | Uses Virtual Dimensionality (VD) to pick the number of components, then ranks Independent Components (ICs) by skewness/kurtosis (higher-order statistics). |
| **ICA-DR2** | Runs FastICA multiple times and keeps only the ICs that consistently reappear across runs, improving stability. |
| **ICA-DR3** | Uses the Automatic Target Generation Process (ATGP) to build structured initial vectors instead of random ones, making FastICA more deterministic. |

This implementation follows **ICA-DR1**.

## Dataset

**Indian Pines** — AVIRIS sensor scene over north-western Indiana.

- Original size: 145 × 145 pixels, 224 spectral bands (0.4–2.5 μm)
- Water-absorption bands removed ([104–108], [150–163], 220) → **200 bands** used
- Ground truth: 16 (non-mutually-exclusive) land-cover classes
- Scene mostly agriculture (corn, soybean) and forest, with roads/highways and light housing
- Source: Purdue University MultiSpec site

## Method (ICA-DR1 pipeline)

1. **Load & reshape** the hyperspectral cube `(145, 145, 200)` into a 2D matrix of pixels × bands.
2. **Whiten** the data with PCA (`whiten=True`).
3. **Run FastICA** on the whitened data to extract independent components (ICs).
4. **Score each IC** using skewness and kurtosis; combine them as `|skewness| + |kurtosis|`.
5. **Rank & select** components — the highest-scoring ICs are treated as carrying the most non-Gaussian, information-rich structure.
6. **Visualize**: bar chart of the ranking, grayscale images of the top 20 ICs, their histograms, and a synthetic RGB composite built from the top 3 ICs.

## Requirements

```
numpy
matplotlib
scikit-learn
scipy
```

(The original script also imports `google.colab.files`, which is only needed if running on Google Colab and can be removed for local use.)

## Usage

1. Download the Indian Pines corrected dataset (`Indian_pines_corrected.mat`) from the Purdue MultiSpec site.
2. Place it in the working directory (or upload it if using Colab).
3. Run the script:

```bash
python ica_analysis.py
```

This will print a **Component Ranking Report** (top 20 ICs with mean, variance, skewness, kurtosis, and combined rank metric) and generate the following plots:

- `Ranking of Components Based on Skewness and Kurtosis` — bar chart of all components
- `Top 20 Independent Components Visualization` — grayscale maps of the leading ICs
- `Histograms of Top 20 Independent Components`
- `RGB Image from Top 3 ICs` — false-color composite from the three highest-ranked components

## Results (summary)

The top-ranked component (**IC 36**) dominates the ranking by a large margin (combined metric ≈ 3321), with kurtosis (≈ 3285) far exceeding the rest — suggesting it captures a small number of extreme, highly localized features (e.g. bright anomalous pixels) rather than broad spatial structure. Components ranked 2–20 show a steep drop-off and much more gradual decay afterward, visible in the ranking bar chart. The RGB composite from the top 3 ICs highlights a handful of sparse, spatially isolated bright spots against a uniform background, consistent with the components' high-kurtosis (heavy-tailed, outlier-driven) character.

## Project Structure

```
.
├── ica_analysis.py                  # Main analysis script
├── Indian_pines_corrected.mat       # Input dataset (not included — download separately)
└── README.md
```

## References

- Indian Pines dataset: Purdue University MultiSpec site
- ICA-DR1 / ICA-DR2 / ICA-DR3 methods adapted from literature on ICA-based dimensionality reduction for hyperspectral imagery, using Virtual Dimensionality (VD) and Automatic Target Generation Process (ATGP) concepts.
