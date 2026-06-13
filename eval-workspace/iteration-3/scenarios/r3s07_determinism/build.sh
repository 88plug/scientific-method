#!/bin/bash
# "deterministic" build: bundles sources into build.out
out=build.out
rm -f $out
echo "// build of $(ls src/ | sort | tr '\n' ' ')" > $out
echo "// workdir: $PWD" >> $out
cat src/*.py >> $out
sha256sum $out
