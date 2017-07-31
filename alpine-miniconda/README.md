
# alpine-miniconda

This image uses `conda` to install packages inside an Alpine Linux container.
To add a new package, add a line to conda-spec.txt.

## Known issues

- All packages are installed in the root environment. Since this is a single-purpose image, this might not be so bad.
- No compiler is included, so this can't be used to build conda packages with C/C++ components. Existing packages from anaconda.org can be installed just fine, though.