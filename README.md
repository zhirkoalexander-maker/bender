# Geometry Studio

A web-based tool for drawing and analyzing geometric shapes. Simple, functional, gets the job done.

## Quick Links

- **[Website](https://zhirkoalexander-maker.github.io/bender/)** - Full documentation and features
- **[Web App](./web/)** - Run locally with Python and Flask

## What is it?

Started as a desktop app for learning geometry. Converted it to a web version because it's more accessible. You can:

- Draw different geometric shapes (triangles, squares, circles, etc.)
- Get calculations done automatically (area, perimeter)
- Transform shapes (rotate, scale, mirror)
- Save and load your drawings

## 30-second Setup

```bash
git clone https://github.com/zhirkoalexander-maker/bender.git
cd bender/web

pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`

## How it Works

1. Select a shape
2. Click points on the canvas
3. Hit F to finish
4. Use tools to transform if you want
5. Save it

That's basically it.

## Features

- **8 Colors** - Cyan, red, blue, orange, mint, pink, purple, light pink
- **Shape Tools** - Triangle, square, rectangle, circle, freeform polygon
- **Transform** - Rotate, scale, mirror (H/V)
- **Calculate** - Automatic area and perimeter
- **Grid** - Optional grid with snap-to-grid
- **Keyboard** - F (finish), Z (undo), Q (clear)
- **Save** - Export as JSON

## Requirements

- Python 3.7+
- Flask

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5 Canvas + Vanilla JavaScript
- **Styling**: CSS with gradient design

## Project Structure

```
.
├── web/                  # Flask app
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── app.js
│       └── style.css
├── docs/                 # GitHub Pages
├── _config.yml
└── main.py              # Original desktop version
```

## What's included

### Backend API

- `/api/analyze` - Get shape properties
- `/api/rotate` - Rotate by angle
- `/api/scale` - Scale by factor
- `/api/mirror` - Mirror horizontally/vertically

### Frontend

- Canvas for drawing
- Color picker (8 colors)
- Shape selection
- Transform controls
- History tracking

## Building it

No build process. Just Flask serving static files. Pretty straightforward.

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
