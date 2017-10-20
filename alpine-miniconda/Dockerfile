
FROM c12e/alpine-miniconda:conda-4.3.14

ADD conda-spec.txt /conda-spec.txt
RUN conda config --add channels conda-forge; sync \
  && conda install --file /conda-spec.txt; sync \
  && conda remove --force qt pyqt sip; sync \
  && conda clean --all; sync

RUN apk --update add perl

RUN mkdir /acs /afs /batch /cvmfs /lustre /net /usr/gridengine

ENV LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
