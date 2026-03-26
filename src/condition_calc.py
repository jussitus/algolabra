from point import Point


def incircle_int_exact(a: Point, b: Point, c: Point, d: Point) -> bool:
    ax = a[0]
    bx = b[0]
    cx = c[0]
    dx = d[0]

    ay = a[1]
    by = b[1]
    cy = c[1]
    dy = d[1]

    az = ax**2 + ay**2
    bz = bx**2 + by**2
    cz = cx**2 + cy**2
    dz = dx**2 + dy**2

    """
    ax ay az 1
    bx by bz 1
    cx cy cz 1
    dx dy dz 1

    subtract fourth row from other three

    (ax-dx) (ay-dy) (az-dz) 0
    (bx-dx) (by-dy) (bz-dz) 0
    (cx-dx) (cy-dy) (cz-dz) 0
      dx      dy      dz    1

    """

    f00 = ax - dx
    f01 = ay - dy
    f02 = az - dz

    f10 = bx - dx
    f11 = by - dy
    f12 = bz - dz

    f20 = cx - dx
    f21 = cy - dy
    f22 = cz - dz

    """
    f00 f01 f02
    f10 f11 f12
    f20 f21 f22

    """

    det = (
        f00 * (f11 * f22 - f12 * f21)
        - f01 * (f10 * f22 - f12 * f20)
        + f02 * (f10 * f21 - f11 * f20)
    )
    return det > 0


def ccw_int_exact(a: Point, b: Point, c: Point) -> bool:
    ax = a[0]
    bx = b[0]
    cx = c[0]

    ay = a[1]
    by = b[1]
    cy = c[1]

    """
    (ax-cx) (ay-cy) 0
    (bx-cx) (by-cy) 0
      cx      cy    1

    """
    d00 = ax - cx
    d01 = ay - cy
    d10 = bx - cx
    d11 = by - cy
    """
    d00 d01
    d10 d11
    """
    det = d00 * d11 - d01 * d10

    return det > 0
