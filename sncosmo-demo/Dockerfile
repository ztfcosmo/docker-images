
FROM ztfcosmology/ubuntu-python3:latest

# install sncosmo and fetch model data
RUN pip3 install sncosmo==1.5.1 iminuit==1.2 \
 && python -c "import sncosmo; sncosmo.Model('salt2'); [sncosmo.get_bandpass('sdss'+band) for band in 'ugriz']"

# execute demo when container starts
ADD sncosmo_demo.py /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/sncosmo_demo.py"]
