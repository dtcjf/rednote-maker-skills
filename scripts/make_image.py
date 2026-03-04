#!/usr/bin/env python3
"""
Generate RedNote (Xiaohongshu) style images.

Generate images from HTML templates with content support, multi-page.
Use playwright for screenshot.

Usage:
  # Generate single page image from template
  python make_image.py -t template.html -T "Title" -d "Content"

  # Generate multi-page image for long content
  python make_image.py -t template.html -T "Title" -d "Long content..." -m
"""

import argparse
import math
import os
import sys
import asyncio
import re
from pathlib import Path

# CSS class names used in HTML templates
TEMPLATE_CLASS_TITLE = "title"
TEMPLATE_CLASS_CONTENT = "content"
TEMPLATE_CLASS_TAGS = "tags"
TEMPLATE_CLASS_PAGE_NUM = "page-num"

def read_template(template_file: str) -> str:
    """Read template file."""
    with open(template_file, 'r', encoding='utf-8') as f:
        return f.read()


def normalize_content(content: str) -> str:
    """Convert HTML tags (like <br>) to plain text newlines."""
    content = re.sub(r'<br\s*/?\s*>', '\n', content, flags=re.IGNORECASE)
    return content


def calculate_pages(content: str, content_size: int = 32, width: int = 1080, height: int = 1440) -> int:
    """Calculate required pages.

    Rules:
    - Container width 980px, max 37 chars per line
    - First page: max 12 lines
    - Subsequent pages: max 14 lines
    - Lines over 37 chars: actual lines = ceil(chars / 37)
    """
    content = normalize_content(content)

    if not content.strip():
        return 1

    # Constants
    CHARS_PER_LINE = 37  # Max chars per line
    FIRST_PAGE_LINES = 12  # Max lines for first page
    OTHER_PAGE_LINES = 14  # Max lines for other pages

    # Split by newline
    raw_lines = content.split('\n')

    # Calculate total lines
    total_lines = 0
    for line in raw_lines:
        line = line.strip()
        if not line:
            continue

        line_len = len(line)
        # Lines over limit, calculate actual lines
        if line_len > CHARS_PER_LINE:
            total_lines += math.ceil(line_len / CHARS_PER_LINE)
        else:
            total_lines += 1

    # Calculate required pages
    if total_lines <= FIRST_PAGE_LINES:
        return 1

    remaining_lines = total_lines - FIRST_PAGE_LINES
    additional_pages = int(math.ceil(remaining_lines / OTHER_PAGE_LINES))

    return 1 + additional_pages


def split_content(content: str, num_pages: int) -> list:
    """Split content into multiple pages, keeping paragraphs intact.

    Rules:
    - First page: max 12 lines
    - Subsequent pages: max 14 lines
    - Lines over 37 chars split into multiple lines
    """
    content = normalize_content(content)

    # Constants
    CHARS_PER_LINE = 37
    FIRST_PAGE_LINES = 12
    OTHER_PAGE_LINES = 14

    # Split by newline into lines
    raw_lines = content.split('\n')
    lines = [line.strip() for line in raw_lines if line.strip()]

    if not lines:
        return [content]

    # Split long lines into multiple lines (by 37 chars)
    expanded_lines = []
    for line in lines:
        line_len = len(line)
        if line_len > CHARS_PER_LINE:
            # Split into multiple lines
            for i in range(0, line_len, CHARS_PER_LINE):
                expanded_lines.append(line[i:i+CHARS_PER_LINE])
        else:
            expanded_lines.append(line)

    # Now expanded_lines is split by actual lines
    total_lines = len(expanded_lines)

    # If total lines less than num_pages, reduce pages
    if total_lines < num_pages:
        num_pages = total_lines
        if num_pages == 1:
            return ['\n'.join(expanded_lines)]

    # Calculate page capacities
    page_capacities = []
    remaining = total_lines
    for i in range(num_pages):
        if i == 0:
            capacity = min(FIRST_PAGE_LINES, remaining)
        else:
            capacity = min(OTHER_PAGE_LINES, remaining)
        page_capacities.append(capacity)
        remaining -= capacity

    # Distribute lines to pages
    pages = []
    current_page_lines = []
    page_idx = 0

    for line in expanded_lines:
        # Check if need to split page
        if len(current_page_lines) >= page_capacities[page_idx] and page_idx < num_pages - 1:
            pages.append('\n'.join(current_page_lines))
            current_page_lines = []
            page_idx += 1

        current_page_lines.append(line)

    # Add last page
    if current_page_lines:
        pages.append('\n'.join(current_page_lines))

    return pages[:num_pages]


