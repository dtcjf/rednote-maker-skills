---
name: rednote-maker
description: Generate RedNote (Xiaohongshu) style cover and image posts. Triggered when user requests generating RedNote images, covers, or image templates. Supports both Text-to-Image mode and HTML Mode.
version: 1.3.0
author: by
tags:
  - xiaohongshu
  - image-generator
  - template
  - html-mode
metadata:
  requires:
    pypi: [playwright]
    bins: [webkit]
---

# RedNote Image Generator

Generate RedNote style cover and image posts. Supports two modes:

1. **Text-to-Image Mode (文图模式)**: Generate images from text content using predefined templates
2. **HTML Mode (HTML模式)**: Generate images from custom HTML files

## Two Operation Modes

### Mode 1: Text-to-Image Mode (Default)

In this mode, you provide text content and the system uses templates to generate images.

```bash
# Basic usage
python rednote-maker/scripts/make_image.py -t rednote-maker/assets/templates/rednote_style1.html -T "Title" -d "Content"

# With all options
python rednote-maker/scripts/make_image.py \
  -t rednote-maker/assets/templates/rednote_style1.html \
  -T "Title" \
  -d "Content" \
  -C "topic1,topic2" \
  -o output.png
```

### Mode 2: HTML Mode (HTML模式)

In this mode, you provide a complete HTML file and the system renders it directly to an image without any template processing.

**Use `--html-mode` flag to enable HTML Mode:**

```bash
# Basic HTML mode usage
python rednote-maker/scripts/make_image.py --html-mode -t my_page.html -o output.png

# With custom viewport size (optional)
python rednote-maker/scripts/make_image.py \
  --html-mode \
  -t my_page.html \
  -o output.png
```

**Key differences in HTML Mode:**

| Feature | Text-to-Image Mode | HTML Mode |
|---------|-------------------|-----------|
| Template processing | Yes | No (direct render) |
| Variable substitution | Yes | No |
| Title parameter (`-T`) | Required | Not used |
| Content parameter (`-d`) | Optional | Not used |
| Multi-page support | Yes | No |
| Viewport detection | Fixed | Auto-detect from HTML |

**When to use HTML Mode:**

- You have a complete HTML design and want to convert it to an image
- You need full control over the HTML/CSS layout
- You're converting web pages or custom designs to images
- You want to bypass template processing and render HTML as-is

**HTML Structure Requirements for HTML Mode:**

The HTML file should be a complete, valid HTML document. The system will:

1. Read the HTML file
2. Auto-detect viewport size from CSS (looking for `#container` width/height)
3. Render the HTML to an image
4. Save the output

**Recommended HTML structure:**

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        #container {
            width: 1242px;    /* Will be auto-detected */
            height: 1660px;   /* Will be auto-detected */
            /* ... */
        }
    </style>
</head>
<body>
    <div id="container">
        <!-- Your content here -->
    </div>
</body>
</html>
```

If no `#container` size is found, the system defaults to **1242×1660** (RedNote recommended size).

## Trigger Conditions

Triggered when user requests:
- Generate RedNote image
- Generate RedNote cover
- Generate RedNote post
- Generate image from template
- Create RedNote style image
- Render HTML to image
- Convert HTML to image
- HTML mode for image generation

## Two Operation Modes

This skill supports **two modes** of operation:

### Mode 1: Text-to-Image Mode (文图模式) - Default

User provides text content, and the system uses templates to generate images.

**Command format:**
```bash
python rednote-maker/scripts/make_image.py -t TEMPLATE -T "Title" -d "Content" -o output.png
```

### Mode 2: HTML Mode (HTML模式)

User provides a complete HTML file, and the system directly renders it to an image without template processing.

**Command format:**
```bash
python rednote-maker/scripts/make_image.py --html-mode -t my_page.html -o output.png
```

**Key difference:** In HTML mode, the HTML file is rendered as-is without any variable substitution or template processing.

## Install Dependencies

```bash
pip install playwright
playwright install webkit
```

## Basic Usage

### Mode 1: Text-to-Image Mode (Default)

In this mode, the system uses predefined templates and substitutes variables to generate images.

