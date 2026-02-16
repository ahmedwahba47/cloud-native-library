#!/usr/bin/env python3
"""
PDF Report Generator for Microservices Assignment
Library Management REST API
Student: Ahmed Wahba (A00336722)

Enhanced with: page numbers, numbered lists, subsection headings, table support.
"""

import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Preformatted
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from datetime import datetime
import os
import sys

# Add report directory to path for diagrams module
sys.path.insert(0, os.path.dirname(__file__))
# Add templates directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'templates'))
from report_content import REPORT_CONTENT
from diagrams import create_system_architecture, create_circuit_breaker_states


def create_styles():
    """Create custom paragraph styles."""
    styles = getSampleStyleSheet()

    # Title style
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#1a365d'),
        alignment=TA_CENTER
    ))

    # Subtitle style
    styles.add(ParagraphStyle(
        name='CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=20,
        textColor=HexColor('#4a5568'),
        alignment=TA_CENTER
    ))

    # Section heading style (H1)
    styles.add(ParagraphStyle(
        name='SectionHeading',
        parent=styles['Heading1'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=12,
        textColor=HexColor('#2c5282')
    ))

    # Subsection heading style (H2)
    styles.add(ParagraphStyle(
        name='SubsectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        spaceBefore=14,
        spaceAfter=8,
        textColor=HexColor('#2d3748')
    ))

    # Custom body text style
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    ))

    # Bullet point style
    styles.add(ParagraphStyle(
        name='BulletPoint',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        leftIndent=20,
        spaceAfter=4
    ))

    # Numbered list style
    styles.add(ParagraphStyle(
        name='NumberedItem',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        leftIndent=20,
        spaceAfter=4
    ))

    # Code block style
    styles.add(ParagraphStyle(
        name='CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        leading=11,
        leftIndent=20,
        rightIndent=20,
        spaceAfter=12,
        spaceBefore=8,
        backColor=HexColor('#f5f5f5')
    ))

    # Subheading style (for bold labels)
    styles.add(ParagraphStyle(
        name='SubHeading',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceBefore=10,
        spaceAfter=4,
        fontName='Helvetica-Bold'
    ))

    # Footer style for page numbers
    styles.add(ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor('#718096'),
        alignment=TA_CENTER
    ))

    # TOC entry style (clickable link)
    styles.add(ParagraphStyle(
        name='TOCEntry',
        parent=styles['Normal'],
        fontSize=11,
        leading=18,
        textColor=HexColor('#2c5282'),
        spaceAfter=4
    ))

    return styles


def add_page_number(canvas, doc):
    """Add page number to footer of each page."""
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(HexColor('#718096'))
    canvas.drawCentredString(A4[0] / 2, 0.5 * inch, text)
    canvas.restoreState()


def create_cover_page(styles):
    """Create the cover page elements."""
    elements = []

    # Add spacing at top
    elements.append(Spacer(1, 2*inch))

    # Title
    elements.append(Paragraph(REPORT_CONTENT['title'], styles['CustomTitle']))

    # Subtitle
    elements.append(Paragraph(REPORT_CONTENT['subtitle'], styles['CustomSubtitle']))

    elements.append(Spacer(1, 1*inch))

    # Student info table
    student_data = [
        ['Student Name:', REPORT_CONTENT['student']],
        ['Student ID:', REPORT_CONTENT['student_id']],
        ['Module:', REPORT_CONTENT['module']],
        ['Date:', datetime.now().strftime('%d %B %Y')]
    ]

    student_table = Table(student_data, colWidths=[2*inch, 3*inch])
    student_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))

    elements.append(student_table)
    elements.append(PageBreak())

    return elements


def convert_markdown_inline(text):
    """Convert inline markdown to ReportLab XML tags."""
    # Escape HTML special chars first (but not our tags)
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')

    # Convert **bold** to <b>bold</b>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)

    # Convert `code` to <font name="Courier">code</font>
    text = re.sub(r'`([^`]+)`', r'<font name="Courier" size="9">\1</font>', text)

    # Convert @Annotation to code style
    text = re.sub(r'(@\w+)', r'<font name="Courier" size="9">\1</font>', text)

    return text


