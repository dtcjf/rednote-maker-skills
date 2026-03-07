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

Generate RedNote (Xiaohongshu) style cover and image posts.

## Install Dependencies

```bash
pip install playwright
playwright install webkit
```

## Two Operation Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **Text-to-Image** (Default) | Provide text content, system uses templates | Quick content generation |
| **HTML Mode** | Provide complete HTML file, direct render | Custom designs, full control |

### Quick Comparison

| Feature | Text-to-Image Mode | HTML Mode |
|---------|-------------------|-----------|
| Template processing | Yes (variable substitution) | No (direct render) |
| Title (`-T`) | Required | Not used |
| Content (`-d`) | Optional | Not used |
| Multi-page | Supported | Not supported |
| Viewport size | Fixed (1242×1660) | Auto-detect from HTML |
| Flag | None | `--html-mode` |

---

## Mode 1: Text-to-Image Mode (文图模式)

Provide text content, and the system uses templates to generate images.

### Basic Usage

```bash
# Generate single page image
python rednote-maker/scripts/make_image.py \
  -t rednote-maker/assets/templates/rednote_style1.html \
  -T "Title" \
  -d "Content" \
  -o output.png

# Generate multi-page for long content
python rednote-maker/scripts/make_image.py \
  -t rednote-maker/assets/templates/rednote_style1.html \
  -T "Title" \
  -d "Long content..." \
  -m \
  -o output.png

# Generate cover image
python rednote-maker/scripts/make_image.py \
  -t rednote-maker/assets/templates/cover_style1.html \
  -T "Graduate School Interview Guide" \
  -s "24考研必看！帮你快速Get复试技巧" \
  -C "考研,复试,研究生" \
  -o cover.png
```

### Parameters

| Parameter | Short | Description | Required |
|-----------|-------|-------------|----------|
| `--template` | `-t` | HTML template file path | Yes |
| `--title` | `-T` | Title | Yes |
| `--desc` | `-d` | Body content | Optional |
| `--output` | `-o` | Output path | Optional |
| `--multi-page` | `-m` | Auto pagination for long content | Optional |
| `--topics` | `-C` | Topic list (comma separated) | Optional |
| `--subtitle` | `-s` | Subtitle (cover only) | Optional |

---

## Mode 2: HTML Mode (HTML模式)

Provide a complete HTML file, and the system renders it directly to an image without template processing.

### Basic Usage

```bash
python rednote-maker/scripts/make_image.py --html-mode -t my_page.html -o output.png
```

### HTML Structure Requirements

Your HTML file should be a complete, valid HTML document with a `#container` element:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
            background: #FAFAFA;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        #container {
            width: 1242px;    /* Auto-detected */
            height: 1660px;   /* Auto-detected */
            background: #FFFFFF;
            padding: 60px;
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

### Viewport Auto-Detection

1. **Primary**: Detects `#container { width: XXXpx; height: XXXpx; }` from CSS
2. **Fallback**: Defaults to **1242×1660** (RedNote recommended size)

### When to Use HTML Mode

- Custom HTML/CSS designs
- Web page to image conversion
- Full control over layout and styling
- Bypass template processing

---

## Available Templates

Location: `rednote-maker/assets/templates/`

### Image Templates

| Template | Style |
|----------|-------|
| `rednote_style1.html` | Black White Minimal |
| `rednote_style2.html` | Vintage Paper |
| `rednote_style3.html` | Candy Gradient |
| `rednote_style4.html` | Purple Starry Sky |
| `rednote_style5.html` | Caramel Cookie |
| `rednote_style6.html` | Retro Chinese |

### Cover Templates

| Template | Style |
|----------|-------|
| `cover_style1.html` | Black White Minimal |
| `cover_style2.html` | Vintage Paper |
| `cover_style3.html` | Candy Gradient |
| `cover_style4.html` | Purple Starry Sky |
| `cover_style5.html` | Caramel Cookie |
| `cover_style6.html` | Retro Chinese |

### Usage Examples

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
```

---

## Custom Templates

### Image Template Structure

```html
<h1 class="title">Title Content</h1>

<div class="content">
    <p>First paragraph</p>
    <p>Second paragraph</p>
</div>

<div class="tags">
    <span class="tag">#topic1</span>
    <span class="tag">#topic2</span>
</div>

<span class="page-num">1/3</span>
```

### Cover Template Structure

```html
<h1 class="cover-title">Cover Title</h1>

<p class="cover-subtitle">Subtitle Content</p>

<div class="cover-tags">
    <span class="cover-tag">#topic1</span>
    <span class="cover-tag">#topic2</span>
</div>
```

### Text Styling

```html
<!-- Color emphasis -->
<span style="color: #FF2442;">Key content</span>
<span style="color: #00FFFF;">Tech style</span>
<span style="color: #FFD700;">Tips</span>

<!-- Size -->
<span style="font-size: 48px;">Large Title</span>
<span style="font-size: 24px;">Small text</span>

<!-- Style -->
<strong>Bold text</strong>
<em>Italic text</em>
<span style="text-decoration: underline;">Underline</span>

<!-- Background highlight -->
<span style="background: #FFE5E5; padding: 2px 8px; border-radius: 4px;">Highlighted</span>
<span style="background: linear-gradient(135deg, #FF6B6B, #FF2442); color: white; padding: 4px 12px; border-radius: 8px;">Gradient</span>
```

### Built-in Style Classes

| Class | Effect |
|-------|--------|
| `.highlight` | Red highlight |
| `.tip` | Orange tip |
| `.note` | Cyan note |

**Important**: Mark ALL key points, not just one!

```html
<!-- Correct -->
<p>Here is <span class="highlight">key point 1</span> and <span class="highlight">key point 2</span></p>

<!-- Wrong -->
<p>Here is <span class="highlight">key point</span> to note</p>
```

---

## Trigger Conditions

Triggered when user requests:
- Generate RedNote image / cover / post
- Generate image from template
- Render HTML to image
- Convert HTML to image

---

## Notes

- Supports jpg, png, jpeg formats
- Topics are auto-formatted (no need to add # manually)
- Recommended cover size: 1080x1080 or 1080x1350
- Long content auto-paginated (max 12-14 lines per page)
