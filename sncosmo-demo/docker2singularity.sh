#!/bin/sh

# Convert docker image to Singularity format
# (not needed for Singularity >= 2.3, which can import Docker containers directly without root privs)
docker run -v `pwd`:/output -v /var/run/docker.sock:/var/run/docker.sock --privileged -t --rm singularityware/docker2singularity -m "/acs /afs /cvmfs /lustre /net" $1
