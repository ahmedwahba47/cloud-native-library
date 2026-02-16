"""
Vector diagrams for Cloud-Native System Report.
Uses ReportLab Drawing objects for professional PDF integration.
"""

import math
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Group, Circle
from reportlab.lib.colors import HexColor

# Consistent color palette
PRIMARY = HexColor('#2c5282')
SECONDARY = HexColor('#3182ce')
ACCENT = HexColor('#ebf8ff')
TEXT_COLOR = HexColor('#2d3748')
BORDER = HexColor('#a0aec0')
GREEN = HexColor('#48bb78')
GREEN_LIGHT = HexColor('#c6f6d5')
ORANGE = HexColor('#ed8936')
ORANGE_LIGHT = HexColor('#feebc8')
WHITE = HexColor('#ffffff')
LIGHT_GRAY = HexColor('#f7fafc')
DARK_BLUE = HexColor('#1a365d')


def _draw_arrow(d, x1, y1, x2, y2, color=PRIMARY, stroke_width=1.5, head_size=7):
    """Draw a line with an arrowhead pointing from (x1,y1) to (x2,y2)."""
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=stroke_width))
    angle = math.atan2(y2 - y1, x2 - x1)
    lx = x2 - head_size * math.cos(angle - math.pi / 6)
    ly = y2 - head_size * math.sin(angle - math.pi / 6)
    rx = x2 - head_size * math.cos(angle + math.pi / 6)
    ry = y2 - head_size * math.sin(angle + math.pi / 6)
    d.add(Polygon(
        points=[x2, y2, lx, ly, rx, ry],
        fillColor=color, strokeColor=color, strokeWidth=0.5
    ))


def _draw_service_box(d, x, y, w, h, name, port, fill=ACCENT, stroke=PRIMARY):
    """Draw a service box with name and port number."""
    d.add(Rect(x, y, w, h, rx=6, ry=6,
               fillColor=fill, strokeColor=stroke, strokeWidth=1.5))
    d.add(String(x + w / 2, y + h / 2 + 2, name,
                 fontSize=9, fillColor=TEXT_COLOR, textAnchor='middle',
                 fontName='Helvetica-Bold'))
    d.add(String(x + w / 2, y + h / 2 - 12, f':{port}',
                 fontSize=8, fillColor=BORDER, textAnchor='middle',
                 fontName='Helvetica'))


