# Chelsea FC Trophy Images - Upload Guide

## Required Images for 3D Carousel

Please save your 5 Chelsea FC trophy celebration images to this directory (`frontend/images/`) with the following **exact filenames**:

### 1. **John Terry - Premier League Trophy**
- **Filename:** `terry-premier-league-trophy.jpg`
- **Description:** John Terry celebrating with the Premier League trophy at Stamford Bridge
- **Recommended Size:** 600x800px (portrait orientation)
- **Your Image:** The player in Chelsea blue jersey with Premier League trophy

### 2. **UEFA Super Cup Celebration**
- **Filename:** `super-cup-celebration.jpg`
- **Description:** Chelsea player celebrating with the UEFA Super Cup trophy
- **Recommended Size:** 600x800px (portrait orientation)
- **Your Image:** Player holding the silver Super Cup trophy

### 3. **Didier Drogba - Champions League**
- **Filename:** `drogba-champions-league.jpg`
- **Description:** Didier Drogba celebrating with the Champions League trophy
- **Recommended Size:** 600x800px (portrait orientation)
- **Your Image:** Drogba with the big-eared Champions League trophy

### 4. **Europa League Team Celebration**
- **Filename:** `europa-league-celebration.jpg`
- **Description:** Chelsea team celebrating Europa League victory (Maurizio Sarri era)
- **Recommended Size:** 600x800px (portrait orientation)
- **Your Image:** Team celebration with Europa League trophy

### 5. **N'Golo Kanté - Champions League 2021**
- **Filename:** `kante-ucl-2021.jpg`
- **Description:** N'Golo Kanté kissing the Champions League trophy (2021 victory)
- **Recommended Size:** 600x800px (portrait orientation)
- **Your Image:** Kanté (#7) with UCL trophy

---

## Image Specifications

### Format
- **Preferred:** JPG or PNG
- **Alternative:** WebP for better performance

### Dimensions
- **Ideal:** 600x800px (3:4 aspect ratio - portrait)
- **Minimum:** 400x533px
- **Maximum:** 1200x1600px

### File Size
- **Target:** 100-300KB per image
- **Maximum:** 500KB per image (optimize for web performance)

### Quality
- High-resolution, clear images
- Good lighting and contrast
- Focused on trophy/celebration moment

---

## Fallback Behavior

The carousel has **automatic fallback** built in:
- If an image fails to load, it will display a placeholder from Unsplash
- The `onerror` attribute handles missing images gracefully
- The 3D carousel will continue rotating even if some images are missing

---

## How to Add Images

### Option 1: Manual Upload
1. Save your 5 trophy images with the exact filenames listed above
2. Place them in: `/Users/nio/blue-sbook/frontend/images/`
3. Refresh your browser - the carousel will automatically load them

### Option 2: Command Line
```bash
# Navigate to images directory
cd /Users/nio/blue-sbook/frontend/images/

# Copy your images here with correct names
cp ~/Downloads/john-terry-pl.jpg terry-premier-league-trophy.jpg
cp ~/Downloads/super-cup.jpg super-cup-celebration.jpg
cp ~/Downloads/drogba-ucl.jpg drogba-champions-league.jpg
cp ~/Downloads/europa-league.jpg europa-league-celebration.jpg
cp ~/Downloads/kante-2021.jpg kante-ucl-2021.jpg
```

---

## Testing

After uploading images:
1. Hard refresh browser: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
2. Open Developer Console (F12)
3. Check for any 404 errors in the Network tab
4. Verify images are loading in the carousel
5. Test 3D rotation is smooth

---

## Current Carousel Configuration

- **Total Items:** 12 carousel items
  - 5 Trophy celebration images (local files)
  - 2 Generic player placeholders (Unsplash fallbacks)
  - 5 Football-themed videos (Coverr CDN)

- **Rotation:** Continuous 360° rotation
- **Speed:** 0.002 degrees per millisecond
- **Radius:** 1000px from center
- **Interactive:** Drag to rotate manually

---

**Questions?** Check the main documentation in `/CLAUDE.md`

KTBFFH! 💙🏆
