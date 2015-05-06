from __future__ import print_function, division, absolute_import

import os
import forest


cfg = forest.Tree()
cfg._describe('meta.user', instanceof=str,
              docstring='the name of the user')
cfg._describe('meta.rootpath', instanceof=str,
              docstring='the path towards the data')

uname = os.uname()
if uname[0] == 'Linux':
    cfg.meta.user     = 'fbenurea'
    cfg.meta.rootpath = '/scratch/fbenurea/'
    testset_filepath  = '/home/fbenurea/code/testsets/testset_kinone'
    code_prefix       = '/home/fbenurea/code/testsets/'

elif uname[0] == 'Darwin':
    cfg.meta.user     = 'fabien'
    cfg.meta.rootpath = '~/research/data/'
    testset_filepath  = '/Users/fabien/research/enc/phd/code/testsets/testset_kinone'
    code_prefix       = '/Users/fabien/research/enc/phd/code/testsets/'

else:
    raise ValueError('Platform not known, setup user and rootpath.')

testset_filepaths  = {'kin_one': code_prefix+'testset_kinone',
                      'dmp2d'  : code_prefix+'testset_dmp2d',
                     }
