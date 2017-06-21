#!/usr/bin/env python

import getpass, socket
print('*** I am {} on {} ***'.format(getpass.getuser(), socket.gethostname()))

import sncosmo

result, model = sncosmo.fit_lc(sncosmo.load_example_data(), sncosmo.Model('salt2'), vparam_names=['c', 't0', 'x0', 'x1'])
for k in sorted(result.keys()):
    print('{}: {}'.format(k, result[k]))
