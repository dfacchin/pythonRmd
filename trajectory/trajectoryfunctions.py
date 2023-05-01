import math

def calc_time(d,a,v):
    try:
        t = (math.sqrt((2*d)/a + v*v)-v)/a
    except:
        t = 0
    return t
def calc_a(d,vi,vf):
    a = (vf*vf-vi*vi)/(2*d)
    return a
"""
d = vi*t +(a*t^2)/2
(vf-vi)/t = a

"""
def calc_vi_dat(d,a,t):
    #vi = a/(2*t*d)
    vi = (d/t)-(a*t)/2
    return vi

def calc_t(vi,vf,a):
    t = (vf-vi)/a
    return t
def calc_t_dva(d,vi,a):
    try:
        t = (math.sqrt((2*d*a) + (vi*vi)) - vi) / a
    except:
        t = 0
    return t
def cald_d(vi,a,t):
    d = vi*t + (a*t*t)/2
    return d
def calc_a_dvt(d,v,t):
    a = (d-v*t)*(2/(t*t))
    return a
def calc_vf_dva(d,vi,a):
    #works if it "goes" straight
    try:
        vf = math.sqrt(2*a*d+vi*vi)
    except:
        vf = 0
    return vf
def calc_vf_dvt(d,v,t):
    vf = (2*d/t)-v
    return vf


if __name__ == "__main__":
    d = 0.1
    a = 1
    t = 1
    print(calc_vi_dat(d,a,t))