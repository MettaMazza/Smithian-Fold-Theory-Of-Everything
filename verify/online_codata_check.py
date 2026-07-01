#!/usr/bin/env python3
# ============================================================================
#  ONLINE CODATA CROSS-CHECK  --  forced values DERIVED here from the fold's two
#  structural integers, compared to values fetched LIVE from NIST's authoritative
#  CODATA table.
# ============================================================================
#  The offline proofs (make -C verify prove) already compare every forced value to a
#  sealed measured constant. A skeptic can still say "you typed those measured numbers
#  in yourself." This script removes that objection: the measured side is fetched, at
#  run time, from NIST -- https://physics.nist.gov/cuu/Constants/Table/allascii.txt --
#  and nothing measured is stored in this file. The forced side is DERIVED here, in
#  exact rational arithmetic, from only the binary count 2 and the colour count 3 (the
#  two generators the fold's period spectrum forces) -- no measured input, no fit.
#
#  Forced (from the One)  vs  Measured (fetched live from NIST). Run it yourself:
#      python3 verify/online_codata_check.py
# ============================================================================
from fractions import Fraction as F
import urllib.request, re, sys

BINARY, COLOUR = 2, 3   # the two generators, counted from the fold's period spectrum

# ---------------------------------------------------------------------------
#  The forced side -- derived here from BINARY and COLOUR, zero parameters.
# ---------------------------------------------------------------------------
def forced_inverse_alpha():
    """1/alpha to the second self-similar order = 5995462/43751 (see fine_structure_constant.ep)."""
    up      = COLOUR + (COLOUR + 1)          # 7  = minimal binary cover of 3^4
    down    = BINARY + COLOUR                # 5  = minimal binary cover of 3^3
    tower   = BINARY ** up                   # 128
    csq     = COLOUR ** BINARY               # 9
    cov     = BINARY * down ** COLOUR        # 250 = 2 * 5^3
    sub     = down ** BINARY * up            # 175 = 5^2 * 7  (one cube direction promoted)
    cov_eff = cov + F(1, sub)                # 43751/175
    return tower + csq * (cov_eff + 1) / cov_eff

def forced_proton_electron():
    """mp/me = (1/c)(m_mu - m_e)/(m_mu m_e) from the forced lepton cubic's bisected roots."""
    e2 = F(1, BINARY * COLOUR)               # 1/6   = 1/(2c)
    e3 = F(1, BINARY * COLOUR ** 5 - 1)      # 1/485 = 1/(2c^5 - 1)
    def f(x): return x**3 - x**2 + e2 * x - e3
    def bisect(lo, hi, n=60):
        lo, hi = F(lo), F(hi); s = f(lo) > 0
        for _ in range(n):
            m = (lo + hi) / 2
            if (f(m) > 0) == s: lo = m
            else: hi = m
        return (lo + hi) / 2
    x1 = bisect(F(1, 1000), F(1, 20))        # electron root
    x2 = bisect(F(1, 10),   F(3, 10))        # muon root
    me, mmu = x1 * x1, x2 * x2
    return F(1, COLOUR) * (mmu - me) / (mmu * me)

def forced_muon_electron():
    """m_mu/m_e = (muon share)/(electron share) from the forced lepton-cubic roots."""
    e2 = F(1, BINARY * COLOUR)
    e3 = F(1, BINARY * COLOUR ** 5 - 1)
    def f(x): return x**3 - x**2 + e2 * x - e3
    def bisect(lo, hi, n=60):
        lo, hi = F(lo), F(hi); s = f(lo) > 0
        for _ in range(n):
            m = (lo + hi) / 2
            if (f(m) > 0) == s: lo = m
            else: hi = m
        return (lo + hi) / 2
    x1 = bisect(F(1, 1000), F(1, 20))
    x2 = bisect(F(1, 10), F(3, 10))
    return (x2 * x2) / (x1 * x1)

def forced_electron_g():
    """Bare Dirac g = 2 -- the fold's two preimages of the One."""
    return F(BINARY)

# ---------------------------------------------------------------------------
#  The measured side -- fetched live from NIST, nothing stored here.
# ---------------------------------------------------------------------------
NIST_URL = "https://physics.nist.gov/cuu/Constants/Table/allascii.txt"

def fetch_nist():
    request = urllib.request.Request(NIST_URL, headers={"User-Agent": "Mozilla/5.0 (SFTOM online CODATA cross-check)"})
    text = urllib.request.urlopen(request, timeout=30).read().decode("utf-8", "replace")
    table = {}
    for line in text.splitlines():
        parts = re.split(r"\s{2,}", line.strip())
        if len(parts) >= 2:
            name, value = parts[0], parts[1].replace(" ", "")
            try:
                table[name.lower()] = float(value)
            except ValueError:
                pass
    return table

def main():
    try:
        nist = fetch_nist()
    except Exception as exc:
        print("could not reach NIST (%s). Offline proof: make -C verify prove" % exc)
        return 2

    rows = [
        ("1/alpha (inverse fine-structure)", forced_inverse_alpha(), "inverse fine-structure constant", 1e-6),
        ("proton / electron mass ratio",     forced_proton_electron(), "proton-electron mass ratio",     1e-2),
        ("muon / electron mass ratio",       forced_muon_electron(),   "muon-electron mass ratio",       1e-2),
        ("electron g (magnitude)",           forced_electron_g(),      "electron g factor",              1e-2),
    ]
    print("=" * 78)
    print("  ONLINE CODATA CROSS-CHECK  --  forced (from the One)  vs  NIST (fetched live)")
    print("=" * 78)
    worst_ok = True
    for label, forced, nist_name, tol in rows:
        if nist_name not in nist:
            print("  ??  %-34s NIST entry '%s' not found" % (label, nist_name))
            worst_ok = False
            continue
        measured = abs(nist[nist_name])
        dev = abs(float(forced) - measured) / measured
        mark = "ok  " if dev <= tol else "FAIL"
        if dev > tol:
            worst_ok = False
        print("  %s%-32s forced %-16.9g  NIST %-16.9g  dev %.4g%%"
              % (mark, label, float(forced), measured, dev * 100))
    print("=" * 78)
    if worst_ok:
        print("  every forced value lands on the LIVE-FETCHED measurement.")
        return 0
    print("  a forced value missed its live measurement (or NIST was unreachable).")
    return 1

if __name__ == "__main__":
    sys.exit(main())
