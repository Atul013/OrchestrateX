# Infinity Castle Theme Setup Guide

## Overview
This is a Demon Slayer Infinity Castle themed version of the OrchestrateX chatbot interface. The theme features a dark, mystical background with geometric patterns reminiscent of the Infinity Castle from Demon Slayer.

## Video Background Setup

### Required Video File
To complete the Infinity Castle theme, you need to add a video file named `infinity-castle-bg.mp4` to the `public` directory.

**Video Requirements:**
- **Theme**: Demon Slayer Infinity Castle
- **Content**: Focus on the castle architecture and geometric patterns
- **Characters**: Minimal or no character presence (architecture-focused)
- **Duration**: 30-60 seconds (will loop)
- **Quality**: 1920x1080 or higher
- **Format**: MP4 (H.264 codec recommended)
- **File Size**: Keep under 10MB for optimal loading

### Where to Find Suitable Videos
1. **YouTube**: Search for "Demon Slayer Infinity Castle AMV" or "Demon Slayer Infinity Castle Background"
2. **Anime Episodes**: Extract scenes focusing on the castle architecture
3. **Fan-made Content**: Look for architectural flythrough videos of the Infinity Castle

### Video Placement
1. Download/create your Infinity Castle video
2. Name it `infinity-castle-bg.mp4`
3. Place it in the `public` directory: `public/infinity-castle-bg.mp4`

## Theme Features

### Visual Elements
- **Background**: Dark gradient with purple, magenta, and deep blue tones
- **Geometric Patterns**: Animated floating patterns inspired by the Infinity Castle's architecture
- **Glassmorphism**: Enhanced glass effects with Infinity Castle color scheme
- **Neon Glow**: Purple and magenta glow effects throughout the interface

### Color Palette
- Primary: `#8A2BE2` (Blue Violet)
- Secondary: `#FF1493` (Deep Pink)
- Accent: `#9400D3` (Dark Violet)
- Background: `#4B0082` (Indigo)

### Animations
- **Floating Cubes**: Geometric elements that rotate and float
- **Pattern Movement**: Animated background patterns
- **Neon Glow**: Pulsing glow effects on interactive elements

## Installation and Running

1. Navigate to the project directory:
   ```bash
   cd "D:\OrchestrateX\FRONTEND\CHAT BOT UI\ORCHACHATBOT_INFINITY_CASTLE\project"
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Add your Infinity Castle video to the `public` directory

4. Start the development server:
   ```bash
   npm run dev
   ```

## Customization

### Adjusting Video Opacity
In `src/App.tsx`, modify the video opacity:
```tsx
className="absolute inset-0 w-full h-full object-cover opacity-60"
```
Change `opacity-60` to any value between `opacity-10` (very transparent) to `opacity-100` (fully opaque).

### Modifying Colors
Update the color values in `src/index.css` in the `.infinity-castle-bg` and related classes.

### Animation Speed
Adjust animation durations in the keyframe animations:
- `infinity-pattern-move`: Pattern movement speed
- `infinity-float`: Floating elements speed
- `infinity-lines-rotate`: Line rotation speed

## Troubleshooting

### Video Not Loading
1. Ensure the video file is named exactly `infinity-castle-bg.mp4`
2. Check that the file is in the `public` directory
3. Verify the video format is MP4
4. Try refreshing the browser cache

### Performance Issues
1. Reduce video file size
2. Lower video quality/resolution
3. Adjust animation speeds in CSS
4. Reduce the number of animated elements

## Files Modified for Infinity Castle Theme

1. `src/App.tsx` - Added video background and theme classes
2. `src/index.css` - Complete theme styling with animations
3. This setup guide

The theme maintains all original functionality while providing an immersive Infinity Castle aesthetic.