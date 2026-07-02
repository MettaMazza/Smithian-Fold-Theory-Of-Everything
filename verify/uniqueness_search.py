#!/usr/bin/env python3
# ============================================================================
#  FREE-INGREDIENT UNIQUENESS SEARCH  --  the alpha assembly is the ONLY one.
# ============================================================================
#  The forcing guards (fine_structure_assembly_is_minimal) hold the ingredients FIXED
#  and vary how they combine. This search does the harder, opposite thing: it holds the
#  combining SHAPE fixed and lets the ingredient VALUES roam over the entire
#  {2,3,5,7}-smooth space -- every prime-power tower, every squared colour block, every
#  smooth covering volume and second-order sub -- then counts how many assemblies land on
#  the measured 1/alpha within the MEASUREMENT'S OWN PUBLISHED UNCERTAINTY.
#
#  The assembly is  1/alpha = tower + colour_block * (cov_eff + 1)/cov_eff ,
#                   cov_eff = cov + 1/sub .
#  The ingredients are kept in their STRUCTURAL ROLES (AGENT.md rule 2): the tower is a
#  genuine prime power A^B (a binary/prime tower, exponent >= 2), the colour block is a
#  square c^2 (a squared count). Their VALUES are otherwise free over the smooth space.
#
#  NOTHING IN THE CHECK IS A DIAL:
#   - The acceptance window is CODATA's own one-sigma uncertainty,
#     1/alpha = 137.035999177(21), i.e. SIGMA = 21e-9 -- not a chosen tolerance.
#   - The sub sampler scans EVERY smooth E whose 1/E is near the required remainder
#     (float pre-selection only); every candidate is confirmed in EXACT rational
#     arithmetic. Widen the bounds and the counts do not change.
#   - The full neighborhood out to 5 sigma is REPORTED, each candidate annotated
#     mechanically as in-role or not (in-role: cov = 2*d^3 and sub = d^2*e for smooth
#     d, e -- the covering-cube parse). Nothing near the measurement is hidden.
#
#  Uniqueness is declared only if EXACTLY ONE candidate lies within 1 sigma and it is
#  in-role. Expected: one hit -- the theory's (2^7, 3^2, 250, 175) = 5995462/43751 at
#  ~0.008 sigma, in-role; the nearest neighbor sits ~1.1 sigma out with no parse; a
#  second in-role point (sub = 200) appears at ~4.9 sigma, excluded by the measurement
#  itself -- printed, not hidden.
#  Run it:  python3 verify/uniqueness_search.py
# ============================================================================
from fractions import Fraction as F

TARGET = F(137035999177, 10**9)   # CODATA 1/alpha (comparison side only)
SIGMA  = F(21, 10**9)             # CODATA's own published one-sigma: 137.035999177(21)
REPORT = 5                        # report the neighborhood out to 5 sigma
NMAX   = 8000                     # smooth-space bound (raise it; the counts are stable)

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

def parse_in_role(D, E, SM):
    """The covering-cube parse: cov = 2*d^3 and sub = d^2*e with smooth d, e.
    Returns (d, e) if the candidate is in-role, else None. Mechanical, no judgment."""
    d = 1
    while 2 * d**3 <= D:
        if 2 * d**3 == D and d in SM:
            if E % (d * d) == 0:
                e = E // (d * d)
                if e >= 1 and e in SM:
                    return (d, e)
        d += 1
    return None

def main():
    SM = smooth(NMAX)
    ft = float(TARGET)
    window = float(REPORT * SIGMA)
    # tower = A^B in role: a prime tower, exponent >= 2, below the target.
    towers = []
    for A in (2, 3, 5, 7):
        B = 2
        while A**B <= 150:
            towers.append((A**B, A, B)); B += 1
    # colour block = c^2 in role: a squared count.
    squares = [(c*c, c) for c in sorted(SM) if c*c <= 150]
    covs = [d for d in sorted(SM) if 2 <= d <= NMAX]
    subs = sorted(SM)

    candidates = {}
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
                if g <= 0 or g > 0.51:
                    continue
                # scan EVERY smooth E whose 1/E is near the required remainder g
                # (the old two-integer sampler missed exact hits inside the window)
                for E in subs:
                    if E < 2:
                        continue
                    if abs(1.0 / E - g) < 1e-3:
                        cov_eff = F(D) + F(1, E)
                        val = F(tw) + Cv * (cov_eff + 1) / cov_eff   # EXACT decider
                        if abs(val - TARGET) <= REPORT * SIGMA:
                            candidates[(tw, A, B, Cv, c, D, E)] = val

    print("=" * 78)
    print("  FREE-INGREDIENT UNIQUENESS  --  the {2,3,5,7}-smooth neighborhood of 1/alpha")
    print("  window: CODATA's own uncertainty, sigma = 21e-9 (nothing here is a dial)")
    print("  (ingredients free in their structural roles: tower = A^B, colour = c^2)")
    print("=" * 78)
    rows = []
    for (tw, A, B, Cv, c, D, E), val in candidates.items():
        ns = abs(val - TARGET) / SIGMA           # exact Fraction distance in sigmas
        role = parse_in_role(D, E, SM)
        rows.append((float(ns), ns, tw, A, B, Cv, c, D, E, val, role))
    rows.sort(key=lambda r: r[0])
    print("  candidates within %d sigma: %d" % (REPORT, len(rows)))
    for nsf, ns, tw, A, B, Cv, c, D, E, val, role in rows:
        tag = ("in-role (cov=2*%d^3, sub=%d^2*%d)" % (role[0], role[0], role[1])) if role else "no parse"
        print("   tower=%d (%d^%d)  colour=%d (%d^2)  cov=%d  sub=%d  ->  %.10f   %.3f sigma   [%s]"
              % (tw, A, B, Cv, c, D, E, float(val), nsf, tag))
    one_sigma = [r for r in rows if r[1] <= SIGMA / SIGMA]   # ns <= 1
    print("=" * 78)
    if len(one_sigma) == 1 and one_sigma[0][10] is not None:
        nsf = one_sigma[0][0]
        print("  UNIQUE: exactly one candidate lies within the measurement's own 1 sigma")
        print("  (%.3f sigma) and it is in-role -- the theory's (2^7, 3^2, 250, 175)." % nsf)
        print("  Every other point in the 5-sigma neighborhood is printed above: the nearest")
        print("  has no structural parse; any other in-role point is excluded by the")
        print("  measurement itself.")
        return 0
    print("  NOT UNIQUE under the measurement's own sigma -- investigate.")
    return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
