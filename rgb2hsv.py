def rgb_to_hsv(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = (maxc-minc) / maxc
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, s, v

def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h*6.0) # XXX assume int() truncates!
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    (r,g,b) = (0,0,0)
    if i == 0:
        (r,g,b) = v, t, p
    if i == 1:
        (r,g,b) = q, v, p
    if i == 2:
        (r,g,b) = p, v, t
    if i == 3:
        (r,g,b) = p, q, v
    if i == 4:
        (r,g,b) = t, p, v
    if i == 5:
        (r,g,b) = v, p, q

    return r*255, g*255, b*255