#### Generate Image Posts

```bash
# Generate single page image from template
python rednote-maker/scripts/make_image.py -t rednote-maker/assets/templates/rednote_style1.html -T "Title" -d "Content"

# Generate multi-page image for long content
python rednote-maker/scripts/make_image.py -t rednote-maker/assets/templates/rednote_style1.html -T "Title" -d "Long content..." -m

# Specify output filename
python rednote-maker/scripts/make_image.py -t rednote-maker/assets/templates/rednote_style3.html -T "Title" -d "Content" -o my_image.png
```

#### Generate Cover Images

```bash
# Generate cover using cover template
python rednote-maker/scripts/make_image.py \
  -t rednote-maker/assets/templates/cover_style1.html \
  -T "Graduate School Interview Guide" \
  -s "24考研必看！帮你快速Get复试技巧" \
  -C "考研,复试,研究生" \
  -o cover.png
```

### Mode 2: HTML Mode (HTML模式)

In this mode, the system directly renders a complete HTML file to an image without any template processing. This gives you full control over the HTML/CSS.

#### Basic Usage

```bash
# Basic HTML mode - render HTML file to image
python rednote-maker/scripts/make_image.py --html-mode -t my_design.html -o output.png

# With specific output path
python rednote-maker/scripts/make_image.py \
  --html-mode \
  -t /path/to/my_page.html \
  -o /path/to/output.png
```

#### How HTML Mode Works

1. Reads the complete HTML file
2. Auto-detects viewport size from CSS (looking for `#container` width/height)
3. Renders the HTML directly to an image
4. Saves the output image

**Key differences:**

| Feature | Text-to-Image Mode | HTML Mode |
|---------|-------------------|-----------|
| Template processing | Yes | No (direct render) |
| Variable substitution | Yes | No |
| Title (`-T`) | Required | Not used |
| Content (`-d`) | Optional | Not used |
| Multi-page support | Yes | No |
| Viewport detection | Fixed | Auto-detect from HTML |

#### HTML Structure Requirements

Your HTML file should be a complete, valid HTML document. The system will auto-detect the viewport size from the `#container` CSS.

**Recommended structure:**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Design</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
            background: #FAFAFA;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        #container {
            /* This size will be auto-detected */
            width: 1242px;
            height: 1660px;
            background: #FFFFFF;
            /* ... */
        }
    </style>
</head>
<body>
    <div id="container">
        <!-- Your content here -->
    </div>
</body>
</html>
```

**Auto-detection:**

If no `#container` size is found, the system defaults to **1242×1660** (RedNote recommended size).

#### When to Use HTML Mode

- You have a complete HTML design and want to convert it to an image
- You need full control over the HTML/CSS layout
- You're converting web pages or custom designs to images
- You want to bypass template processing and render HTML as-is

## Parameters

| Parameter | Short | Description | Text Mode | HTML Mode |
|-----------|-------|-------------|-----------|-----------|
| `--template` | `-t` | HTML template file path (required) | Yes | Yes (HTML file path) |
| `--title` | `-T` | Title (required in text mode) | Required | Not used |
| `--desc` | `-d` | Body content | Optional | Not used |
| `--output` | `-o` | Output path | Yes | Yes |
| `--multi-page` | `-m` | Auto pagination | Yes | No |
| `--topics` | `-C` | Topic list | Optional | Not used |
| `--subtitle` | `-s` | Subtitle | Cover only | Not used |
| `--html-mode` | - | Enable HTML Mode | No | **Yes (required)** |

## HTML Mode (HTML模式) Detailed Guide

### What is HTML Mode?

HTML Mode allows you to convert a complete HTML file directly to an image without any template processing. The HTML is rendered as-is in a headless browser and captured as an image.

### When to Use HTML Mode

- **Custom designs**: You have a complete HTML/CSS design and want to convert it to an image
- **Web page capture**: You want to convert web pages or web-based designs to images
- **Full control**: You need complete control over the HTML structure and styling
- **Bypass templates**: You don't want variable substitution or template processing

### HTML Mode Usage