def generate_page_html(template: str, title: str, content: str = "", page: int = 1, total_pages: int = 1, topics: list = None, subtitle: str = "") -> str:
    """Generate single page HTML from template.

    Args:
        template: HTML template content
        title: Main title
        content: Body content (for image note)
        page: Current page number
        total_pages: Total pages
        topics: Topic tag list
        subtitle: Subtitle (for cover)
    """
    html = template

    # Check if it's a cover template
    is_cover = 'cover-title' in template or 'class="cover-' in template

    if is_cover:
        # Cover template handling
        if title:
            # Replace cover title
            html = re.sub(r'<h1[^>]*class="[^"]*title[^"]*"[^>]*>.*?</h1>', f'<h1 class="cover-title">{title}</h1>', html, flags=re.DOTALL)
        if subtitle:
            # Replace subtitle
            html = re.sub(r'<p[^>]*class="[^"]*subtitle[^"]*"[^>]*>.*?</p>', f'<p class="cover-subtitle">{subtitle}</p>', html, flags=re.DOTALL)
    else:
        # Replace title (only show on first page)
        if title:
            html = re.sub(r'<h1[^>]*class="title"[^>]*>.*?</h1>', f'<h1 class="title">{title}</h1>', html, flags=re.DOTALL)
            # Hide subtitle (not first page)
            if page > 1:
                html = re.sub(r'<div[^>]*class="subtitle"[^>]*>.*?</div>', '', html, flags=re.DOTALL)
        else:
            # Not first page, hide title, divider and subtitle
            html = re.sub(r'<h1[^>]*class="title"[^>]*>.*?</h1>', '', html, flags=re.DOTALL)
            html = re.sub(r'<div[^>]*class="divider"[^>]*>.*?</div>', '', html, flags=re.DOTALL)
            html = re.sub(r'<div[^>]*class="subtitle"[^>]*>.*?</div>', '', html, flags=re.DOTALL)

    # Replace content (not cover template)
    if not is_cover:
        # Clean <br> tags, unify with \n
        content = re.sub(r'<br\s*/?\s*>', '\n', content, flags=re.IGNORECASE)
        content = content.strip()

        if '\n' in content:
            paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
            # Replace newlines with <br>
            content_html = '<div class="content">' + '<br>'.join(paragraphs) + '</div>'
        else:
            content_html = f'<div class="content">{content}</div>'

        content_pattern = r'<div[^>]*class="content"[^>]*>.*?</div>'
        html = re.sub(content_pattern, content_html, html, flags=re.DOTALL)

    # Handle topic tags (only show on first page)
    if topics and len(topics) > 0 and page == 1:
        # Ensure each topic has # symbol
        formatted_topics = []
        for t in topics:
            t = t.strip()
            if t.startswith('#') and t.endswith('#'):
                formatted_topics.append(t)
            else:
                formatted_topics.append(f"#{t}#")
        tags_html = '<div class="tags">' + ''.join([f'<span class="tag">{t}</span>' for t in formatted_topics]) + '</div>'
        html = re.sub(r'<div[^>]*class="tags"[^>]*>.*?</div>', tags_html, html, flags=re.DOTALL)
    else:
        # Hide topics
        html = re.sub(r'<div[^>]*class="tags"[^>]*>.*?</div>', '', html, flags=re.DOTALL)

    # Handle topic tags (cover template)
    if is_cover and topics and len(topics) > 0:
        formatted_topics = []
        for t in topics:
            t = t.strip()
            if t.startswith('#') and t.endswith('#'):
                formatted_topics.append(t)
            else:
                formatted_topics.append(f"#{t}#")
        tags_html = '<div class="cover-tags">' + ''.join([f'<span class="cover-tag">{t}</span>' for t in formatted_topics]) + '</div>'
        html = re.sub(r'<div[^>]*class="cover-tags"[^>]*>.*?</div>', tags_html, html, flags=re.DOTALL)

    # Handle page number
    if total_pages > 1:
        html = re.sub(r'<span[^>]*class="page-num"[^>]*>.*?</span>', f'<span class="page-num">{page}/{total_pages}</span>', html, flags=re.DOTALL)
    else:
        html = re.sub(r'<span[^>]*class="page-num"[^>]*>.*?</span>', '', html, flags=re.DOTALL)

    return html


