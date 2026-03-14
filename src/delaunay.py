from edge import Edge, makeQuadEdge, splice, connect, deleteEdge
from condition import ccw, inCircle, rightOf, leftOf, valid

def delaunay(s) -> (Edge, Edge):
    # s must be sorted in increasing x direction
    if len(s) == 2:
        a = makeQuadEdge(s[0],s[1])
        return (a, a.sym)
    elif len(s) == 3:
        a = makeQuadEdge(s[0],s[1])
        b = makeQuadEdge(s[1],s[2])
        splice(a.sym,b)
        if ccw(s[0],s[1],s[2]):
            c = connect(b,a)
            return (a,b.sym)
        elif ccw(s[0],s[2],s[1]):
            c = connect(b,a)
            return (c.sym, c)
        else:
            return (a, b.sym)

    else:
        mid = len(s) // 2
        (ldo,ldi) = delaunay(s[:mid])
        (rdi, rdo) = delaunay(s[mid:])

        while True:
            if leftOf(rdi.org, ldi):
                ldi = ldi.lnext
            elif rightOf(ldi.org, rdi):
                rdi = rdi.rprev
            else:
                break
        basel = connect(rdi.sym, ldi)
        if ldi.org == ldo.org:
            ldo = basel.sym
        if rdi.org == rdo.org:
            rdo = basel

        # merge loop
        while True:
            lcand = basel.sym.onext
            if valid(lcand,basel):
                while inCircle(basel.dest,basel.org,lcand.dest,lcand.onext.dest):
                    t = lcand.onext
                    deleteEdge(lcand)
                    lcand = t
            rcand = basel.oprev

            if valid(rcand,basel):
                while inCircle(basel.dest,basel.org,rcand.dest,rcand.oprev.dest):
                    t = rcand.oprev
                    deleteEdge(rcand)
                    rcand = t

            if not valid(lcand,basel) and not valid(rcand,basel):
                break

            if not valid(lcand,basel) or (valid(rcand,basel) and inCircle(lcand.dest, lcand.org, rcand.org, rcand.dest)):
                basel = connect(rcand,basel.sym)
            else:
                basel = connect(basel.sym, lcand.sym)
        return (ldo,rdo)
