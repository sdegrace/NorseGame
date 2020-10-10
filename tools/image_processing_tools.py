from math import sqrt


def FloodFill( bitmap, initNode, targetColor, replaceColor ):
   ysize, xsize = bitmap.shape
   Q = []
   if bitmap[ initNode[0], initNode[1] ] != targetColor:
      return Q
   Q.append( initNode )
   while Q != []:
      node = Q.pop(0)
      if bitmap[ node[0], node[1] ] == targetColor:
         W = list( node )
         if node[0] + 1 < xsize:
            E = list( [ node[0] + 1, node[1] ] )
         else:
            E = list( node )
      # Move west until color of node does not match targetColor
      while bitmap[ W[0], W[1] ] == targetColor:
         bitmap[ W[0], W[1] ] = replaceColor
         if W[1] + 1 < ysize:
            if bitmap[ W[0], W[1] + 1 ] == targetColor:
               Q.append( [ W[0], W[1] + 1 ] )
         if W[1] - 1 >= 0:
            if bitmap[ W[0], W[1] - 1 ] == targetColor:
               Q.append( [ W[0], W[1] - 1 ] )
         if W[0] - 1 >= 0:
            W[0] = W[0] - 1
         else:
            break
      # Move east until color of node does not match targetColor
      while bitmap[ E[0], E[1] ] == targetColor:
         bitmap[ E[0], E[1] ] = replaceColor
         if E[1] + 1 < ysize:
            if bitmap[ E[0], E[1] + 1 ] == targetColor:
               Q.append( [ E[0], E[1] + 1 ] )
         if E[1] - 1 >= 0:
            if bitmap[ E[0], E[1] - 1 ] == targetColor:
               Q.append( [ E[0], E[1] -1 ] )
         if E[0] + 1 < xsize:
            E[0] = E[0] + 1
         else:
            break
      return Q

def line(x0, y0, x1, y1):
    "Bresenham's line algorithm"
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    on_points = []
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            on_points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            on_points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    on_points.append((x, y))
    return on_points

def circle(x0, y0, x1, y1):
    radius = round(sqrt(abs(x1-x0)**2 + abs(y1-y0)**2))
    on_points = []
    on_points.append((x0, y0 + radius))

    f = 1 - radius
    ddf_x = 1
    ddf_y = -2 * radius
    x = 0
    y = radius
    while x < y:
        if f >= 0:
            y -= 1
            ddf_y += 2
            f += ddf_y
        x += 1
        ddf_x += 2
        f += ddf_x
        on_points.append((x0 + x, y0 + y))
        on_points.append((x0 - x, y0 + y))
        on_points.append((x0 + x, y0 - y))
        on_points.append((x0 - x, y0 - y))
        on_points.append((x0 + y, y0 + x))
        on_points.append((x0 - y, y0 + x))
        on_points.append((x0 + y, y0 - x))
        on_points.append((x0 - y, y0 - x))
    return on_points

def rectangle(x1, y1, x2, y2):
    points = [(x1, y) for y in range(y1, y2)]
    points.extend((x2, y) for y in range(y1, y2))
    points.extend((x, y1) for x in range(x1, x2))
    points.extend((x, y2) for x in range(x1, x2+1))
    return points

def circle_center_from_3_points(x1, y1, x2, y2, x3, y3):
    ax = (x1 + x2) / 2
    ay = (y1 + y2) / 2
    ux = (y1 - y2)
    uy = (x2 - x1)
    bx = (x2 + x3) / 2
    by = (y2 + y3) / 2
    vx = (y2 - y3)
    vy = (x3 - x2)
    dx = ax - bx
    dy = ay - by
    vu = vx * uy - vy * ux
    if vu == 0:
        return
    g = (dx * uy - dy * ux) / vu
    c_x = bx + g * vx
    c_y = by + g * vy
    return c_x, c_y

def arc(x1, y1, x2, y2, x3, y3):
    x0, y0 = circle_center_from_3_points(x1, y1, x2, y2, x3, y3)

    radius = round(sqrt(abs(x1 - x0) ** 2 + abs(y1 - y0) ** 2))
    on_points = []
    on_points.append((x0, y0 + radius))

    f = 1 - radius
    ddf_x = 1
    ddf_y = -2 * radius
    x = 0
    y = radius
    while x < y:
        if f >= 0:
            y -= 1
            ddf_y += 2
            f += ddf_y
        x += 1
        ddf_x += 2
        f += ddf_x
        on_points.append((x0 + x, y0 + y))
    # f = 1 - radius
    # ddf_x = 1
    # ddf_y = -2 * radius
    # x = 0
    # y = radius
    # while x < y:
    #     if f >= 0:
    #         y -= 1
    #         ddf_y += 2
    #         f += ddf_y
    #     x += 1
    #     ddf_x += 2
    #     f += ddf_x
    #     on_points.append((x0 - x, y0 + y))
    # f = 1 - radius
    # ddf_x = 1
    # ddf_y = -2 * radius
    # x = 0
    # y = radius
    # while x < y:
    #     if f >= 0:
    #         y -= 1
    #         ddf_y += 2
    #         f += ddf_y
    #     x += 1
    #     ddf_x += 2
    #     f += ddf_x
    #     on_points.append((x0 + x, y0 - y))
    # f = 1 - radius
    # ddf_x = 1
    # ddf_y = -2 * radius
    # x = 0
    # y = radius
    # while x < y:
    #     if f >= 0:
    #         y -= 1
    #         ddf_y += 2
    #         f += ddf_y
    #     x += 1
    #     ddf_x += 2
    #     f += ddf_x
    #     on_points.append((x0 - x, y0 - y))
    # f = 1 - radius
    # ddf_x = 1
    # ddf_y = -2 * radius
    # x = 0
    # y = radius
    # while x < y:
    #     if f >= 0:
    #         y -= 1
    #         ddf_y += 2
    #         f += ddf_y
    #     x += 1
    #     ddf_x += 2
    #     f += ddf_x
    #     on_points.append((x0 + y, y0 + x))
    # f = 1 - radius
    # ddf_x = 1
    # ddf_y = -2 * radius
    # x = 0
    # y = radius
    # while x < y:
    #     if f >= 0:
    #         y -= 1
    #         ddf_y += 2
    #         f += ddf_y
    #     x += 1
    #     ddf_x += 2
    #     f += ddf_x
    #     on_points.append((x0 - y, y0 + x))
    #
    # f = 1 - radius
    # ddf_x = 1
    # ddf_y = -2 * radius
    # x = 0
    # y = radius
    # while x < y:
    #     if f >= 0:
    #         y -= 1
    #         ddf_y += 2
    #         f += ddf_y
    #     x += 1
    #     ddf_x += 2
    #     f += ddf_x
    #     on_points.append((x0 + y, y0 - x))
    # f = 1 - radius
    # ddf_x = 1
    # ddf_y = -2 * radius
    # x = 0
    # y = radius
    # while x < y:
    #     if f >= 0:
    #         y -= 1
    #         ddf_y += 2
    #         f += ddf_y
    #     x += 1
    #     ddf_x += 2
    #     f += ddf_x
    #     on_points.append((x0 - y, y0 - x))
    return on_points



def contrasting_text_color(hex_str):
    (r, g, b) = (hex_str[:2], hex_str[2:4], hex_str[4:])
    print(hex_str)
    return '#000000' if 1 - (int(r, 16) * 0.299 + int(g, 16) * 0.587 + int(b, 16) * 0.114) / 255 < 0.5 else '#ffffff'