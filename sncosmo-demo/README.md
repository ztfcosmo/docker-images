# Demo: sncosmo in a Singularity image via Docker

Here we demonstrate a container workflow, using [Docker](https://www.docker.com) to create images that will be executed with [Singularity](http://singularity.lbl.gov).

This is a bit of overkill for
[sncosmo](http://sncosmo.readthedocs.io/en/v1.5.1/), as it depends mostly on
nicely-packaged dependencies that can be installed with `pip` and isolated in a
virtualenv. Still, it can be a pain to build e.g. scipy from scratch, and to
deploy your environment on a cluster with no shared accessible from the submit
node. This is especially true in cases where you're running opportunistically
on a set of remote sites that may change every week. As long as the remote
admins are willing to install Singularity, though, you can just copy in a
single (large) file and be running in minutes.

## Docker image

First, clone this repo to a machine where you have Docker installed (and have admin rights):

```
git clone git@github.com:ztfcosmo/docker-images.git && cd docker-images/sncosmo-demo
```

Then, build the demo image. We'll call it `sncosmo`:

```
docker build -t sncosmo .
```

Executing the image will run the default entry point (the demo script shipped in the git repository):

```
docker run --rm sncosmo
*** I am root on c069cb651672 ***
chisq: 124.60107115345085
covariance: [[  2.72494078e-01  -5.20203746e-08   5.68395451e-03   2.51680894e-02]
 [ -5.20203746e-08   9.85514189e-14  -5.41566808e-09  -4.65311983e-08]
 [  5.68395451e-03  -5.41566808e-09   1.10208867e-01   2.49875595e-03]
 [  2.51680894e-02  -4.65311983e-08   2.49875595e-03   2.21960773e-02]]
data_mask: [ True  True  True False  True  True  True False  True  True  True False
  True  True  True False  True  True  True False  True  True  True False
  True  True  True False  True  True  True False  True  True  True False
  True  True  True False]
errors: OrderedDict([('t0', 0.5220053033735894), ('x0', 3.139290029302165e-07), ('x1', 0.33197720811197756), ('c', 0.14898347983305252)])
message: Minimization exited successfully.
ncall: 416
ndof: 26
nfit: 1
param_names: ['z', 't0', 'x0', 'x1', 'c']
parameters: [  0.00000000e+00   5.50986757e+04   1.28807239e-06  -8.61532837e-01
   1.93219345e+00]
success: True
vparam_names: ['t0', 'x0', 'x1', 'c']
```

The `--rm` flag discards changes to the container's filesystem when it exits,
ensuring repeatability.

## Docker to Singularity conversion

Singularity 2.3 can import Docker images directly without root privileges, but
until it is widely deployed you'll have to convert the Docker image to
Singularity format on your own machine using the handy `docker2singularity`
utility. The `docker2singularity.sh` wrapper script does this for you:

```
./docker2singularity.sh sncosmo
Size: 967 MB for the singularity container
(1/9) Creating an empty image...
Creating a sparse image with a maximum size of 967MiB...
Using given image size of 967
Formatting image (/sbin/mkfs.ext3)
Done. Image can be found at: /tmp/sncosmo-2017-06-21-20a50d68c95e.img
(2/9) Importing filesystem...
(3/9) Bootstrapping...
(4/9) Adding run script...
(5/9) Setting ENV variables...
Singularity: sexec (U=0,P=136)> Command=exec, Container=/tmp/sncosmo-2017-06-21-20a50d68c95e.img, CWD=/, Arg1=/bin/sh
(6/9) Adding mount points...
Singularity: sexec (U=0,P=142)> Command=exec, Container=/tmp/sncosmo-2017-06-21-20a50d68c95e.img, CWD=/, Arg1=/bin/sh
(7/9) Fixing permissions...
Singularity: sexec (U=0,P=148)> Command=exec, Container=/tmp/sncosmo-2017-06-21-20a50d68c95e.img, CWD=/, Arg1=/bin/sh
We're running on BusyBox/Buildroot
Singularity: sexec (U=0,P=181)> Command=exec, Container=/tmp/sncosmo-2017-06-21-20a50d68c95e.img, CWD=/, Arg1=/bin/sh
(8/9) Stopping and removing the container...
20a50d68c95e
20a50d68c95e
(9/9) Moving the image to the output folder...
  1,013,973,024 100%   73.56MB/s    0:00:13 (xfr#1, to-chk=0/1)
```

Now, copy the image (in this example, `sncosmo-2017-06-21-20a50d68c95e.img`) to the submit node of your favorite shared cluster.

## Executing with Singularity

First, we can run the container directly on the submit node:

```
./sncosmo-2017-06-21-20a50d68c95e.img 
*** I am jvsanten on wgs04.zeuthen.desy.de ***
chisq: 124.60107115345085
covariance: [[  2.72494078e-01  -5.20203746e-08   5.68395451e-03   2.51680894e-02]
 [ -5.20203746e-08   9.85514189e-14  -5.41566808e-09  -4.65311983e-08]
 [  5.68395451e-03  -5.41566808e-09   1.10208867e-01   2.49875595e-03]
 [  2.51680894e-02  -4.65311983e-08   2.49875595e-03   2.21960773e-02]]
data_mask: [ True  True  True False  True  True  True False  True  True  True False
  True  True  True False  True  True  True False  True  True  True False
  True  True  True False  True  True  True False  True  True  True False
  True  True  True False]
errors: OrderedDict([('t0', 0.5220053033735894), ('x0', 3.139290029302165e-07), ('x1', 0.33197720811197756), ('c', 0.14898347983305252)])
message: Minimization exited successfully.
ncall: 416
ndof: 26
nfit: 1
param_names: ['z', 't0', 'x0', 'x1', 'c']
parameters: [  0.00000000e+00   5.50986757e+04   1.28807239e-06  -8.61532837e-01
   1.93219345e+00]
success: True
vparam_names: ['t0', 'x0', 'x1', 'c']
```

There are a couple of differences to the Docker version above. First, the image
itself is executable, which is kind of neat. Also, I am now a normal user
instead of root. The complete lack of privilege escalation is one of the things
that seems to make academic computing folk more comfortable with Singularity
than with Docker. Also, container changes are discarded by default (so `--rm`
is on by default; use `singularity --writable run
sncosmo-2017-06-21-20a50d68c95e.img` to save changes), and the process in the
image is attached to the calling tty by default (so `-it` is on by default).

Running on a single machine where we don't have root is not much of an
improvement over running on our laptop. The neat thing, however, is that it's
very straightforward to submit a Singularity image as a job to a batch system.
For example, using UGE we would do:

```
qsub -j y -cwd -l h_rt=00:01:00 -b y sncosmo-2017-06-21-6f6d6f1aab00.img 
Your job 20536421 ("singularity") has been submitted
```

The output in the log file is identical to the version that ran on our laptop
and on the submit node:

```
cat singularity.o20536421 
*** I am jvsanten on bladeg1.zeuthen.desy.de ***
chisq: 124.60107115345085
covariance: [[  2.72494078e-01  -5.20203746e-08   5.68395451e-03   2.51680894e-02]
 [ -5.20203746e-08   9.85514189e-14  -5.41566808e-09  -4.65311983e-08]
 [  5.68395451e-03  -5.41566808e-09   1.10208867e-01   2.49875595e-03]
 [  2.51680894e-02  -4.65311983e-08   2.49875595e-03   2.21960773e-02]]
data_mask: [ True  True  True False  True  True  True False  True  True  True False
  True  True  True False  True  True  True False  True  True  True False
  True  True  True False  True  True  True False  True  True  True False
  True  True  True False]
errors: OrderedDict([('t0', 0.5220053033735894), ('x0', 3.139290029302165e-07), ('x1', 0.33197720811197756), ('c', 0.14898347983305252)])
message: Minimization exited successfully.
ncall: 416
ndof: 26
nfit: 1
param_names: ['z', 't0', 'x0', 'x1', 'c']
parameters: [  0.00000000e+00   5.50986757e+04   1.28807239e-06  -8.61532837e-01
   1.93219345e+00]
success: True
vparam_names: ['t0', 'x0', 'x1', 'c']
```

In this case these 3 machines were all running different operating systems, but
we could still run exactly the same image.