async def screenshot_from_html_string(output_path: str, html_content: str, save_html: bool = True):
    """Screenshot from HTML content."""
    from playwright.async_api import async_playwright

    # Save HTML for debugging
    if save_html:
        html_path = output_path.replace('.png', '.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"  HTML saved: {html_path}")

    async with async_playwright() as p:
        try:
            browser = await p.webkit.launch()
        except:
            try:
                browser = await p.chromium.launch()
            except Exception as e:
                raise RuntimeError(f"Failed to launch browser: {e}")

        page = await browser.new_page(
            viewport={'width': 1080, 'height': 1440},
            device_scale_factor=2
        )

        # Set HTML content
        await page.set_content(html_content, wait_until='domcontentloaded')
        await page.wait_for_timeout(500)

        # Check if content overflows container
        container_info = await page.evaluate('''() => {
            const container = document.getElementById('container');
            if (!container) return { overflow: false, scrollHeight: 0, clientHeight: 0 };
            const style = window.getComputedStyle(container);
            return {
                overflow: style.overflow,
                scrollHeight: container.scrollHeight,
                clientHeight: container.clientHeight
            };
        }''')

        is_overflow = container_info['scrollHeight'] > container_info['clientHeight']

        if is_overflow:
            print(f"  Content overflow ({container_info['scrollHeight']} > {container_info['clientHeight']}), auto adjusting container height")

            # Dynamically adjust container height to fit content
            await page.evaluate(f'''() => {{
                const container = document.getElementById('container');
                if (container) {{
                    container.style.height = '{container_info['scrollHeight']}px';
                    container.style.overflow = 'visible';
                }}
            }}''')

            # Wait for styles to apply
            await page.wait_for_timeout(200)

            # Use visible area screenshot
            await page.screenshot(path=output_path, full_page=False)
        else:
            await page.screenshot(path=output_path, full_page=False)

        await browser.close()

    return output_path


async def create_images_from_template(
    template_file: str,
    title: str,
    content: str = "",
    output_dir: str = ".",
    prefix: str = "rednote",
    multi_page: bool = False,
    topics: list = None,
    subtitle: str = ""
) -> list:
    """Generate images from template.

    Args:
        template_file: Template file path
        title: Title
        content: Body content (for image note)
        output_dir: Output directory
        prefix: Output file prefix
        multi_page: Enable multi-page
        topics: Topic list, e.g. ["#coding#", "#learning#"]
        subtitle: Subtitle (for cover)

    Returns:
        List of generated image paths
    """
    # Read template
    template = read_template(template_file)

    # Check if it's a cover template
    is_cover = 'cover-title' in template or 'class="cover-' in template

    os.makedirs(output_dir, exist_ok=True)

    # Cover only generates 1 page
    if is_cover:
        total_pages = 1
    elif multi_page:
        total_pages = calculate_pages(content)
    else:
        total_pages = 1

    # Split content (always call to clean <br>)
    pages_content = split_content(content, total_pages) if content else [""]

    print(f"Content length: {len(content)} chars")
    print(f"Split into {len(pages_content)} pages")

    # Smart hint for long content
    if not multi_page and len(content) > 350:
        print(f"Hint: Content is long ({len(content)} chars), recommend adding -m for auto pagination")

    output_paths = []

    for i, page_content in enumerate(pages_content):
        output_file = os.path.join(output_dir, f"{prefix}_{i+1}.png")

        print(f"  Generating page {i+1}/{len(pages_content)}...")

        # Generate single page HTML
        page_html = generate_page_html(
            template=template,
            title=title if i == 0 else "",  # Only show title on first page
            content=page_content,
            page=i + 1,
            total_pages=len(pages_content),
            topics=topics,
            subtitle=subtitle
        )

        # Screenshot
        await screenshot_from_html_string(output_file, page_html)

        output_paths.append(output_file)

    return output_paths


async def main_async():
    parser = argparse.ArgumentParser(description="Generate RedNote style images/covers from templates")
    parser.add_argument("-t", "--template", required=True, help="HTML template file path")
    parser.add_argument("-T", "--title", required=True, help="Title (for cover/image)")
    parser.add_argument("-d", "--desc", default="", help="Body content (for image note, optional for cover)")
    parser.add_argument("-o", "--output", default="rednote_image.png", help="Output path")
    parser.add_argument("-m", "--multi-page", action="store_true", help="Auto pagination for long content")
    parser.add_argument("-C", "--topics", help="Topic list, comma separated, e.g. coding,learning")
    parser.add_argument("-s", "--subtitle", default="", help="Subtitle (for cover only)")

    args = parser.parse_args()

    # Parse topics (format: topic1,topic2 or #topic1#,#topic2#)
    topics = None
    if args.topics:
        raw_topics = [t.strip() for t in args.topics.split(',')]
        topics = []
        for t in raw_topics:
            if t.startswith('#') and t.endswith('#'):
                topics.append(t)
            else:
                topics.append(f"#{t}#")

    # Determine output directory and prefix
    if os.path.isdir(args.output):
        output_dir = args.output
        prefix = "rednote"
    else:
        output_dir = os.path.dirname(args.output) or "."
        prefix = os.path.splitext(os.path.basename(args.output))[0]

    print("Generating RedNote style images...\n")

    try:
        paths = await create_images_from_template(
            template_file=args.template,
            title=args.title,
            content=args.desc,
            output_dir=output_dir,
            prefix=prefix,
            multi_page=args.multi_page,
            topics=topics,
            subtitle=args.subtitle
        )

        print(f"\nDone! Generated {len(paths)} images:")
        for p in paths:
            print(f"   {p}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
