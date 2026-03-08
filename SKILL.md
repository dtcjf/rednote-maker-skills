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

### Font & Readability Guidelines (Important!)

**To ensure text is clearly visible on mobile devices, follow these guidelines:**

#### Minimum Font Sizes

| Element | Minimum Size | Recommended Size |
|---------|--------------|------------------|
| Title | 72px | 84-108px |
| Subtitle | 54px | 60-72px |
| Body text | 48px | 54-66px |
| Captions/Tags | 36px | 39-45px |
| Page numbers | 36px | 39-42px |

#### Content Overflow Prevention (Important!)

**To prevent content from exceeding the 1660px container height, follow these guidelines:**

| Element | Recommended Count | Notes |
|---------|-------------------|-------|
| Title lines | 1-2 lines | Keep titles concise |
| Body paragraphs | 4-6 paragraphs | Reduce if using large fonts |
| List items | 3-4 items | Use compact spacing |
| Action boxes | 1-2 boxes | Combine content if needed |

**Tips to avoid overflow:**

1. **Reduce padding/margins** when content is tight:
   ```css
   #container { padding: 60px 50px; }  /* Instead of 80px 70px */
   .content p { margin-bottom: 25px; } /* Instead of 35px */
   ```

2. **Use compact list spacing**:
   ```css
   li { margin-bottom: 12px; padding-left: 40px; }
   ```

3. **Limit action boxes** to essential content only

4. **Test content fit** before generating final images

#### Line Height & Spacing

```css
/* Recommended line height for readability */
body { line-height: 1.6; }
.title { line-height: 1.3; }
.content { line-height: 1.8-2.0; }

/* Paragraph spacing */
p { margin-bottom: 20-30px; }
```

#### Color Contrast

```css
/* High contrast for readability */
.title { color: #1A1A1A; }           /* Dark on light */
.content { color: #333333; }         /* Slightly lighter */

/* On dark backgrounds */
.title { color: #FFFFFF; }           /* White on dark */
.content { color: rgba(255,255,255,0.9); }

/* Highlight colors - use sparingly */
.highlight { color: #FF2442; }       /* Red accent */
.tip { color: #FFD700; }             /* Gold accent */
```

#### Complete Example with Proper Sizing

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
            min-height: 100vh;
        }

        #container {
            width: 1242px;
            height: 1660px;
            background: #FFFFFF;
            padding: 70px 60px;
        }

        /* Title: 84-108px recommended */
        .title {
            font-size: 96px;
            font-weight: 700;
            color: #1A1A1A;
            line-height: 1.3;
            margin-bottom: 40px;
        }

        /* Body: 54-66px recommended */
        .content {
            font-size: 60px;
            color: #333333;
            line-height: 1.9;
        }

        .content p {
            margin-bottom: 25px;
        }

        /* Tags: 39-45px recommended */
        .tag {
            font-size: 42px;
            padding: 12px 24px;
        }

        /* Page number: 39-42px recommended */
        .page-num {
            font-size: 42px;
        }
    </style>
</head>
<body>
    <div id="container">
        <h1 class="title">标题文字</h1>
        <div class="content">
            <p>正文内容，字号40px确保手机上清晰可见。</p>
        </div>
    </div>
</body>
</html>
```

#### Why These Sizes?

- **1242px width** is 2x the iPhone logical resolution (621pt)
- **40px font** appears as ~20pt on screen, comfortable for reading
- **Smaller fonts** may look blurry or hard to read on mobile devices

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

## Writing RedNote-Style Copy

When generating RedNote (Xiaohongshu) content, follow these copywriting guidelines:

### RedNote Copy Style Characteristics

**1. Conversational and Personal**
- Write as if chatting with a friend
- Use first-person perspective ("I", "my")
- Be relatable and authentic

**Example:**
```
❌ "This product is very good and recommended."
✅ "OMG! I've been using this for a week and my skin is literally glowing!"
```

**2. Use Emotional Expressions**
- Common RedNote expressions:
  - "绝了" (Absolutely amazing)
  - "种草" (Recommend / Put on wishlist)
  - "拔草" (Bought and tried)
  - "YYDS" (Eternal god - best ever)
  - "宝藏" (Hidden gem)
  - "踩雷" (Bad experience)
  - "干货" (Solid content / Useful info)

**3. Rich Formatting**
- Use emojis liberally ✨🌟💫
- Short paragraphs (2-3 lines max)
- Use bullet points and numbering
- Add personal touches and anecdotes

**4. Hashtag Strategy**
- Include 3-5 relevant hashtags
- Mix of broad and specific tags
- Popular tags: #小红书 #好物分享 #生活记录 #ootd

### Copy Templates

**Template 1: Product Review**
```
标题：被问了800遍的XX！真的绝了！

姐妹们！今天必须给你们安利这个XX！
✨ 颜值：绝绝子！实物比图片还好看
✨ 使用感：超级XX，完全不XX
✨ 性价比：学生党也能冲！

用了XX天真的离不开了！
姐妹们快冲！🏃‍♀️💨

#好物分享 #XX推荐 #宝藏好物
```

**Template 2: Tutorial/Guide**
```
标题：保姆级XX教程！新手一看就会！

姐妹们要的XX教程来啦！
全程干货！建议收藏⭐

Step 1: XX
💡 小技巧：XX

Step 2: XX
⚠️ 注意：XX

Step 3: XX
✨ 效果：XX

真的超级简单！
手残党也能学会！
快去试试吧～

#干货分享 #XX教程 #新手必看
```

**Template 3: Lifestyle/Plog**
```
标题：XX日常｜这就是我想要的生活✨

记录一下今天的XX～

🌞 早上XX
☕ 中午XX
🌙 晚上XX

虽然是很平常的一天
但是感觉很幸福💕

你们今天过得怎么样？
评论区聊聊吧～

#日常记录 #生活碎片 #plog
```

## Image Size Guidelines

| Type | Size | Aspect Ratio |
|------|------|--------------|
| Cover | 1080×1080px or 1080×1350px | 1:1 or 4:5 |
| Post Images | 1242×1660px (recommended) | 3:4 |
| Long Images | 1080×1920px | 9:16 |

## Notes

- Supports jpg, png, jpeg formats
- Topics are auto-formatted (no need to add # manually)
- Recommended cover size: 1080x1080 or 1080x1350
- Long content auto-paginated (max 12-14 lines per page)
