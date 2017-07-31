
FROM c12e/alpine-miniconda:conda-4.3.14

ADD conda-spec.txt /conda-spec.txt
RUN conda config conda config --add channels conda-forge \
  && conda install --file /conda-spec.txt
  && conda clean --all