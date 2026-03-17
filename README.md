# Geometry Studio

Draw shapes on a canvas and get instant calculations. No measuring with a protractor, no calculator - just draw and the numbers show up automatically.

**[Try it](https://zhirkoalexander-maker.github.io/bender/)** - opens in your browser, no download or setup.

## Why it exists

I got tired of the geometry homework workflow: draw a shape, measure everything with a ruler and protractor, punch numbers into a calculator. Too many places to mess up. Built this so you just draw it and the tool figures out all the angles, lengths, area, whatever.

## What you can do

Draw pretty much anything - triangles, squares, rectangles, circles, or irregular shapes. The tool calculates:
- All side lengths
- All angles
- Perimeter and area
- For triangles specifically: heights, medians, and what type (equilateral, isosceles, etc.)
- Heron's formula for verification

If you don't feel like drawing, you can build shapes by typing in dimensions instead. It has templates for common shapes.

You can also flip shapes around, rotate them, make them bigger or smaller. The calculations stay accurate.

## Visualizing geometry

Turn on visual aids to understand what's happening:
- Medians (lines from corners to opposite side midpoints)
- Altitudes (perpendiculars from corners to opposite sides)  
- Angle bisectors (lines that split angles in half)
- Circumcircle (circle touching all corners of a triangle)

Helps with actually understanding the geometry instead of just memorizing it.

## Basic flow

1. Pick a shape type on the left
2. Click on the canvas to place points
3. Press F or double-click when done
4. Numbers appear in the analysis panel
5. Save your work using the Projects button

## Keys

- **F** - finish shape
- **Z** - undo last point
- **Q** - clear everything

## How it works

Everything runs in your browser. No servers, no uploading. Your projects save locally so they stick around.

Built with HTML5 Canvas and JavaScript. Math uses actual geometric formulas - Shoelace formula for area, proper angle calculations, all that.

## Run it

**[https://zhirkoalexander-maker.github.io/bender/](https://zhirkoalexander-maker.github.io/bender/)**

Or locally:

```bash
cd web
python3 -m http.server 8000
```

Then `http://localhost:8000`

---

Made for actually understanding geometry, not just drawing shapes. If you've got a math test coming up, this might actually help.

## Why I made this

Needed a simple way to visualize geometric shapes and their properties. The math was interesting, and a web interface is easier to share than a desktop app.

## Future ideas

- SVG/PDF export
- More tools (measuring, angles, etc.)
- Better mobile support
- Cleaner UI in some places

## License

MIT - do whatever you want with it.

---

More info on the [website](https://zhirkoalexander-maker.github.io/bender/)
