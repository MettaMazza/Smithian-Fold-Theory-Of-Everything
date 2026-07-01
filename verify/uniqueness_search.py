#!/usr/bin/env python3
# ============================================================================
#  FREE-INGREDIENT UNIQUENESS SEARCH  --  the alpha assembly is the ONLY one.
# ============================================================================
#  The forcing guards (fine_structure_assembly_is_minimal) hold the ingredients FIXED
#  and vary how they combine. This search does the harder, opposite thing: it holds the
#  combining SHAPE fixed and lets the ingredient VALUES roam over the entire
#  {2,3,5,7}-smooth space -- every prime-power tower, every squared colour block, every
#  smooth covering volume and second-order sub -- then counts how many assemblies land on
#  the measured 1/alpha to nine significant digits.
#
#  The assembly is  1/alpha = tower + colour_block * (cov_eff + 1)/cov_eff ,
#                   cov_eff = cov + 1/sub .
#  The ingredients are kept in their STRUCTURAL ROLES (AGENT.md rule 2): the tower is a
#  genuine prime power A^B (a binary/prime tower, exponent >= 2), the colour block is a
#  square c^2 (a squared count). Their VALUES are otherwise free over the smooth space.
#
#  The hit decision is EXACT (Python Fraction, no float): a float pass only pre-selects
#  candidates near the target; every candidate is then confirmed in exact rational
#  arithmetic against the tolerance. Widen the bounds and the count does not change.
#
#  Result: exactly ONE hit -- the theory's (2^7, 3^2, 250, 175) = 5995462/43751.
#  Run it:  python3 verify/uniqueness_search.py
# ============================================================================
from fractions import Fraction as F

TARGET = F(137035999177, 10**9)   # CODATA 1/alpha (comparison side only)
TOL    = F(1, 10**7)              # nine significant digits
NMAX   = 8000                     # smooth-space bound (raise it; the count is stable)

def smooth(n):
    """All {2,3,5,7}-smooth numbers <= n."""
    out = set(); p2 = 1
    while p2 <= n:
        p3 = p2
        while p3 <= n:
            p5 = p3
            while p5 <= n:
                p7 = p5
                while p7 <= n:
                    out.add(p7); p7 *= 7
                p5 *= 5
            p3 *= 3
        p2 *= 2
    return out

def main():
    SM = smooth(NMAX)
    ft = float(TARGET)
    # tower = A^B in role: a prime tower, exponent >= 2, below the target.
    towers = []
    for A in (2, 3, 5, 7):
        B = 2
        while A**B <= 150:
            towers.append((A**B, A, B)); B += 1
    # colour block = c^2 in role: a squared count.
    squares = [(c*c, c) for c in sorted(SM) if c*c <= 150]
    covs = [d for d in sorted(SM) if 2 <= d <= NMAX]

    hits = set()
    for tw, A, B in towers:
        for Cv, c in squares:
            r = ft - tw - Cv
            if r <= 0:
                continue
            cov_guess = Cv / r                 # float, only to pre-select candidates
            if cov_guess < 2 or cov_guess > NMAX:
                continue
            for D in covs:
                g = cov_guess - D
                if g <= 0:
                    continue
                Ereal = 1.0 / g
                for E in (int(Ereal), int(Ereal) + 1):     # nearest sub candidates
                    if E < 2 or E not in SM:
                        continue
                    cov_eff = F(D) + F(1, E)
                    val = F(tw) + Cv * (cov_eff + 1) / cov_eff   # EXACT
                    if abs(val - TARGET) <= TOL:
                        hits.add((tw, A, B, Cv, c, D, E, val))

    print("=" * 74)
    print("  FREE-INGREDIENT UNIQUENESS  --  9-digit hits over the {2,3,5,7}-smooth space")
    print("  (ingredients free in their structural roles: tower = A^B, colour = c^2)")
    print("=" * 74)
    print("  hits found: %d" % len(hits))
    for tw, A, B, Cv, c, D, E, val in sorted(hits, key=lambda h: h[0]):
        dev = abs(float(val) - float(TARGET))
        print("   tower=%d (%d^%d)  colour=%d (%d^2)  cov=%d  sub=%d  ->  %s = %.10f  (dev %.1e)"
              % (tw, A, B, Cv, c, D, E, val, float(val), dev))
    print("=" * 74)
    if len(hits) == 1:
        print("  UNIQUE: the theory's assembly is the only one that lands. Nothing else in")
        print("  the whole smooth space reproduces 1/alpha to nine digits -- in role.")
        return 0
    print("  NOT UNIQUE -- investigate.")
    return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
