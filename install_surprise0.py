import sys, os

# # Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
#
# # Restore
def enablePrint():
    sys.stdout = sys.__stdout__

blockPrint()

def run_once():
    import pip

    try:
        from pip import main as pipmain
    except:
        from pip._internal import main as pipmain

    with open("requirements0.txt") as f:
        for line in f:
        # call pip's main function with each requirement
            pipmain(['install','-U', line])

    run_once.func_code = (lambda:None).func_code

run_once()

enablePrint()

import os
os.system('pip install scikit-surprise==1.0.4')

import surprise


import site
reload(site)
