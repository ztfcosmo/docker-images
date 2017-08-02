
FROM c12e/alpine-miniconda:conda-4.3.14

ADD conda-spec.txt /conda-spec.txt
RUN conda config --add channels conda-forge \
  && conda install --file /conda-spec.txt \
  && conda remove --force qt pyqt sip \
  && conda clean --all

ENV LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