```bash
# Basic usage
python rednote-maker/scripts/make_image.py --html-mode -t my_page.html -o output.png

# With paths
python rednote-maker/scripts/make_image.py \
  --html-mode \
  -t /path/to/design.html \
  -o /path/to/output.png
```

### HTML Structure for HTML Mode

Your HTML file should be a complete, valid HTML document. The system will:

1. Read the HTML file
2. Auto-detect viewport size from CSS (looking for `#container` width/height)
3. Render the HTML in a headless browser
4. Capture the screenshot and save as image

**Recommended HTML structure:**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Design</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
            background: #FAFAFA;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        #container {
            /* This size will be auto-detected */
            width: 1242px;
            height: 1660px;
            background: #FFFFFF;
            padding: 60px;
            /* ... */
        }
    </style>
</head>
<body>
    <div id="container">
        <!-- Your custom content here -->
        <h1>My Title</h1>
        <p>My content...</p>
    </div>
</body>
</html>
```

### Viewport Size Auto-Detection

In HTML Mode, the system automatically detects the viewport size from your CSS:

1. **Primary detection**: Looks for `#container { width: XXXpx; height: XXXpx; }`
2. **Fallback**: If no container size found, defaults to **1242×1660** (RedNote recommended)

You can also specify a custom viewport by adding a comment in your HTML:
```html
<!-- viewport: 1080x1920 -->
```

### HTML Mode vs Text-to-Image Mode Comparison

| Feature | Text-to-Image Mode | HTML Mode |
|---------|-------------------|-----------|
| **Input** | Text content + template | Complete HTML file |
| **Template processing** | Yes (variable substitution) | No (direct render) |
| **Title parameter** | Required | Not used |
| **Content parameter** | Optional | Not used |
| **Multi-page** | Supported | Not supported |
| **Viewport size** | Fixed (1242×1660) | Auto-detect from HTML |
| **Use case** | Quick content generation | Custom designs, web capture |

### Examples

**Text-to-Image Mode:**
```bash
# Quick post generation
python rednote-maker/scripts/make_image.py \
  -t rednote-maker/assets/templates/rednote_style1.html \
  -T "今日分享" \
  -d "今天学习了很多新知识..." \
  -o post.png
```

**HTML Mode:**
```bash
# Custom design conversion
python rednote-maker/scripts/make_image.py \
  --html-mode \
  -t my_custom_design.html \
  -o custom_output.png
```

## Available Templates

Templates are in `rednote-maker/assets/templates/` directory:

**Image Templates:**

| Template | Style |
|----------|-------|
| `rednote_style1.html` | Black White Minimal |
| `rednote_style2.html` | Vintage Paper |
| `rednote_style3.html` | Candy Gradient |
| `rednote_style4.html` | Purple Starry Sky |
| `rednote_style5.html` | Caramel Cookie |
| `rednote_style6.html` | Retro Chinese |

**Cover Templates (one-to-one with image templates):**

| Template | Style |
|----------|-------|
| `cover_style1.html` | Black White Minimal |
| `cover_style2.html` | Vintage Paper |
| `cover_style3.html` | Candy Gradient |
| `cover_style4.html` | Purple Starry Sky |
| `cover_style5.html` | Caramel Cookie |
| `cover_style6.html` | Retro Chinese |

## Template Style Examples

