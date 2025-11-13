# Quantum Metrology Multi-Parameter Estimation Task

This task implements simultaneous estimation of three parameters in a two-mode optical quantum network with Heisenberg-limited precision.

## Task Overview

**Goal:** Implement maximum likelihood estimators for three unknown parameters (φ₀, φ₁, φ₂) in a quantum optical interferometer using homodyne detection measurements.

**Difficulty:** Expert

**Key Challenges:**
1. Understand quantum Fisher Information theory
2. Implement analytical maximum likelihood estimators from research paper
3. Verify Heisenberg scaling (Δφ ~ 1/N vs shot-noise 1/√N)
4. Compute and validate Fisher Information Matrix properties

## Physics Background

### The Optical Network

The system consists of:
- A beam splitter with reflectivity parameter φ₀
- Phase shifters φ₁ and φ₂ in the two arms
- Input: Squeezed vacuum (port 1) + squeezed-coherent state (port 2)
- Measurement: Balanced homodyne detection at both outputs

### Unitary Transformation

```
U = [[e^(iφ₁)cos(φ₀),  e^(iφ₁)sin(φ₀)],
     [-e^(iφ₂)sin(φ₀), e^(iφ₂)cos(φ₀)]]
```

### Measurement Statistics

Homodyne outcomes (x₁, x₂) follow Gaussian distribution:
- Mean vector **μ** depends on all three parameters
- Covariance matrix **Σ** depends only on φ₁, φ₂ (for separable inputs)

This decomposition is KEY to achieving multi-parameter Heisenberg scaling!

## Implementation Requirements

### Core Functions

1. **`estimate_parameters(measurements, config)`**
   - Input: List of (x₁, x₂) tuples, configuration dict
   - Output: (φ₀_est, φ₁_est, φ₂_est)
   - Method: Maximum likelihood estimation

2. **`compute_fisher_information(config, φ₀, φ₁, φ₂)`**
   - Compute 3×3 Fisher Information Matrix
   - Decomposition: F = F^S + F^N
   - F^S: Signal variation (estimates φ₀)
   - F^N: Noise variation (estimates φ₁, φ₂)

3. **`verify_heisenberg_scaling(measurements, config, true_params)`**
   - Check uncertainties achieve Δφ ~ O(1/N)
   - Compare with Cramér-Rao bounds
   - Return comprehensive metrics

### Maximum Likelihood Estimators (Analytical Forms)

From the paper (Eqs. 17-19), for equal squeezing r₁ = r₂ = r:

**IMPORTANT CONSTRAINT:** The analytical form for φ̃₀ in Eq. 17 assumes that local
oscillator phases are tuned according to Eq. 9: θᵢ = γᵢ + kᵢ/Nₛ (asymptotic regime).
For arbitrary local oscillator phases, you must account for the sin(θ-φ) terms.

```python
# Sample mean and covariance
μ̃ = mean(measurements)
Σ̃ = cov(measurements)

# Step 1: Estimate φ₁ and φ₂ from covariance (works for any local oscillator phases)
φ̃₁ = θ₁ + (1/2) * arccos((2Σ̃₁₁ - cosh(2r)) / sinh(2r))

φ̃₂ = θ₂ + (1/2) * arccos((2Σ̃₂₂ - cosh(2r)) / sinh(2r))

# Step 2: Estimate φ₀ from mean vector
# Simplified form (only valid when local oscillators are tuned per Eq. 9):
# φ̃₀ = arctan(-μ̃₁ / μ̃₂)

# General form (works for arbitrary local oscillator phases):
# From μ₁ = √2α sin(φ₀) sin(θ₁-φ₁) and μ₂ = √2α cos(φ₀) sin(θ₂-φ₂)
# Solving for φ₀: tan(φ₀) = (μ̃₁ / μ̃₂) × [sin(θ₂-φ̃₂) / sin(θ₁-φ̃₁)]
φ̃₀ = arctan(μ̃₁ × sin(θ₂-φ̃₂) / (μ̃₂ × sin(θ₁-φ̃₁)))
# Map to [0, π] range for beam splitter reflectivity
```

**Note on Paper Equations:** The research paper (Rai et al., 2025) uses offsets
in Eqs. 18-19: `θᵢ + (1/2)(-2π + arccos(...))` for φ₁ and `θᵢ + (1/2)(-4π + arccos(...))`
for φ₂. These offsets select specific solution branches for their experimental setup.
The simplified form shown above (without offsets) works for the general case and is
what the tests expect.

### Fisher Information Matrix

```python
# Signal contribution (Eq. 8)
F^S_mn = (∂μ/∂φ_m)^T Σ^(-1) (∂μ/∂φ_n)

# Noise contribution (Eq. 8)
F^N_mn = (1/2) Tr[Σ^(-1)(∂Σ/∂φ_m)Σ^(-1)(∂Σ/∂φ_n)]

# Total
F = F^S + F^N
```

### Cramér-Rao Bounds (Eqs. 14-16)

```
(Δφ₀)² ≥ (1/ν) * (1 + 16k²) / (8N_c N_s)

(Δφ₁)² ≥ (1/ν) * (1 + 16k²)² / (128k² N_s²)

(Δφ₂)² ≥ (1/ν) * (1 + 16k²)² / (128k² N_s²)
```

where:
- ν = number of measurements
- N_c = coherent photon number (|α|²)
- N_s = squeezed photon number (sinh²(r))
- k = detuning parameter in θᵢ = γᵢ + k/N_s

## Configuration Parameters

