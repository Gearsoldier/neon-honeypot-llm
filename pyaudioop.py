# Minimal shim for Python 3.13 where audioop is gone.
# We don't actually use audio features, so safe no-ops.
def rms(fragment, width): return 0
def avg(fragment, width): return 0
def maxpp(fragment, width): return 0
def minmax(fragment, width): return (0, 0)
def tostereo(fragment, width, left, right): return fragment
def add(fragment1, fragment2, width): return fragment1
def mul(fragment, width, factor): return fragment
def bias(fragment, width, add): return fragment
def lin2lin(fragment, width, newwidth): return fragment
def ratecv(fragment, width, nchannels, inrate, outrate, state, weightA=1, weightB=0): return (fragment, None)
def byteswap(fragment, width): return fragment
