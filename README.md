# Geometry Studio

A web-based tool for learning geometry by drawing and analyzing shapes. Built to actually help with math homework and understanding geometric concepts.

**[👉 Try it here](https://zhirkoalexander-maker.github.io/bender/)** - No installation needed, works in browser.

## Why I made this

I kept using calc for geometry homework but it got annoying - you'd draw something by hand, measure it with a protractor, do the math... lots of room for mistakes. So I built a tool where you just draw the shape and it calculates everything for you. No more "did I measure at the right angle?"

The older version was desktop. The web version is way cleaner and actually useful in class.

## What it does

### Drawing
- Draw triangles, squares, rectangles, circles, or freeform shapes
- Snap to grid to keep things aligned
- Point your cursor where you want it, click, done
- Press F to finish the shape (or double-click)

### Real-time Analysis (the useful part)
When you draw a shape, you instantly get:
- **Side lengths** - all of them
- **Angles** - in degrees
- **Perimeter** - total outline length
- **Area** - using real geometric formulas
- **Triangle detection** - if it's equilateral, isosceles, or right-angled
- **Heights & medians** - perpendiculars and lines to midpoints
- **Heron's formula** - alternative way to verify area

For example: draw a triangle, and it'll immediately tell you the side lengths, all three angles, whether it's a right triangle, what the heights are, and the exact area. Perfect for checking your work.

### Project Management
- Save multiple projects locally
- Switch between them without losing work
- Each project keeps all your shapes
- Quick save button, no dialogs

### Visualization Tools
Toggle these on/off to see:
- **Medians** (red dashed lines) - from vertices to opposite side midpoints
- **Altitudes** (blue lines) - perpendiculars from vertices to sides  
- **Angle bisectors** (purple lines) - splits angles in half
- **Circumcircle** (orange) - circle that passes through all vertices

Perfect for understanding the geometry you're learning about.

### Transformations
- Rotate by any angle
- Scale up or down
- Mirror horizontally or vertically
- Updates all calculations automatically

## How to use it

1. Pick a shape type (Triangle, Square, etc.) or use Freeform for custom shapes
2. Click points on the canvas (grid helps with alignment)
3. Press F when done (or double-click to close)
4. All the math happens instantly in the Analysis panel
5. Use Select mode to pick existing shapes and inspect them
6. Save to a project when you want to come back later

## Keyboard shortcuts

| Key | What it does |
|-----|------------|
| **F** | Finish current shape |
| **Z** | Undo last point |
| **Q** | Clear everything |

## What makes it different

Most drawing tools are just... drawing. This one actually calculates. You get:

- **Instant feedback** - see all the numbers the moment you finish
- **Real formulas** - not approximations. Uses Shoelace formula for area, angle calculation, Heron's formula for triangles
- **Learning features** - highlights triangle types, shows geometric constructions (medians, altitudes, bisectors)
- **Project management** - save your work, come back to it later
- **No backend needed** - everything runs in your browser, nothing sent to servers

## Technical details

- Built with HTML5 Canvas and vanilla JavaScript
- All math calculations happen client-side
- Projects saved in browser's localStorage
- Works offline (once the page loads)
- No external dependencies except the browser

## Try it

**[👉 https://zhirkoalexander-maker.github.io/bender/](https://zhirkoalexander-maker.github.io/bender/)**

Or run locally:

```bash
cd web
python3 -m http.server 8000
```

Then open `http://localhost:8000`

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
