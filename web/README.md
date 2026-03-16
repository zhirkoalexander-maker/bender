# 🎨 GEOMETRY STUDIO - Web Version

Interactive geometric drawing application with beautiful modern UI. Create, analyze, and transform geometric shapes with ease.

## ✨ Features

- **Interactive Canvas**: Click to place points and create shapes
- **Multiple Shapes**: Triangle, Square, Rectangle, Circle, and Free Polygon
- **Rich Color Palette**: 8 beautiful gradient colors to choose from
- **Advanced Tools**:
  - 🔄 Rotate shapes
  - 📏 Scale/Resize
  - ↔/↕ Mirror (Horizontal/Vertical)
  - 🎯 Move shapes
  - 🗑 Clear canvas
  
- **Shape Analysis**: 
  - Automatic perimeter calculation
  - Area computation using Shoelace formula
  - Visual polygon properties
  
- **Smart Features**:
  - Grid system with snap-to-grid
  - Keyboard shortcuts (Z=Undo, F=Finish, Q=Clear)
  - Action history tracking
  - Save drawings as JSON
  - Real-time coordinate display

- **Beautiful UI**:
  - Modern gradient design
  - Dark theme with vibrant accents
  - Responsive layout
  - Smooth animations
  - Interactive buttons with ripple effects

## 🚀 Getting Started

### Requirements
- Python 3.7+
- Flask 2.3+

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/zhirkoalexander-maker/bender.git
cd bender/web
```

2. **Create virtual environment** (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
python app.py
```

5. **Open in browser**:
```
http://localhost:5000
```

## 🎮 How to Use

1. **Select a Shape**: Click one of the shape buttons on the left panel
2. **Place Points**: Click on the canvas to place points
3. **Finish Shape**: Double-click, press F, or click the "Finish" button
4. **Transform**:
   - Use rotation, scaling, or mirroring tools
   - Apply transformations to modify your shapes
5. **Save**: Click "Save" to download drawings as JSON files

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| F | Finish current shape |
| Z | Undo last action |
| Q | Clear canvas |

## 🎨 Color Palette

- **Red**: #FF6B6B
- **Cyan**: #4ECDC4
- **Blue**: #45B7D1
- **Orange**: #FFA502
- **Mint**: #95E1D3
- **Pink**: #F38181
- **Purple**: #AA96DA
- **Light Pink**: #FCBAD3

## 📊 Project Structure

```
web/
├── app.py              # Flask server & API
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
├── templates/
│   └── index.html     # Main page
└── static/
    ├── style.css      # Beautiful gradient styles
    └── app.js         # Interactive canvas logic
```

## 🔧 API Endpoints

- `GET /` - Main page
- `POST /api/analyze` - Analyze shape properties
- `POST /api/rotate` - Rotate shape
- `POST /api/scale` - Scale shape
- `POST /api/mirror` - Mirror shape
- `POST /api/save` - Save drawing
- `GET /api/drawings` - Get all saved drawings

## 🎯 Features Coming Soon

- [ ] SVG export
- [ ] Cloud save with accounts
- [ ] Shape templates library
- [ ] Advanced formula solver
- [ ] Measurement tools
- [ ] 3D rendering

## 📝 License

MIT License - feel free to use and modify!

## 👨‍💻 Author

Created with ❤️ by **zhirkoalexander-maker**

---

**Enjoy creating beautiful geometric art!** 🚀✨
