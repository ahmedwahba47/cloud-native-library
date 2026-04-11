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
    """Create a system architecture diagram showing all components.
    Client -> API Gateway -> {Services}
    Service A (2 instances) -> Service B (inter-service call via Feign)
    Service A shares PostgreSQL database
    """
    width = 470
    height = 370
    d = Drawing(width, height)

    box_h = 40
    svc_w = 140

    # --- Title ---
    d.add(String(width / 2, height - 12, 'Cloud-Native System Architecture',
                 fontSize=11, fillColor=DARK_BLUE, textAnchor='middle',
                 fontName='Helvetica-Bold'))

    # --- Client (far left) ---
    cx, cy = 10, 195
    d.add(Rect(cx, cy, 55, 40, rx=4, ry=4,
               fillColor=LIGHT_GRAY, strokeColor=BORDER, strokeWidth=1.5))
    d.add(String(cx + 27, cy + 16, 'Client',
                 fontSize=9, fillColor=TEXT_COLOR, textAnchor='middle',
                 fontName='Helvetica-Bold'))

    # --- API Gateway ---
    gw_x, gw_y = 90, 190
    d.add(Rect(gw_x, gw_y, 100, 50, rx=6, ry=6,
               fillColor=HexColor('#e2e8f0'), strokeColor=DARK_BLUE, strokeWidth=2))
    d.add(String(gw_x + 50, gw_y + 30, 'API Gateway',
                 fontSize=9, fillColor=TEXT_COLOR, textAnchor='middle',
                 fontName='Helvetica-Bold'))
    d.add(String(gw_x + 50, gw_y + 17, ':8080 | OAuth2/JWT | lb://',
                 fontSize=7, fillColor=BORDER, textAnchor='middle',
                 fontName='Helvetica'))
    d.add(String(gw_x + 50, gw_y + 6, 'Load Balanced Routing',
                 fontSize=6, fillColor=SECONDARY, textAnchor='middle',
                 fontName='Helvetica-Oblique'))
    _draw_arrow(d, cx + 55, cy + 20, gw_x, gw_y + 25, color=DARK_BLUE)

    # --- Infrastructure row (top) ---
    infra_y = 310
    # Eureka
    d.add(Rect(220, infra_y, svc_w, box_h, rx=6, ry=6,
               fillColor=ORANGE_LIGHT, strokeColor=ORANGE, strokeWidth=1.5))
    d.add(String(220 + svc_w / 2, infra_y + 22, 'Eureka Server',
                 fontSize=9, fillColor=TEXT_COLOR, textAnchor='middle',
                 fontName='Helvetica-Bold'))
    d.add(String(220 + svc_w / 2, infra_y + 9, ':8761 | Service Registry',
                 fontSize=7, fillColor=BORDER, textAnchor='middle',
                 fontName='Helvetica'))

    # Config Server
    d.add(Rect(220, infra_y - 52, svc_w, box_h, rx=6, ry=6,
               fillColor=GREEN_LIGHT, strokeColor=GREEN, strokeWidth=1.5))
    d.add(String(220 + svc_w / 2, infra_y - 52 + 22, 'Config Server',
                 fontSize=9, fillColor=TEXT_COLOR, textAnchor='middle',
                 fontName='Helvetica-Bold'))
    d.add(String(220 + svc_w / 2, infra_y - 52 + 9, ':8888 | Centralised Config',
                 fontSize=7, fillColor=BORDER, textAnchor='middle',
                 fontName='Helvetica'))

    # --- Service B: Library API (right side, middle) ---
    lib_x, lib_y = 220, 185
    d.add(Rect(lib_x, lib_y, svc_w, 60, rx=6, ry=6,
               fillColor=ACCENT, strokeColor=PRIMARY, strokeWidth=1.5))
    d.add(String(lib_x + svc_w / 2, lib_y + 42, 'Library API',
                 fontSize=10, fillColor=TEXT_COLOR, textAnchor='middle',
                 fontName='Helvetica-Bold'))
    d.add(String(lib_x + svc_w / 2, lib_y + 28, 'Service B | :8081',
                 fontSize=7, fillColor=BORDER, textAnchor='middle',
                 fontName='Helvetica'))
    d.add(String(lib_x + svc_w / 2, lib_y + 15, 'Books & Loans',
                 fontSize=7, fillColor=PRIMARY, textAnchor='middle',
                 fontName='Helvetica-Oblique'))
    d.add(String(lib_x + svc_w / 2, lib_y + 4, 'PostgreSQL',
                 fontSize=6, fillColor=BORDER, textAnchor='middle',
                 fontName='Helvetica'))

    # Arrow: Gateway -> Library API
    _draw_arrow(d, gw_x + 100, gw_y + 25, lib_x, lib_y + 30,
                color=SECONDARY, stroke_width=1.5)

    # --- Service A: Catalog Service (2 instances, bottom) ---
    cat1_x, cat1_y = 220, 95
    cat2_x, cat2_y = 220, 40

    for i, (bx, by) in enumerate([(cat1_x, cat1_y), (cat2_x, cat2_y)]):
        inst = i + 1
        d.add(Rect(bx, by, svc_w, 45, rx=6, ry=6,
                   fillColor=ACCENT, strokeColor=PRIMARY, strokeWidth=1.5))
        d.add(String(bx + svc_w / 2, by + 30, f'Catalog Service',
                     fontSize=9, fillColor=TEXT_COLOR, textAnchor='middle',
                     fontName='Helvetica-Bold'))
        d.add(String(bx + svc_w / 2, by + 18, f'Instance {inst} | :8082',
                     fontSize=7, fillColor=BORDER, textAnchor='middle',
                     fontName='Helvetica'))
        d.add(String(bx + svc_w / 2, by + 6, 'Reading Lists & Recommendations',
                     fontSize=6, fillColor=PRIMARY, textAnchor='middle',
                     fontName='Helvetica-Oblique'))

    # Bracket label for "Service A"
    d.add(String(210, 80, 'Service A',
                 fontSize=8, fillColor=PRIMARY, textAnchor='end',
                 fontName='Helvetica-Bold'))
    d.add(String(210, 68, '(2 replicas)',
                 fontSize=7, fillColor=BORDER, textAnchor='end',
                 fontName='Helvetica'))

    # Arrow: Gateway -> Catalog instances (lb:// routes to both)
    _draw_arrow(d, gw_x + 70, gw_y, lib_x + 20, cat1_y + 45,
                color=SECONDARY, stroke_width=1.2)
    _draw_arrow(d, gw_x + 50, gw_y, lib_x + 20, cat2_y + 45,
                color=SECONDARY, stroke_width=1.0, head_size=5)

    # Feign arrows: Catalog instances -> Library API
    _draw_arrow(d, cat1_x + svc_w / 2 + 20, cat1_y + 45, lib_x + svc_w / 2 + 20, lib_y,
                color=ORANGE, stroke_width=1.5)
    _draw_arrow(d, cat2_x + svc_w - 10, cat2_y + 45, lib_x + svc_w - 10, lib_y,
                color=ORANGE, stroke_width=1.0, head_size=5)
    feign_label_x = (cat1_x + svc_w / 2 + 20 + lib_x + svc_w / 2 + 20) / 2 + 15
    feign_label_y = (cat1_y + 45 + lib_y) / 2
    d.add(String(feign_label_x, feign_label_y + 5, 'Feign +',
                 fontSize=7, fillColor=ORANGE, textAnchor='middle',
                 fontName='Helvetica-Bold'))
    d.add(String(feign_label_x, feign_label_y - 5, 'Circuit Breaker',
                 fontSize=7, fillColor=ORANGE, textAnchor='middle',
                 fontName='Helvetica-Oblique'))

    # --- Shared Database (PostgreSQL) ---
    db_x, db_y = 390, 55
    # Cylinder shape for database
    d.add(Rect(db_x, db_y, 65, 40, rx=3, ry=3,
               fillColor=HexColor('#faf5ff'), strokeColor=HexColor('#805ad5'), strokeWidth=1.5))
    d.add(String(db_x + 32, db_y + 24, 'PostgreSQL',
                 fontSize=8, fillColor=TEXT_COLOR, textAnchor='middle',
                 fontName='Helvetica-Bold'))
    d.add(String(db_x + 32, db_y + 12, 'All Services',
                 fontSize=7, fillColor=HexColor('#805ad5'), textAnchor='middle',
                 fontName='Helvetica'))

    # Arrows: Both catalog instances -> DB
    _draw_arrow(d, cat1_x + svc_w, cat1_y + 15, db_x, db_y + 35,
                color=HexColor('#805ad5'), stroke_width=1.0, head_size=5)
    _draw_arrow(d, cat2_x + svc_w, cat2_y + 25, db_x, db_y + 20,
                color=HexColor('#805ad5'), stroke_width=1.0, head_size=5)
    # Arrow: Library API -> DB
    _draw_arrow(d, lib_x + svc_w, lib_y + 10, db_x + 10, db_y + 40,
                color=HexColor('#805ad5'), stroke_width=1.0, head_size=5)

    # --- Observability Stack ---
    obs_x = 385
    d.add(Rect(obs_x, infra_y - 52, 75, 92, rx=6, ry=6,
               fillColor=LIGHT_GRAY, strokeColor=BORDER, strokeWidth=1))
    d.add(String(obs_x + 37, infra_y + 30, 'Observability',
                 fontSize=7, fillColor=TEXT_COLOR, textAnchor='middle',
                 fontName='Helvetica-Bold'))
    d.add(String(obs_x + 37, infra_y + 14, 'Zipkin :9411',
                 fontSize=7, fillColor=BORDER, textAnchor='middle',
                 fontName='Helvetica'))
    d.add(String(obs_x + 37, infra_y + 2, 'Grafana :3000',
                 fontSize=7, fillColor=BORDER, textAnchor='middle',
                 fontName='Helvetica'))
    d.add(String(obs_x + 37, infra_y - 10, 'Loki :3100',
                 fontSize=7, fillColor=BORDER, textAnchor='middle',
                 fontName='Helvetica'))
    d.add(String(obs_x + 37, infra_y - 24, 'Traces + Logs',
                 fontSize=6, fillColor=SECONDARY, textAnchor='middle',
                 fontName='Helvetica-Oblique'))

    # --- Legend ---
    ly = 8
    d.add(Line(10, ly + 3, 30, ly + 3, strokeColor=SECONDARY, strokeWidth=1.5))
    d.add(String(33, ly, 'Gateway routing (lb://)',
                 fontSize=7, fillColor=TEXT_COLOR, textAnchor='start',
                 fontName='Helvetica'))
    d.add(Line(150, ly + 3, 170, ly + 3, strokeColor=ORANGE, strokeWidth=1.5))
    d.add(String(173, ly, 'Inter-service (Feign)',
                 fontSize=7, fillColor=TEXT_COLOR, textAnchor='start',
                 fontName='Helvetica'))
    d.add(Line(290, ly + 3, 310, ly + 3, strokeColor=HexColor('#805ad5'), strokeWidth=1))
    d.add(String(313, ly, 'Database connection',
                 fontSize=7, fillColor=TEXT_COLOR, textAnchor='start',
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


def create_request_flow():
    """Sequence-style diagram: Client -> Gateway -> Catalog -> Library API."""
    width = 470
    height = 280
    d = Drawing(width, height)

    d.add(String(width / 2, height - 10, 'Request Flow: Adding a Book to a Reading List',
                 fontSize=10, fillColor=DARK_BLUE, textAnchor='middle',
                 fontName='Helvetica-Bold'))

    cols = [60, 175, 295, 410]
    names = ['Client', 'API Gateway', 'Catalog Service', 'Library API']
    colors = [LIGHT_GRAY, HexColor('#e2e8f0'), ACCENT, ACCENT]
    strokes = [BORDER, DARK_BLUE, PRIMARY, PRIMARY]

    top_y = height - 35
    box_w, box_h = 90, 28

    for i, (cx, name, fill, stroke) in enumerate(zip(cols, names, colors, strokes)):
        d.add(Rect(cx - box_w / 2, top_y - box_h, box_w, box_h, rx=4, ry=4,
                   fillColor=fill, strokeColor=stroke, strokeWidth=1.5))
        d.add(String(cx, top_y - box_h / 2 - 2, name,
                     fontSize=8, fillColor=TEXT_COLOR, textAnchor='middle',
                     fontName='Helvetica-Bold'))
        d.add(Line(cx, top_y - box_h, cx, 15,
                   strokeColor=BORDER, strokeWidth=0.5, strokeDashArray=[4, 3]))

    y = top_y - box_h - 18
    step = 30

    messages = [
        (0, 1, 'POST /api/reading-lists/1/books', DARK_BLUE),
        (1, 2, 'Route via lb://catalog-service', SECONDARY),
        (2, 3, 'Feign: GET /api/books/1 (via Eureka)', ORANGE),
        (3, 2, 'BookDTO {title, author}', ORANGE),
        (2, 1, 'ReadingListDTO (enriched)', SECONDARY),
        (1, 0, '200 OK + book data from Service B', DARK_BLUE),
    ]

    labels_right = [
        'JWT validated',
        'Eureka resolves name',
        'Book verification',
        'Data enrichment',
        'Response assembled',
        'End-to-end complete',
    ]

    for i, ((src, dst, label, color), rlabel) in enumerate(zip(messages, labels_right)):
        my = y - i * step
        sx, dx = cols[src], cols[dst]
        _draw_arrow(d, sx, my, dx, my, color=color, stroke_width=1.2, head_size=5)
        mid = (sx + dx) / 2
        d.add(String(mid, my + 5, label,
                     fontSize=7, fillColor=color, textAnchor='middle',
                     fontName='Helvetica'))
        # Step number
        d.add(String(10, my - 3, str(i + 1),
                     fontSize=8, fillColor=PRIMARY, textAnchor='middle',
                     fontName='Helvetica-Bold'))
        # Right-side annotation
        d.add(String(462, my - 3, rlabel,
                     fontSize=6, fillColor=BORDER, textAnchor='end',
                     fontName='Helvetica-Oblique'))

    return d


def create_trace_timeline():
    """Zipkin-style trace timeline showing spans across 3 services."""
    width = 470
    height = 160
    d = Drawing(width, height)

    d.add(String(width / 2, height - 10, 'Distributed Trace: Happy Path (~25ms total)',
                 fontSize=10, fillColor=DARK_BLUE, textAnchor='middle',
                 fontName='Helvetica-Bold'))

    axis_y = 22
    axis_left = 140
    axis_right = 450
    d.add(Line(axis_left, axis_y, axis_right, axis_y,
               strokeColor=BORDER, strokeWidth=1))
    for t in [0, 5, 10, 15, 20, 25]:
        tx = axis_left + (t / 25) * (axis_right - axis_left)
        d.add(Line(tx, axis_y - 3, tx, axis_y + 3,
                   strokeColor=BORDER, strokeWidth=0.5))
        d.add(String(tx, axis_y - 12, f'{t}ms',
                     fontSize=6, fillColor=BORDER, textAnchor='middle',
                     fontName='Helvetica'))

    spans = [
        ('API Gateway', 0, 25, HexColor('#e2e8f0'), DARK_BLUE, 115),
        ('Catalog Service', 2, 23, ACCENT, PRIMARY, 80),
        ('Library API', 8, 16, HexColor('#feebc8'), ORANGE, 45),
    ]

    bar_h = 22
    for name, start_ms, end_ms, fill, stroke, row_y in spans:
        x1 = axis_left + (start_ms / 25) * (axis_right - axis_left)
        x2 = axis_left + (end_ms / 25) * (axis_right - axis_left)
        bw = x2 - x1

        d.add(String(axis_left - 8, row_y + bar_h / 2 - 3, name,
                     fontSize=8, fillColor=TEXT_COLOR, textAnchor='end',
                     fontName='Helvetica-Bold'))
        d.add(Rect(x1, row_y, bw, bar_h, rx=3, ry=3,
                   fillColor=fill, strokeColor=stroke, strokeWidth=1.2))
        duration = end_ms - start_ms
        d.add(String(x1 + bw / 2, row_y + bar_h / 2 - 3, f'{duration}ms',
                     fontSize=7, fillColor=TEXT_COLOR, textAnchor='middle',
                     fontName='Helvetica-Bold'))

    d.add(String(axis_left, height - 18,
                 'Trace ID: 69ca90f8...  (same ID propagated across all services via HTTP headers)',
                 fontSize=7, fillColor=BORDER, textAnchor='start',
                 fontName='Helvetica-Oblique'))

    return d
