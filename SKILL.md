---
name: rednote-maker
description: Generate RedNote (Xiaohongshu) style cover and image posts. Triggered when user requests generating RedNote images, covers, or image templates.
version: 1.2.0
author: by
tags:
  - xiaohongshu
  - image-generator
  - template
metadata:
  requires:
    pypi: [playwright]
    bins: [webkit]
---

# RedNote Image Generator

Generate RedNote style cover and image posts.

## Trigger Conditions

Triggered when user requests:
- Generate RedNote image
- Generate RedNote cover
- Generate RedNote post
- Generate image from template
- Create RedNote style image

## Install Dependencies

```bash
pip install playwright
playwright install webkit
```

## Basic Usage

### Generate Image Posts

```bash
# Generate single page image from template
python rednote-maker/scripts/make_image.py -t rednote-maker/assets/templates/rednote_style1.html -T "Title" -d "Content"

# Generate multi-page image for long content
python rednote-maker/scripts/make_image.py -t rednote-maker/assets/templates/rednote_style1.html -T "Title" -d "Long content..." -m

# Specify output filename
python rednote-maker/scripts/make_image.py -t rednote-maker/assets/templates/rednote_style3.html -T "Title" -d "Content" -o my_image.png
```

### Generate Cover Images

```bash
# Generate cover using cover template
python rednote-maker/scripts/make_image.py \
  -t rednote-maker/assets/templates/cover_style1.html \
  -T "Graduate School Interview Guide" \
  -s "24考研必看！帮你快速Get复试技巧" \
  -C "考研,复试,研究生" \
  -o cover.png
```

## Parameters

| Parameter | Short | Description |
|-----------|-------|-------------|
| `--template` | `-t` | HTML template file path (required) |
| `--title` | `-T` | Title (required) |
| `--desc` | `-d` | Body content (for image, optional for cover) |
| `--output` | `-o` | Output path, default: rednote_image.png |
| `--multi-page` | `-m` | Auto pagination for long content (image only) |
| `--topics` | `-C` | Topic list, comma separated, e.g. coding,learning |
| `--subtitle` | `-s` | Subtitle (cover only) |

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