def create_system_architecture():
    """Create a system architecture diagram showing 6 components.
    Client -> API Gateway -> {Eureka, Library API, Catalog Service, Config Server, Zipkin}
    Catalog Service -> Library API (inter-service call)
    """
    width = 470
    height = 310
    d = Drawing(width, height)

    box_w = 120
    box_h = 44
    small_box_w = 100
    small_box_h = 40

    # Client box - left side
    client_x = 10
    client_y = height / 2 - box_h / 2 + 20
    d.add(Rect(client_x, client_y, 60, box_h, rx=6, ry=6,
               fillColor=LIGHT_GRAY, strokeColor=BORDER, strokeWidth=1.5))
    d.add(String(client_x + 30, client_y + box_h / 2 - 4, 'Client',
                 fontSize=10, fillColor=TEXT_COLOR, textAnchor='middle',
                 fontName='Helvetica-Bold'))

    # API Gateway - center-left
    gw_x = 100
    gw_y = client_y
    _draw_service_box(d, gw_x, gw_y, box_w, box_h, 'API Gateway', '8080',
                      fill=HexColor('#e2e8f0'), stroke=DARK_BLUE)

    # Arrow: Client -> Gateway
    _draw_arrow(d, client_x + 60, client_y + box_h / 2,
                gw_x, gw_y + box_h / 2, color=DARK_BLUE)

    # Right-side services (stacked vertically)
    svc_x = 280
    svc_gap = 8

    services = [
        ('Eureka Server', '8761', HexColor('#feebc8'), ORANGE),
        ('Library API (B)', '8081', ACCENT, PRIMARY),
        ('Catalog Service (A)', '8082', ACCENT, PRIMARY),
        ('Config Server', '8888', GREEN_LIGHT, GREEN),
        ('Zipkin Tracing', '9411', LIGHT_GRAY, BORDER),
    ]

    total_svc_h = len(services) * small_box_h + (len(services) - 1) * svc_gap
    svc_start_y = height / 2 + total_svc_h / 2 + 10

    svc_positions = {}
    for i, (name, port, fill, stroke) in enumerate(services):
        sy = svc_start_y - i * (small_box_h + svc_gap) - small_box_h
        _draw_service_box(d, svc_x, sy, 170, small_box_h, name, port,
                          fill=fill, stroke=stroke)
        svc_positions[name] = (svc_x, sy, 170, small_box_h)

    # Arrows from Gateway to each service
    gw_right = gw_x + box_w
    gw_cy = gw_y + box_h / 2
    for name, (sx, sy, sw, sh) in svc_positions.items():
        target_y = sy + sh / 2
        _draw_arrow(d, gw_right, gw_cy, sx, target_y, color=SECONDARY,
                    stroke_width=1.0, head_size=5)

    # Inter-service arrow: Catalog Service -> Library API
    cat_pos = svc_positions['Catalog Service (A)']
    lib_pos = svc_positions['Library API (B)']
    cat_top = cat_pos[1] + cat_pos[3]
    lib_bot = lib_pos[1]
    mid_x = cat_pos[0] + cat_pos[2] - 20
    _draw_arrow(d, mid_x, cat_top, mid_x, lib_bot,
                color=ORANGE, stroke_width=1.5)
    d.add(String(mid_x + 5, (cat_top + lib_bot) / 2 - 3, 'Feign',
                 fontSize=7, fillColor=ORANGE, textAnchor='start',
                 fontName='Helvetica-Oblique'))

    # Legend at bottom
    legend_y = 8
    d.add(String(10, legend_y, 'Legend:',
                 fontSize=8, fillColor=TEXT_COLOR, textAnchor='start',
                 fontName='Helvetica-Bold'))
    # Gateway arrow
    d.add(Line(55, legend_y + 3, 75, legend_y + 3,
               strokeColor=SECONDARY, strokeWidth=1))
    d.add(String(78, legend_y, 'Routes to',
                 fontSize=8, fillColor=TEXT_COLOR, textAnchor='start',
                 fontName='Helvetica'))
    # Feign arrow
    d.add(Line(135, legend_y + 3, 155, legend_y + 3,
               strokeColor=ORANGE, strokeWidth=1.5))
    d.add(String(158, legend_y, 'Inter-service call',
                 fontSize=8, fillColor=TEXT_COLOR, textAnchor='start',
                 fontName='Helvetica'))

    return d


