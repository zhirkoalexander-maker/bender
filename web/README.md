# Geometry Studio

A simple web-based tool for drawing and analyzing geometric shapes. Built with Flask and HTML5 Canvas.

Started as a desktop app (tkinter), turned it into something you can use in the browser. Works pretty well for sketching shapes and getting some basic info about them.

## What it does

- Draw shapes (triangles, squares, circles, whatever)
- Quick calculations for perimeter and area
- Transform shapes (rotate, scale, mirror them around)
- Basic grid system to help you draw straight
- Save your drawings

Nothing too fancy, but gets the job done.

## Running it locally

```bash
git clone https://github.com/zhirkoalexander-maker/bender.git
cd bender/web

pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000`

### Requirements

- Python 3.7+
- Flask

## How to use

Pick a shape, click on the canvas to place points, hit F or double-click to finish. You can transform it after if you want. Pretty straightforward.

Keyboard stuff:
- **F** - finish shape
- **Z** - undo
- **Q** - clear everything

## What's in there

### Backend (Flask)
- Basic shape analysis (calculates area and perimeter)
- Transform endpoints for rotate, scale, mirror
- Not much else, really

### Frontend
- HTML5 canvas for drawing
- Some CSS for the dark theme
- JavaScript that handles the drawing logic and interactions

```
web/
├── app.py
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

## Room for improvement

- Could export as SVG or PDF someday
- Probably could add more measurement tools
- The UI could be cleaner in some places
- Mobile support would be nice

## License

MIT. Do whatever with it.