```python
config = {
    'r': 1.5,          # Squeezing parameter
    'alpha': 3.0,      # Coherent state amplitude
    'theta1': 0.15,    # Local oscillator phase 1
    'theta2': 0.25,    # Local oscillator phase 2
    'Ns': sinh(r)²,    # Squeezed photon number
    'Nc': alpha²       # Coherent photon number
}
```

## Test Criteria

Your implementation must pass:

1. **Solution Exists:** All required functions (estimate_parameters, compute_fisher_information, verify_heisenberg_scaling) are implemented

2. **Parameter Estimation Accuracy:**
   - φ₀: absolute error < 0.02 radians with 5000 samples
   - φ₁, φ₂: absolute error < 0.03 radians with 5000 samples

3. **Fisher Information Properties:**
   - Symmetric: F = F^T
   - Positive semi-definite (eigenvalues ≥ 0)
   - All elements are finite
   - Non-zero (contains information)

4. **Fisher Information Scaling:** FIM diagonal elements scale with photon number (between 2x and 8x when doubling N)

5. **Estimation Accuracy Across Parameter Regimes:**
   - φ₀: error < 0.5-0.7 radians (beam splitter reflectivity estimation is challenging)
   - φ₁, φ₂: error < 0.1 radians (phase estimation from covariance is accurate)
   - Maximum error across all parameters: < 1.0 radian

6. **CRB Approximation:** Uncertainties within factor of 3 of Cramér-Rao bounds with 1000 samples

7. **Unbiasedness:** Mean estimator bias < 0.1 radians (10%) over 50 trials

8. **Edge Cases:** Handles boundary parameters without crashing (near zero, near 2π)

9. **Data Format:** Correctly processes list of (x₁, x₂) measurement tuples

10. **Return Values:** verify_heisenberg_scaling returns all required fields (estimates, uncertainties, crb_bounds, achieves_heisenberg, fisher_information)

### Note on Test Criteria

The test criteria focus on **practical estimation accuracy** rather than strict theoretical bounds. The tests verify that:
- **φ₁ and φ₂ phase estimation is accurate** (< 0.1 rad error from covariance matrix)
- **φ₀ reflectivity estimation is reasonable** (< 0.5-0.7 rad error; this parameter is harder to estimate)
- **Fisher Information is mathematically correct** (symmetric, PSD, scales properly)
- **Uncertainties are reasonable** (within 3x of theoretical bounds is acceptable for bootstrap)
- **Estimators are approximately unbiased** (< 10% bias for finite samples)

**Why φ₀ has larger errors:** The beam splitter reflectivity φ₀ is estimated from the mean vector, which requires dividing by sin(θ-φ) terms that can amplify noise. In contrast, φ₁ and φ₂ are estimated directly from the covariance matrix diagonal elements, which is more robust.

For production implementations requiring optimal uncertainty quantification, consider using Fisher Information-based uncertainties instead of bootstrap.

## Key Insights for Success

### Why This Decomposition Works

The Fisher Information splits because:
- **Σ depends only on (φ₁, φ₂)** → F^N can estimate phases from noise
- **μ depends on all three** → F^S can estimate reflectivity from signal

This is ONLY true for separable input states!

### Heisenberg vs Shot-Noise Scaling

**Shot-noise:** Δφ ~ 1/√N (classical limit)
**Heisenberg:** Δφ ~ 1/N (quantum limit)

For N=100 photons:
- Shot-noise: Δφ ~ 0.1
- Heisenberg: Δφ ~ 0.01 (10× better!)

### Local Oscillator Tuning

The phases θᵢ must be tuned as:
```
θᵢ = γᵢ + k/N_s
```
where γᵢ is the minimum variance phase. This detuning is CRITICAL for Heisenberg scaling!

## Common Pitfalls

1. **Forgetting wraparound:** Phases are mod 2π
2. **Numerical instability:** arccos argument must be in [-1, 1]
3. **Matrix singularity:** Check Fisher Information is invertible
4. **Wrong scaling:** Remember φ₀ scales with N_total, φ₁,₂ with N_s only
5. **Ignoring correlations:** Covariance matrix structure matters

## Debugging Tips

If your estimates are wrong:
1. Check sample mean/covariance calculation
2. Verify arctan2 vs arctan (for φ₀)
3. Check angle normalization (0 to 2π or -π to π)
4. Print intermediate values in MLE formulas

If Fisher Information is wrong:
1. Verify mean and covariance derivatives
2. Check matrix multiplication order
3. Test symmetry F = F^T
4. Compute eigenvalues to check positive semi-definiteness

If accuracy tests fail:
1. Check photon number calculations (N_s, N_c)
2. Verify local oscillator phases
3. Ensure sufficient measurements (ν ≥ 500)
4. Check φ₀ estimation formula and range mapping [0, π]
5. Verify φ₁, φ₂ estimation from covariance matrix

## Reference

Based on: Rai et al., "Simultaneous estimation of three parameters with Heisenberg scaling sensitivity in a two-channel optical network", Eur. Phys. J. Plus (2025) 140:858

## Solution Structure

```
estimator.py
├── compute_mean_vector()           # Eq. (5)
├── compute_covariance_matrix()     # Eq. (6)
├── compute_fisher_information()    # Eq. (8)
├── estimate_parameters()           # Eqs. (17-19)
├── verify_heisenberg_scaling()     # Check CRB saturation
└── generate_synthetic_measurements() # For testing
```

Good luck! This task requires deep understanding of quantum estimation theory.