def create_circuit_breaker_states():
    """Create a circuit breaker state diagram.
    Closed -> Open -> Half-Open -> Closed
    With transition conditions on arrows.
    """
    width = 470
    height = 180
    d = Drawing(width, height)

    box_w = 110
    box_h = 50
    mid_y = height / 2

    # State positions (left to right)
    closed_x = 30
    open_x = 180
    half_x = 330

    closed_y = mid_y - box_h / 2
    open_y = mid_y - box_h / 2
    half_y = mid_y - box_h / 2

    # Closed state (green - normal operation)
    d.add(Rect(closed_x, closed_y, box_w, box_h, rx=8, ry=8,
               fillColor=GREEN_LIGHT, strokeColor=GREEN, strokeWidth=2))
    d.add(String(closed_x + box_w / 2, closed_y + box_h / 2 + 4, 'CLOSED',
                 fontSize=12, fillColor=TEXT_COLOR, textAnchor='middle',
                 fontName='Helvetica-Bold'))
    d.add(String(closed_x + box_w / 2, closed_y + box_h / 2 - 10, '(normal)',
                 fontSize=8, fillColor=GREEN, textAnchor='middle',
                 fontName='Helvetica'))

    # Open state (red/orange - blocking)
    d.add(Rect(open_x, open_y, box_w, box_h, rx=8, ry=8,
               fillColor=ORANGE_LIGHT, strokeColor=ORANGE, strokeWidth=2))
    d.add(String(open_x + box_w / 2, open_y + box_h / 2 + 4, 'OPEN',
                 fontSize=12, fillColor=TEXT_COLOR, textAnchor='middle',
                 fontName='Helvetica-Bold'))
    d.add(String(open_x + box_w / 2, open_y + box_h / 2 - 10, '(blocking)',
                 fontSize=8, fillColor=ORANGE, textAnchor='middle',
                 fontName='Helvetica'))

    # Half-Open state (blue - testing)
    d.add(Rect(half_x, half_y, box_w, box_h, rx=8, ry=8,
               fillColor=ACCENT, strokeColor=SECONDARY, strokeWidth=2))
    d.add(String(half_x + box_w / 2, half_y + box_h / 2 + 4, 'HALF-OPEN',
                 fontSize=12, fillColor=TEXT_COLOR, textAnchor='middle',
                 fontName='Helvetica-Bold'))
    d.add(String(half_x + box_w / 2, half_y + box_h / 2 - 10, '(testing)',
                 fontSize=8, fillColor=SECONDARY, textAnchor='middle',
                 fontName='Helvetica'))

    # Arrow: Closed -> Open (top path)
    ax1 = closed_x + box_w
    ay1 = closed_y + box_h - 8
    ax2 = open_x
    ay2 = open_y + box_h - 8
    _draw_arrow(d, ax1, ay1, ax2, ay2, color=ORANGE, stroke_width=1.5)
    d.add(String((ax1 + ax2) / 2, ay1 + 10, 'Failure rate >= 50%',
                 fontSize=8, fillColor=ORANGE, textAnchor='middle',
                 fontName='Helvetica'))

    # Arrow: Open -> Half-Open (top path)
    bx1 = open_x + box_w
    by1 = open_y + box_h - 8
    bx2 = half_x
    by2 = half_y + box_h - 8
    _draw_arrow(d, bx1, by1, bx2, by2, color=SECONDARY, stroke_width=1.5)
    d.add(String((bx1 + bx2) / 2, by1 + 10, 'Wait 10s timeout',
                 fontSize=8, fillColor=SECONDARY, textAnchor='middle',
                 fontName='Helvetica'))

    # Arrow: Half-Open -> Closed (curved, below)
    # Draw as a path going below the boxes
    low_y = closed_y - 30
    # Line segments: half-open bottom -> down -> left -> up -> closed bottom
    hx_mid = half_x + box_w / 2
    cx_mid = closed_x + box_w / 2

    d.add(Line(hx_mid, half_y, hx_mid, low_y,
               strokeColor=GREEN, strokeWidth=1.5))
    d.add(Line(hx_mid, low_y, cx_mid, low_y,
               strokeColor=GREEN, strokeWidth=1.5))
    _draw_arrow(d, cx_mid, low_y, cx_mid, closed_y,
                color=GREEN, stroke_width=1.5)
    d.add(String((hx_mid + cx_mid) / 2, low_y - 12, 'Test calls succeed',
                 fontSize=8, fillColor=GREEN, textAnchor='middle',
                 fontName='Helvetica'))

    # Arrow: Half-Open -> Open (failure, going back above)
    high_y = open_y + box_h + 30
    ox_mid = open_x + box_w / 2

    d.add(Line(half_x, half_y + box_h / 2 + 8, half_x - 15, high_y,
               strokeColor=ORANGE, strokeWidth=1.0, strokeDashArray=[3, 3]))
    d.add(Line(half_x - 15, high_y, ox_mid, high_y,
               strokeColor=ORANGE, strokeWidth=1.0, strokeDashArray=[3, 3]))
    _draw_arrow(d, ox_mid, high_y, ox_mid, open_y + box_h,
                color=ORANGE, stroke_width=1.0, head_size=5)
    d.add(String((half_x - 15 + ox_mid) / 2, high_y + 6, 'Test calls fail',
                 fontSize=7, fillColor=ORANGE, textAnchor='middle',
                 fontName='Helvetica-Oblique'))

    return d