def process_content(content, styles):
    """Process content text and convert to flowables."""
    elements = []
    lines = content.strip().split('\n')

    in_code_block = False
    code_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check for code block markers
        if stripped.startswith('```'):
            if in_code_block:
                # End code block
                if code_lines:
                    code_text = '\n'.join(code_lines)
                    elements.append(Preformatted(code_text, styles['CodeBlock']))
                code_lines = []
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
            i += 1
            continue

        # Detect JSON blocks (lines starting with {)
        if stripped.startswith('{') and not in_code_block:
            json_lines = []
            while i < len(lines) and (lines[i].strip().startswith('{') or
                                       lines[i].strip().startswith('}') or
                                       lines[i].strip().startswith('"') or
                                       lines[i].strip().startswith('[') or
                                       lines[i].strip().startswith(']') or
                                       lines[i].strip() == '' or
                                       ':' in lines[i]):
                if lines[i].strip() == '' and json_lines and json_lines[-1].strip().endswith('}'):
                    break
                json_lines.append(lines[i])
                i += 1
                if lines[i-1].strip() == '}' and i < len(lines) and not lines[i].strip().startswith('"'):
                    break
            if json_lines:
                code_text = '\n'.join(json_lines)
                elements.append(Preformatted(code_text, styles['CodeBlock']))
            continue

        # Detect flow diagrams with arrows
        if '->' in stripped and not in_code_block and ('Layer' in stripped or '[' in stripped):
            elements.append(Preformatted(stripped, styles['CodeBlock']))
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Skip empty lines
        if not stripped:
            i += 1
            continue

        # Handle numbered lists (1. 2. 3. etc.)
        numbered_match = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if numbered_match:
            num = numbered_match.group(1)
            text = convert_markdown_inline(numbered_match.group(2))
            elements.append(Paragraph(f'{num}. {text}', styles['NumberedItem']))
            i += 1
            continue

        # Handle bullet points
        if stripped.startswith('- '):
            bullet_text = convert_markdown_inline(stripped[2:])
            elements.append(Paragraph(f'&bull; {bullet_text}', styles['BulletPoint']))
            i += 1
            continue

        # Handle lines that start with bold (subheadings)
        if stripped.startswith('**') and ':**' in stripped:
            # This is a label like **Domain:** value
            match = re.match(r'\*\*([^*]+):\*\*\s*(.*)', stripped)
            if match:
                label = match.group(1)
                value = match.group(2)
                if value:
                    text = f'<b>{label}:</b> {convert_markdown_inline(value)}'
                    elements.append(Paragraph(text, styles['CustomBody']))
                else:
                    elements.append(Paragraph(f'<b>{label}:</b>', styles['SubHeading']))
                i += 1
                continue

        # Handle standalone bold lines (like Challenge titles)
        if stripped.startswith('**') and stripped.endswith('**'):
            text = stripped[2:-2]
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph(f'<b>{text}</b>', styles['SubHeading']))
            i += 1
            continue

        # Regular paragraph - convert inline markdown
        text = convert_markdown_inline(stripped)
        elements.append(Paragraph(text, styles['CustomBody']))
        i += 1

    return elements


def create_section(section, styles, section_idx=0):
    """Create a section with heading and content."""
    elements = []

    # Section heading with bookmark anchor
    anchor = f'<a name="section{section_idx}"/>'
    elements.append(Paragraph(f'{anchor}{section["title"]}', styles['SectionHeading']))

    # Insert diagrams for specific sections
    if 'Architecture Overview' in section['title']:
        elements.append(Spacer(1, 0.1*inch))
        elements.append(create_system_architecture())
        elements.append(Spacer(1, 0.1*inch))

    if 'Resilience' in section['title']:
        elements.append(Spacer(1, 0.1*inch))
        elements.append(create_circuit_breaker_states())
        elements.append(Spacer(1, 0.1*inch))

    # Process content
    content_elements = process_content(section['content'], styles)
    elements.extend(content_elements)

    elements.append(Spacer(1, 0.3*inch))

    return elements


def generate_report():
    """Generate the complete PDF report."""
    output_path = os.path.join(os.path.dirname(__file__), 'Cloud-Native-System-Report-Ahmed-Wahba-A00336722.pdf')

    # Create document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = create_styles()
    elements = []

    # Cover page
    elements.extend(create_cover_page(styles))

    # Table of contents header
    elements.append(Paragraph('Table of Contents', styles['SectionHeading']))
    elements.append(Spacer(1, 0.2*inch))

    # TOC entries (clickable links)
    for i, section in enumerate(REPORT_CONTENT['sections']):
        link = f'<a href="#section{i}" color="#2c5282">{section["title"]}</a>'
        elements.append(Paragraph(link, styles['TOCEntry']))

    elements.append(PageBreak())

    # Content sections
    for i, section in enumerate(REPORT_CONTENT['sections']):
        elements.extend(create_section(section, styles, section_idx=i))

    # Build PDF with page numbers
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f'Report generated: {output_path}')


if __name__ == '__main__':
    generate_report()
