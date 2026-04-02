#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RM_LITERAL_PREFIX="${RM_LITERAL_PREFIX:-$HOME/.conda-envs/rm-literal}"
PKGCONFIG_DIR="$RM_LITERAL_PREFIX/lib/pkgconfig"

micromamba create -y -p "$RM_LITERAL_PREFIX" -c conda-forge \
  python=3.10 \
  pip \
  wheel \
  "setuptools<60" \
  numpy=1.23.5 \
  scipy \
  pandas \
  matplotlib \
  emcee \
  mpi4py \
  cython \
  pkgconfig \
  openmpi \
  gsl \
  libhwloc \
  liblapacke \
  openblas

mkdir -p "$RM_LITERAL_PREFIX/bin" "$PKGCONFIG_DIR"
ln -sf "$(command -v gfortran)" "$RM_LITERAL_PREFIX/bin/gfortran"
ln -sf "$(command -v gfortran)" "$RM_LITERAL_PREFIX/bin/f95"
ln -sf "$(command -v gfortran)" "$RM_LITERAL_PREFIX/bin/f77"
ln -sf "$(command -v gcc)" "$RM_LITERAL_PREFIX/bin/gcc"
ln -sf "$(command -v gcc)" "$RM_LITERAL_PREFIX/bin/cc"
ln -sf "$(command -v gcc)" "$RM_LITERAL_PREFIX/bin/x86_64-conda-linux-gnu-cc"
if command -v g++ >/dev/null 2>&1; then
  ln -sf "$(command -v g++)" "$RM_LITERAL_PREFIX/bin/c++"
  ln -sf "$(command -v g++)" "$RM_LITERAL_PREFIX/bin/x86_64-conda-linux-gnu-c++"
fi
ln -sf "$(command -v gfortran)" "$RM_LITERAL_PREFIX/bin/x86_64-conda-linux-gnu-gfortran"

cat > "$PKGCONFIG_DIR/hwloc.pc" <<PC
prefix=$RM_LITERAL_PREFIX
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
includedir=\${prefix}/include

Name: hwloc
Description: Portable Hardware Locality
Version: 2.13.0
Libs: -L\${libdir} -lhwloc
Cflags: -I\${includedir}
PC

cat > "$PKGCONFIG_DIR/lapacke.pc" <<PC
prefix=$RM_LITERAL_PREFIX
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
includedir=\${prefix}/include

Name: lapacke
Description: C interface to LAPACK
Version: 3.11.0
Libs: -L\${libdir} -llapacke -llapack -lopenblas
Cflags: -I\${includedir}
PC

export PATH="$RM_LITERAL_PREFIX/bin:$PATH"
export PKG_CONFIG_PATH="$PKGCONFIG_DIR${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
export CC=mpicc
export FC=gfortran
export F77=f77
export OMPI_CC=x86_64-conda-linux-gnu-cc
export OMPI_CXX=x86_64-conda-linux-gnu-c++
export OMPI_FC=x86_64-conda-linux-gnu-gfortran

"$RM_LITERAL_PREFIX/bin/python" -m pip install --no-build-isolation --no-cache-dir \
  git+https://github.com/nye17/javelin.git
"$RM_LITERAL_PREFIX/bin/python" -m pip install --no-build-isolation --no-cache-dir \
  git+https://github.com/LiyrAstroph/MICA2.git

cd "$ROOT"
uv venv .uv-pypetal --python "$RM_LITERAL_PREFIX/bin/python" --seed
./.uv-pypetal/bin/python -m pip install --upgrade pip
./.uv-pypetal/bin/python -m pip install \
  numpy==1.22.4 \
  pypetal \
  pyzdcf \
  PyROA

uv venv .uv-litmus --python "$RM_LITERAL_PREFIX/bin/python" --seed
./.uv-litmus/bin/python -m pip install --upgrade pip
./.uv-litmus/bin/python -m pip install litmus-rm
