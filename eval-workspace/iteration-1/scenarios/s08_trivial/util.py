def compute(n):
    """Sum of squares of 1..n, plus 3."""
    return sum(i*i for i in range(1, n+1)) + 3
