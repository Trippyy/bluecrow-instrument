import sys, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import ControlBoundsPen
from fontTools.misc.transform import Transform

FP="/Users/Nishant/Library/Application Support/Adobe/CoreSync/plugins/livetype/.r/.41049.otf"
font=TTFont(FP); gs=font.getGlyphSet(); cmap=font.getBestCmap(); hmtx=font["hmtx"]
try:
    kt={}
    for st in font["kern"].kernTables: kt.update(st.kernTable)
except Exception: kt={}

def build(s, tracking=0):
    paths=[]; x=0; prev=None
    bx0=by0=1e9; bx1=by1=-1e9
    for ch in s:
        gn=cmap.get(ord(ch))
        if gn is None: x+=600; prev=None; continue
        if prev is not None: x+=kt.get((prev,gn),0)
        bp=ControlBoundsPen(gs); gs[gn].draw(bp)
        if bp.bounds:
            gx0,gy0,gx1,gy1=bp.bounds
            bx0=min(bx0,gx0+x); bx1=max(bx1,gx1+x)
            by0=min(by0,gy0);   by1=max(by1,gy1)
        sp=SVGPathPen(gs)
        gs[gn].draw(TransformPen(sp, Transform(1,0,0,-1,x,0)))
        d=sp.getCommands()
        if d: paths.append(d)
        x+=hmtx[gn][0]+tracking; prev=gn
    if bx0>bx1: bx0,by0,bx1,by1=0,0,x,1000
    w=bx1-bx0; h=by1-by0
    return {"d":" ".join(paths), "viewBox":f"{bx0:.0f} {-by1:.0f} {w:.0f} {h:.0f}",
            "ar": round(w/h,4)}

words=json.loads(sys.argv[1])
print(json.dumps({k:build(v[0],v[1]) for k,v in words.items()}))
