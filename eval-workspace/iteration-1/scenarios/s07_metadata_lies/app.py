import os, time
CACHE_ENABLED = os.environ.get("ENABLE_CACHE", "false").lower() == "true"
_cache={}
def fetch(key):
    if CACHE_ENABLED and key in _cache: return _cache[key]
    time.sleep(0.05)  # simulated backend call
    val=f"value-{key}"
    if CACHE_ENABLED: _cache[key]=val
    return val
if __name__=="__main__":
    t0=time.perf_counter()
    for _ in range(20): fetch("hot")
    print(f"cache_enabled={CACHE_ENABLED} 20 hot fetches in {time.perf_counter()-t0:.2f}s")
