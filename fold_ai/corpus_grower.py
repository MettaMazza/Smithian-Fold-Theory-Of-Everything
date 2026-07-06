"""THE FLOOD: continuous ingestion of clean public-domain prose (Project
Gutenberg) into the growing diet. Legal, massive, real conversational and
narrative English -- the fluency diet the physics corpus could never be.
Runs forever; each book stripped of license boilerplate, saved to diet/.
The engine reads diet/ at every wake, so it grows continuously."""
import urllib.request, os, time, re, random

DIET = os.path.dirname(os.path.abspath(__file__)) + "/diet"
os.makedirs(DIET, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (UnisonAI diet builder; research)"}
rng = random.Random()

def fetch(book_id):
    for url in (f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
                f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt",
                f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", errors="ignore")
        except Exception:
            continue
    return None

def strip_boiler(t):
    s = re.search(r"\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG.*?\*\*\*", t, re.S)
    e = re.search(r"\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG", t, re.S)
    if s: t = t[s.end():]
    if e: t = t[:e.start()]
    return t.strip()

if __name__ == "__main__":
    have = set(int(f[3:-4]) for f in os.listdir(DIET) if f.startswith("gb_") and f.endswith(".txt"))
    got = len(have)
    total_mb = sum(os.path.getsize(DIET + "/" + f) for f in os.listdir(DIET)) / 1e6
    print(f"diet start: {got} books, {total_mb:.1f} MB", flush=True)
    while True:
        bid = rng.randint(1, 70000)
        if bid in have:
            continue
        t = fetch(bid)
        if not t or "PROJECT GUTENBERG" not in t:
            time.sleep(1); continue
        body = strip_boiler(t)
        if len(body) < 20000:      # skip stubs
            time.sleep(1); continue
        # keep prose-dense books (real sentences, dialogue)
        if body.count(".") < 500:
            time.sleep(1); continue
        open(f"{DIET}/gb_{bid}.txt", "w").write(body)
        have.add(bid); got += 1
        total_mb += len(body) / 1e6
        print(f"+book {bid}: {len(body)//1000}KB  (total {got} books, {total_mb:.1f} MB)", flush=True)
        time.sleep(2)             # polite