```bash
# Black White Minimal
python rednote-maker/scripts/make_image.py -t rednote_style1.html -T "Title" -d "Content" -o out.png

# Vintage Paper
python rednote-maker/scripts/make_image.py -t rednote_style2.html -T "Title" -d "Content" -o out.png

# Candy Gradient
python rednote-maker/scripts/make_image.py -t rednote_style3.html -T "Title" -d "Content" -o out.png

# Purple Starry Sky
python rednote-maker/scripts/make_image.py -t rednote_style4.html -T "Title" -d "Content" -o out.png

# Caramel Cookie
python rednote-maker/scripts/make_image.py -t rednote_style5.html -T "Title" -d "Content" -o out.png

# Retro Chinese
python rednote-maker/scripts/make_image.py -t rednote_style6.html -T "Title" -d "Content" -o out.png

# Cover styles
python rednote-maker/scripts/make_image.py -t cover_style1.html -T "Title" -s "Subtitle" -C "topic1,topic2" -o cover.png
python rednote-maker/scripts/make_image.py -t cover_style2.html -T "Title" -s "Subtitle" -C "topic1,topic2" -o cover.png
python rednote-maker/scripts/make_image.py -t cover_style3.html -T "Title" -s "Subtitle" -C "topic1,topic2" -o cover.png
python rednote-maker/scripts/make_image.py -t cover_style4.html -T "Title" -s "Subtitle" -C "topic1,topic2" -o cover.png
python rednote-maker/scripts/make_image.py -t cover_style5.html -T "Title" -s "Subtitle" -C "topic1,topic2" -o cover.png
python rednote-maker/scripts/make_image.py -t cover_style6.html -T "Title" -s "Subtitle" -C "topic1,topic2" -o cover.png
```

## Custom Templates

Users can create their own HTML templates with these key elements:

**Image Templates:**

```html
<!-- Title -->
<h1 class="title">Title Content</h1>

<!-- Content (supports multiple paragraphs) -->
<div class="content">
    <p>First paragraph</p>
    <p>Second paragraph</p>
</div>

<!-- Page number (auto hidden when not multi-page) -->
<span class="page-num">1/3</span>
```

**Cover Templates:**

```html
<!-- Cover Title -->
<h1 class="cover-title">Cover Title</h1>

<!-- Cover Subtitle -->
<p class="cover-subtitle">Subtitle Content</p>

<!-- Cover Tags -->
<div class="cover-tags">
    <span class="cover-tag">#topic1</span>
    <span class="cover-tag">#topic2</span>
</div>
```

## HTML Template Enhancement

Enhance text presentation in custom templates:

### Text Color
```html
<!-- Red emphasis -->
<span style="color: #FF2442;">Key content</span>

<!-- Cyan tech style -->
<span style="color: #00FFFF;">Key content</span>

<!-- Gold tips -->
<span style="color: #FFD700;">Tips</span>
```

### Text Size
```html
<!-- Large title -->
<span style="font-size: 48px;">Large Title</span>

<!-- Small auxiliary -->
<span style="font-size: 24px;">Auxiliary text</span>
```

### Text Style
```html
<!-- Bold -->
<strong>Bold text</strong>

<!-- Italic -->
<em>Italic text</em>

<!-- Underline -->
<span style="text-decoration: underline;">Underline</span>
```

### Background Highlight
```html
<!-- Red highlight background -->
<span style="background: #FFE5E5; padding: 2px 8px; border-radius: 4px;">Highlighted</span>

<!-- Gradient background -->
<span style="background: linear-gradient(135deg, #FF6B6B, #FF2442); color: white; padding: 4px 12px; border-radius: 8px;">Gradient Button</span>
```

### Built-in Style Classes (for default templates)

Some templates support these CSS classes:

| Class | Effect |
|-------|--------|
| `.highlight` | Red highlight |
| `.tip` | Orange tip |
| `.note` | Cyan note |
| `.code-block` | Code block (tech style) |

### Important: Mark All Key Points

**When generating content, AI should identify and mark ALL key points that need emphasis, not just one!**

Example:
```html
<!-- Correct: mark all key points -->
<p>Here is <span class="highlight">key point 1</span> to note, also <span class="highlight">key point 2</span> is important</p>
<p>This is <span class="tip">tip 1</span> and <span class="tip">tip 2</span></p>

<!-- Wrong: only mark one -->
<p>Here is <span class="highlight">key point</span> to note</p>
```

**Criteria for identifying key points:**
- Key data/numbers: e.g. "5 tips", "3 steps"
- Core knowledge/methods
- Easy to miss details
- Summary statements
- Action guidance/suggestions

## Notes

- Supports jpg, png, jpeg formats
- Topics are auto-formatted, no need to add # manually
- Recommended cover image size: 1080x1080 or 1080x1350
- Cover and image templates are one-to-one, choose based on content
- Long content auto-paginated, max 12-14 lines per page
