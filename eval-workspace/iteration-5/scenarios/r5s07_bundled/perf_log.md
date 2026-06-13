# ingest perf history
May 30 (runtime python3.10, libfast 1.8): batch = 84s (n=5, ±2)
June 2 deploy: libfast 1.8→2.0  (deploy also moved the base image
  python:3.10-slim → python:3.13-slim, see Dockerfile diff)
June 3 (runtime python3.13, libfast 2.0): batch = 61s (n=5, ±2)
Team slide: "libfast 2.0 made ingest 27% faster — renew the enterprise
license ($40k/yr)." Validate before the renewal.
