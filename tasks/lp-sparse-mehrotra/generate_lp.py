import numpy as np
import scipy.sparse as sp

# Generate a well-conditioned test LP problem:
# minimize c^T x subject to A x = b, x >= 0

np.random.seed(42)

# Problem dimensions (much larger for real difficulty)
m = 100  # constraints
n = 250  # variables

# Create sparse constraint matrix A with ~3% density (very sparse = harder)
density = 0.03
A_data = []
A_row = []
A_col = []

# Generate random sparse entries
for i in range(m):
    for j in range(n):
        if np.random.rand() < density:
            A_data.append(np.random.randn())
            A_row.append(i)
            A_col.append(j)

# Weak diagonal dominance (harder conditioning)
for i in range(min(m, n)):
    A_data.append(1.5 + np.random.rand() * 0.5)  # Much weaker dominance
    A_row.append(i)
    A_col.append(i)

# Build sparse matrix
A = sp.coo_matrix((A_data, (A_row, A_col)), shape=(m, n), dtype=np.float64)
A = A.tocsr()

# Generate a feasible interior point x0 >> 0
x0 = 2.0 + np.random.rand(n) * 3.0  # values between 2 and 5

# Set b = A @ x0 to ensure strict feasibility
b = A @ x0

# Generate cost vector c that ensures bounded optimum
# Strategy: Use c = A^T w for some w, which ensures c is in row space of A
# This prevents unboundedness in the null space of A
w = np.random.randn(m)
c = A.T @ w + np.ones(n) * 0.1  # Slight positive bias for regularization

# Save A, b, c separately (NOT as a sparse object inside NPZ)
np.savez(
    "/app/lp.npz",
    A_data=A.data,
    A_indices=A.indices,
    A_indptr=A.indptr,
    A_shape=A.shape,
    b=b,
    c=c
)

print("✅ Generated /app/lp.npz")
print(f"   Dimensions: {m} constraints × {n} variables")
print(f"   Sparsity: {A.nnz} non-zeros ({100*A.nnz/(m*n):.1f}%)")
print("   Condition estimate: Matrix is diagonally dominant")
