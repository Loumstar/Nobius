from math import pi, sin, cos

def get_arc_path(minutes, r, cx, cy):
    arc = 2 * pi * minutes / 60

    dx = r * sin(arc)
    dy = r * (1 - cos(arc))
    flags = "0,1" if minutes < 30 else "1,1"

    return f"M {cx},{cy - r} a {r},{r} 90 {flags} {dx},{dy}"

def get_ticks(minutes, r_lb, r_ub, cx, cy):
    arc = 2 * pi * minutes / 60
    
    x_lb = cx + (r_lb * sin(arc))
    y_lb = cy - (r_lb * cos(arc))
    x_ub = cx + (r_ub * sin(arc))
    y_ub = cy - (r_ub * cos(arc))

    return f"M {x_lb},{y_lb} L {x_ub},{y_ub}"