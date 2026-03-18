import tkinter as tk
from tkinter import messagebox, simpledialog
import math
from datetime import datetime

class GeometryStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Geometry Studio")
        self.root.geometry("1400x850")
        self.root.configure(bg='#0a0e27')
        
        # Canvas settings
        self.canvas_width = 650
        self.canvas_height = 750
        self.points = []
        self.midpoints = []
        self.circle_center = None
        self.grid_size = 20
        self.axis_offset = 60
        self.current_color = '#FF0000'
        self.shape_finished = False
        
        # State
        self.mode = "triangle"
        self.grid_enabled = True
        self.snap_enabled = True
        self.drag_mode = False
        self.midpoint_mode = False
        self.history = []
        
        # Список сохранённых фигур
        self.shapes = []  # [(points, color, mode), ...]
        self.selected_shape_idx = None
        
        # Визуальные помощники
        self.show_altitude = False
        self.show_diagonal = False
        self.altitude_vertex = None
        self.diagonal_points = None
        
        # Keyboard shortcuts
        self.root.bind('q', lambda e: self.clear_all())
        self.root.bind('d', lambda e: self.toggle_drag_mode())
        self.root.bind('m', lambda e: self.toggle_midpoint_mode())
        self.root.bind('z', lambda e: self.undo())
        self.root.bind('f', lambda e: self.finish_shape())
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg='#0f2847', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🎨 GEOMETRY STUDIO", font=('Arial', 16, 'bold'),
                bg='#0f2847', fg='#00d4ff').pack(side=tk.LEFT, padx=20, pady=10)
        
        self.status_label = tk.Label(header, text="✓ Ready", font=('Arial', 11, 'bold'),
                                    bg='#0f2847', fg='#10b981')
        self.status_label.pack(side=tk.LEFT, padx=30, pady=10)
        
        # Quick buttons
        btns_frame = tk.Frame(header, bg='#0f2847')
        btns_frame.pack(side=tk.RIGHT, padx=15, pady=8)
        
        tk.Button(btns_frame, text="New (Q)", command=self.clear_all, 
                 bg='#1a2547', fg='#00d4ff', font=('Arial', 9), 
                 relief=tk.FLAT, padx=6, pady=3).pack(side=tk.LEFT, padx=3)
        tk.Button(btns_frame, text="Finish (F)", command=self.finish_shape, 
                 bg='#1a2547', fg='#00d4ff', font=('Arial', 9), 
                 relief=tk.FLAT, padx=6, pady=3).pack(side=tk.LEFT, padx=3)
        tk.Button(btns_frame, text="Undo (Z)", command=self.undo, 
                 bg='#1a2547', fg='#00d4ff', font=('Arial', 9), 
                 relief=tk.FLAT, padx=6, pady=3).pack(side=tk.LEFT, padx=3)
        tk.Button(btns_frame, text="Drag (D)", command=self.toggle_drag_mode, 
                 bg='#1a2547', fg='#00d4ff', font=('Arial', 9), 
                 relief=tk.FLAT, padx=6, pady=3).pack(side=tk.LEFT, padx=3)
        tk.Button(btns_frame, text="Marks (M)", command=self.toggle_midpoint_mode, 
                 bg='#1a2547', fg='#00d4ff', font=('Arial', 9), 
                 relief=tk.FLAT, padx=6, pady=3).pack(side=tk.LEFT, padx=3)
        tk.Button(btns_frame, text="Save", command=self.save_data, 
                 bg='#1a2547', fg='#00d4ff', font=('Arial', 9), 
                 relief=tk.FLAT, padx=6, pady=3).pack(side=tk.LEFT, padx=3)
        
        # Content area
        content = tk.Frame(self.root, bg='#0a0e27')
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # LEFT PANEL
        left = tk.Frame(content, bg='#0f1535', relief=tk.RAISED, bd=1)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        tk.Label(left, text="SHAPES", font=('Arial', 10, 'bold'),
                bg='#0f1535', fg='#00d4ff').pack(pady=(10, 8), padx=10)
        
        self.shape_btns = {}
        shapes = [("Triangle", "triangle", "#FF0000"),
                 ("Rectangle", "rectangle", "#0066FF"),
                 ("Square", "square", "#FFFF00"),
                 ("Circle", "circle", "#00FF00"),
                 ("Freeform", "freeform", "#FF00FF")]
        
        for text, val, color in shapes:
            btn = tk.Button(left, text=text, font=('Arial', 9, 'bold'),
                           width=14, height=2, bg='#1a2547', fg='white',
                           activebackground=color, relief=tk.FLAT, bd=0,
                           cursor='hand2',
                           command=lambda v=val, c=color: self.select_shape(v, c))
            btn.pack(fill=tk.X, padx=10, pady=2)
            self.shape_btns[val] = btn
        
        # Colors
        tk.Label(left, text="COLORS", font=('Arial', 10, 'bold'),
                bg='#0f1535', fg='#00d4ff').pack(pady=(15, 8), padx=10)
        
        colors = [('#FF0000', 'Red'), ('#0066FF', 'Blue'), ('#FFFF00', 'Yellow'),
                 ('#00FF00', 'Green'), ('#FF00FF', 'Magenta'), ('#00FFFF', 'Cyan')]
        
        for color, name in colors:
            tk.Button(left, text=name, bg=color, fg='white',
                     font=('Arial', 8, 'bold'), width=14,
                     relief=tk.FLAT, bd=0, cursor='hand2',
                     command=lambda c=color: self.set_color(c)).pack(fill=tk.X, padx=10, pady=1)
        
        # Tools
        tk.Label(left, text="TOOLS", font=('Arial', 10, 'bold'),
                bg='#0f1535', fg='#00d4ff').pack(pady=(15, 8), padx=10)
        
        tk.Button(left, text="Rotate", command=self.rotate_shape,
                 bg='#1a2547', fg='#00d4ff', font=('Arial', 9, 'bold'),
                 relief=tk.FLAT, bd=0, cursor='hand2', 
                 width=14, height=1).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(left, text="Move", command=self.move_shape,
                 bg='#1a2547', fg='#00d4ff', font=('Arial', 9, 'bold'),
                 relief=tk.FLAT, bd=0, cursor='hand2',
                 width=14, height=1).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(left, text="Mirror H", command=self.mirror_horizontal,
                 bg='#1a2547', fg='#00d4ff', font=('Arial', 9, 'bold'),
                 relief=tk.FLAT, bd=0, cursor='hand2',
                 width=14, height=1).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(left, text="Mirror V", command=self.mirror_vertical,
                 bg='#1a2547', fg='#00d4ff', font=('Arial', 9, 'bold'),
                 relief=tk.FLAT, bd=0, cursor='hand2',
                 width=14, height=1).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(left, text="Scale", command=self.scale_shape,
                 bg='#1a2547', fg='#00d4ff', font=('Arial', 9, 'bold'),
                 relief=tk.FLAT, bd=0, cursor='hand2',
                 width=14, height=1).pack(fill=tk.X, padx=10, pady=2)
        
        # Helpers
        tk.Label(left, text="HELPERS", font=('Arial', 10, 'bold'),
                bg='#0f1535', fg='#ff6b6b').pack(pady=(15, 8), padx=10)
        
        tk.Button(left, text="🏔️ Altitude", command=self.toggle_altitude,
                 bg='#1a2547', fg='#ff6b6b', font=('Arial', 9, 'bold'),
                 relief=tk.FLAT, bd=0, cursor='hand2',
                 width=14, height=1).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(left, text="📍 Diagonal", command=self.toggle_diagonal,
                 bg='#1a2547', fg='#ff6b6b', font=('Arial', 9, 'bold'),
                 relief=tk.FLAT, bd=0, cursor='hand2',
                 width=14, height=1).pack(fill=tk.X, padx=10, pady=2)
        tk.Button(left, text="🎯 Select Shape", command=self.select_shape_mode,
                 bg='#1a2547', fg='#ff6b6b', font=('Arial', 9, 'bold'),
                 relief=tk.FLAT, bd=0, cursor='hand2',
                 width=14, height=1).pack(fill=tk.X, padx=10, pady=2)
        
        # Display
        tk.Label(left, text="DISPLAY", font=('Arial', 10, 'bold'),
                bg='#0f1535', fg='#00d4ff').pack(pady=(15, 8), padx=10)
        
        self.grid_var = tk.BooleanVar(value=True)
        self.snap_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(left, text="Grid", variable=self.grid_var,
                      bg='#0f1535', fg='#e0e6ff', font=('Arial', 9),
                      selectcolor='#0f1535',
                      command=self.redraw_canvas).pack(anchor=tk.W, padx=15, pady=2)
        tk.Checkbutton(left, text="Snap", variable=self.snap_var,
                      bg='#0f1535', fg='#e0e6ff', font=('Arial', 9),
                      selectcolor='#0f1535').pack(anchor=tk.W, padx=15, pady=2)
        
        # CENTER PANEL
        center = tk.Frame(content, bg='#0a0e27')
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(center, text="CANVAS", font=('Arial', 10, 'bold'),
                bg='#0a0e27', fg='#00d4ff').pack(pady=(0, 8))
        
        canvas_frame = tk.Frame(center, bg='#1a2547', relief=tk.SUNKEN, bd=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height,
                               bg='white', highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Info
        tk.Label(center, text="INFO", font=('Arial', 10, 'bold'),
                bg='#0a0e27', fg='#00d4ff').pack(pady=(8, 5))
        
        info_frame = tk.Frame(center, bg='#1a2547', relief=tk.SUNKEN, bd=1)
        info_frame.pack(fill=tk.X)
        
        self.info_text = tk.Text(info_frame, height=3, font=('Courier', 9),
                                bg='#1a2547', fg='#00ff88', state=tk.DISABLED)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.update_info("Ready")
        
        # RIGHT PANEL
        right = tk.Frame(content, bg='#0f1535', relief=tk.RAISED, bd=1)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right, text="AI ASSISTANT", font=('Arial', 10, 'bold'),
                bg='#0f1535', fg='#00d4ff').pack(pady=(10, 8), padx=10)
        
        chat_frame = tk.Frame(right, bg='#050812', relief=tk.SUNKEN, bd=1)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        scroll = tk.Scrollbar(chat_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat = tk.Text(chat_frame, height=40, width=50, font=('Courier', 8),
                           bg='#050812', fg='#00ffff', yscrollcommand=scroll.set, state=tk.DISABLED)
        self.chat.pack(fill=tk.BOTH, expand=True)
        scroll.config(command=self.chat.yview)
        
        self.chat_print("\n🎨 GEOMETRY STUDIO v2.0\n\n")
        self.chat_print("📚 TIPS:\n")
        self.chat_print("  • Click shape button\n")
        self.chat_print("  • Click canvas to add points\n")
        self.chat_print("  • Press F to finish shape\n")
        self.chat_print("  • Use Drag to move\n")
        self.chat_print("  • Use Marks for midpoints\n\n")
        
        # Formula
        input_frame = tk.Frame(right, bg='#0f1535')
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(input_frame, text="Formula:", font=('Arial', 9),
                bg='#0f1535', fg='#e0e6ff').pack(side=tk.LEFT)
        
        self.formula_input = tk.Entry(input_frame, font=('Courier', 9),
                                     bg='#1a2547', fg='#00ffff', insertbackground='#00ffff')
        self.formula_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        self.formula_input.bind('<Return>', lambda e: self.analyze_formula())
        
        tk.Button(input_frame, text="Analyze", command=self.analyze_formula,
                 bg='#1a2547', fg='#00d4ff', font=('Arial', 8, 'bold'),
                 relief=tk.FLAT, bd=0, cursor='hand2').pack(side=tk.LEFT)
        
        # Now set initial shape and bind events
        self.select_shape("triangle", "#FF0000")
        self.bind_canvas_events()
        self.redraw_canvas()
    
    def select_shape(self, shape, color):
        self.mode = shape
        self.current_color = color
        for btn in self.shape_btns.values():
            btn.config(bg='#1a2547')
        self.shape_btns[shape].config(bg=color)
        self.reset_shape()
        self.update_status(f"✓ {shape.upper()}")
        self.chat_print(f"\n> {shape.upper()}\n")
    
    def bind_canvas_events(self):
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
    
    def on_motion(self, e):
        rx, ry = self.canvas_to_real(e.x, e.y)
        self.root.title(f"X={rx:.0f} Y={ry:.0f} | {self.mode}")
    
    def on_click(self, e):
        if self.midpoint_mode:
            self.mark_midpoint(e.x, e.y)
            return
        
        if self.drag_mode and self.points:
            self.start_drag(e.x, e.y)
            return
        
        x, y = self.snap_point(e.x, e.y)
        self.history.append((self.points.copy(), self.circle_center))
        
        mode = self.mode
        
        if mode == "circle":
            if self.circle_center is None:
                self.circle_center = (x, y)
                self.points = [(x, y)]
                self.update_status("Center set")
                self.chat_print("> Center set\n")
            else:
                self.points.append((x, y))
                self.analyze_shape()
                self.shape_finished = True
                self.update_status("✓ Done!")
                self.chat_print("> Circle done!\n")
            self.redraw_canvas()
        elif mode == "square":
            if len(self.points) < 2:
                self.points.append((x, y))
                if len(self.points) == 1:
                    self.update_status("Point 1/2")
                    self.chat_print("> Point 1/2\n")
                else:
                    self.create_square()
                    self.update_status("✓ Done!")
                    self.chat_print("> Square done!\n")
            self.redraw_canvas()
        elif mode == "rectangle":
            if len(self.points) < 2:
                self.points.append((x, y))
                if len(self.points) == 1:
                    self.update_status("Point 1/2")
                    self.chat_print("> Point 1/2\n")
                else:
                    self.create_rectangle()
                    self.update_status("✓ Done!")
                    self.chat_print("> Rectangle done!\n")
            self.redraw_canvas()
        elif mode == "triangle":
            if len(self.points) < 3:
                self.points.append((x, y))
                self.update_status(f"Point {len(self.points)}/3")
                self.chat_print(f"> Point {len(self.points)}/3\n")
            self.redraw_canvas()
            if len(self.points) == 3:
                self.analyze_shape()
        else:
            self.points.append((x, y))
            self.update_status(f"Point {len(self.points)}")
            self.chat_print(f"> Point {len(self.points)}\n")
            self.redraw_canvas()
    
    def on_double_click(self, e):
        if len(self.points) >= 3:
            self.finish_shape()
    
    def on_drag(self, e):
        if self.drag_mode and hasattr(self, 'drag_start_x'):
            dx = e.x - self.drag_start_x
            dy = e.y - self.drag_start_y
            
            self.points = [(p[0] + dx, p[1] + dy) for p in self.points]
            if self.circle_center:
                self.circle_center = (self.circle_center[0] + dx, self.circle_center[1] + dy)
            
            self.drag_start_x = e.x
            self.drag_start_y = e.y
            self.redraw_canvas()
    
    def on_release(self, e):
        if hasattr(self, 'drag_start_x'):
            del self.drag_start_x
    
    def snap_point(self, x, y):
        if not self.snap_var.get():
            return x, y
        grid = self.grid_size
        snapped_x = round((x - self.axis_offset) / grid) * grid + self.axis_offset
        snapped_y = round((y - self.axis_offset) / grid) * grid + self.axis_offset
        return snapped_x, snapped_y
    
    def canvas_to_real(self, x, y):
        return ((x - self.axis_offset) / self.grid_size, 
                (self.axis_offset - y) / self.grid_size)
    
    def reset_shape(self):
        self.points = []
        self.circle_center = None
        self.midpoints = []
        self.shape_finished = False
        if hasattr(self, 'canvas'):
            self.redraw_canvas()
            self.update_info("Ready")
    
    def toggle_drag_mode(self):
        if not self.points:
            messagebox.showwarning("Error", "Draw first!")
            return
        self.drag_mode = not self.drag_mode
        self.midpoint_mode = False
        status = "ON" if self.drag_mode else "OFF"
        self.update_status(f"Drag: {status}")
        self.chat_print(f"> Drag {status}\n")
    
    def toggle_midpoint_mode(self):
        if len(self.points) < 2:
            messagebox.showwarning("Error", "Need 2+ points!")
            return
        self.midpoint_mode = not self.midpoint_mode
        self.drag_mode = False
        status = "ON" if self.midpoint_mode else "OFF"
        self.update_status(f"Marks: {status}")
        self.chat_print(f"> Marks {status}\n")
    
    def start_drag(self, x, y):
        self.drag_start_x = x
        self.drag_start_y = y
    
    def mark_midpoint(self, click_x, click_y):
        if len(self.points) < 2:
            return
        
        min_dist = 15
        closest_mid = None
        
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            dist, mid = self.distance_to_segment(click_x, click_y, p1, p2)
            if dist < min_dist:
                min_dist = dist
                closest_mid = mid
        
        if closest_mid:
            if closest_mid not in self.midpoints:
                self.midpoints.append(closest_mid)
                self.redraw_canvas()
                self.chat_print("> Midpoint marked\n")
    
    def distance_to_segment(self, px, py, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1
        
        if dx == 0 and dy == 0:
            return math.sqrt((px - x1)**2 + (py - y1)**2), p1
        
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx*dx + dy*dy)))
        closest = (x1 + t * dx, y1 + t * dy)
        dist = math.sqrt((px - closest[0])**2 + (py - closest[1])**2)
        mid = ((x1 + x2) / 2, (y1 + y2) / 2)
        
        return dist, mid
    
    def create_square(self):
        if len(self.points) < 2:
            return
        
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        side = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        if side > 0:
            dx = (x2 - x1) / side
            dy = (y2 - y1) / side
        else:
            dx, dy = 1, 0
        
        px, py = -dy, dx
        
        self.points = [
            (x1, y1),
            (x1 + dx * side, y1 + dy * side),
            (x1 + dx * side + px * side, y1 + dy * side + py * side),
            (x1 + px * side, y1 + py * side)
        ]
        self.analyze_shape()
        self.shape_finished = True
    
    def create_rectangle(self):
        if len(self.points) < 2:
            return
        
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        
        self.points = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        self.analyze_shape()
        self.shape_finished = True
    
    def redraw_canvas(self):
        self.canvas.delete("all")
        
        # Grid
        if self.grid_var.get():
            for i in range(0, self.canvas_width, self.grid_size):
                self.canvas.create_line(i, 0, i, self.canvas_height, fill='#cccccc', width=1)
            for i in range(0, self.canvas_height, self.grid_size):
                self.canvas.create_line(0, i, self.canvas_width, i, fill='#cccccc', width=1)
        
        # Axes
        self.draw_axes()
        
        # Рисуем все сохранённые фигуры
        for idx, (pts, color, mode) in enumerate(self.shapes):
            # Подсветка выбранной фигуры
            shape_color = color
            shape_width = 4
            if idx == self.selected_shape_idx:
                shape_color = '#FFD700'  # Gold для выбранной
                shape_width = 6
            
            if len(pts) > 1:
                for i in range(len(pts) - 1):
                    x1, y1 = pts[i]
                    x2, y2 = pts[i + 1]
                    self.canvas.create_line(x1, y1, x2, y2, fill=shape_color, width=shape_width, dash=(4, 4))
                
                # Замыкаем фигуру
                if len(pts) >= 2:
                    x1, y1 = pts[-1]
                    x2, y2 = pts[0]
                    self.canvas.create_line(x1, y1, x2, y2, fill=shape_color, width=shape_width, dash=(4, 4))
                
                if len(pts) >= 3:
                    points_flat = [c for p in pts for c in p]
                    self.canvas.create_polygon(*points_flat, fill='', 
                                              outline=shape_color, width=shape_width)
        
        # Draw current shape
        if self.mode == "circle" and self.circle_center:
            cx, cy = self.circle_center
            if len(self.points) > 1:
                rx, ry = self.points[1]
                radius = math.sqrt((rx - cx)**2 + (ry - cy)**2)
                self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                                       fill=self.current_color, outline=self.current_color, width=4)
            self.canvas.create_oval(cx - 8, cy - 8, cx + 8, cy + 8, fill='#FF0000', outline='white', width=2)
        else:
            if len(self.points) > 1:
                for i in range(len(self.points) - 1):
                    x1, y1 = self.points[i]
                    x2, y2 = self.points[i + 1]
                    self.canvas.create_line(x1, y1, x2, y2, fill=self.current_color, width=4)
                
                # Замыкаем фигуру линией от последней точки к первой
                if len(self.points) >= 2:
                    x1, y1 = self.points[-1]
                    x2, y2 = self.points[0]
                    self.canvas.create_line(x1, y1, x2, y2, fill=self.current_color, width=4)
                
                if self.shape_finished and len(self.points) >= 3:
                    points_flat = [c for p in self.points for c in p]
                    self.canvas.create_polygon(*points_flat, fill=self.current_color, 
                                              outline=self.current_color, width=2)
        
        # Points
        for i, (x, y) in enumerate(self.points):
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='#FFFF00', outline='#000000', width=2)
            self.canvas.create_text(x, y, text=str(i + 1), fill='#000000', 
                                   font=('Arial', 12, 'bold'))
        
        # Midpoints
        for mx, my in self.midpoints:
            self.canvas.create_oval(mx - 8, my - 8, mx + 8, my + 8, fill='#00FF00', outline='#000000', width=2)
        
        # Рисуем высоту если активна
        if self.show_altitude and len(self.points) >= 3 and self.altitude_vertex is not None:
            self.draw_altitude()
        
        # Рисуем диагональ если активна
        if self.show_diagonal and len(self.points) >= 3:
            self.draw_diagonals()
    
    def draw_axes(self):
        self.canvas.create_line(self.axis_offset, self.axis_offset, self.canvas_width, self.axis_offset,
                               fill='#000000', width=3)
        self.canvas.create_line(self.axis_offset, self.axis_offset, self.axis_offset, 0,
                               fill='#000000', width=3)
        
        for i in range(0, self.canvas_width - self.axis_offset, self.grid_size * 2):
            x = self.axis_offset + i
            self.canvas.create_line(x, self.axis_offset - 7, x, self.axis_offset + 7, fill='#000000', width=2)
        
        for i in range(0, self.axis_offset, self.grid_size * 2):
            y = self.axis_offset - i
            self.canvas.create_line(self.axis_offset - 7, y, self.axis_offset + 7, y, fill='#000000', width=2)
        
        self.canvas.create_text(self.canvas_width - 30, self.axis_offset + 25, text="X", 
                               fill='#000000', font=('Arial', 14, 'bold'))
        self.canvas.create_text(self.axis_offset - 30, 25, text="Y", 
                               fill='#000000', font=('Arial', 14, 'bold'))
    
    def analyze_shape(self):
        if len(self.points) < 2:
            return
        
        sides = []
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
            sides.append(dist)
        
        info = f"Points: {len(self.points)} | Sides: {', '.join([f'{s:.0f}' for s in sides[:4]])}"
        
        if len(self.points) >= 3:
            perim = sum(sides)
            
            area = 0
            for i in range(len(self.points)):
                p1 = self.points[i]
                p2 = self.points[(i + 1) % len(self.points)]
                area += p1[0] * p2[1] - p2[0] * p1[1]
            area = abs(area) / 2
            
            info += f" | P={perim:.0f}px | A={area:.0f}px²"
        
        self.update_info(info)
    
    def analyze_finished_shape(self):
        """AI анализирует завершённую фигуру"""
        if len(self.points) < 3:
            return
        
        sides = []
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
            sides.append(dist)
        
        perim = sum(sides)
        area = 0
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            area += p1[0] * p2[1] - p2[0] * p1[1]
        area = abs(area) / 2
        
        # Определяем тип фигуры
        n = len(self.points)
        analysis = ""
        
        if n == 3:
            analysis += "📐 TRIANGLE\n\n"
            analysis += f"  Vertices: {n}\n"
            analysis += f"  Sides: {', '.join([f'{s:.1f}' for s in sides])}\n"
            analysis += f"  Perimeter: P = {perim:.1f}\n"
            analysis += f"  Area: A = {area:.1f}\n\n"
            analysis += "📖 FORMULAS:\n"
            analysis += f"  • Area: A = √[s(s-a)(s-b)(s-c)]\n"
            s = perim / 2
            analysis += f"    (s = {s:.1f}, semi-perimeter)\n"
            analysis += f"  • Perimeter: P = a + b + c\n"
            analysis += f"    = {' + '.join([f'{s:.1f}' for s in sides])}\n"
            analysis += f"    = {perim:.1f}\n\n"
            
            # Проверяем прямоугольный ли треугольник
            sides_sorted = sorted(sides)
            if abs(sides_sorted[0]**2 + sides_sorted[1]**2 - sides_sorted[2]**2) < 1:
                analysis += "✓ This is a RIGHT TRIANGLE!\n"
                analysis += f"  Pythagorean: {sides_sorted[0]:.1f}² + {sides_sorted[1]:.1f}² = {sides_sorted[2]:.1f}²\n"
        
        elif n == 4:
            # Проверяем квадрат/прямоугольник
            is_square = all(abs(s - sides[0]) < 0.1 for s in sides)
            is_rect = (abs(sides[0] - sides[2]) < 0.1 and abs(sides[1] - sides[3]) < 0.1)
            
            if is_square:
                analysis += "▢ SQUARE\n\n"
                analysis += f"  Side: a = {sides[0]:.1f}\n"
                analysis += f"  Perimeter: P = 4a = {perim:.1f}\n"
                analysis += f"  Area: A = a² = {area:.1f}\n\n"
                analysis += "📖 FORMULAS:\n"
                analysis += f"  • Area: A = a² = {sides[0]:.1f}² = {area:.1f}\n"
                analysis += f"  • Perimeter: P = 4a = 4 × {sides[0]:.1f} = {perim:.1f}\n"
                diag = sides[0] * math.sqrt(2)
                analysis += f"  • Diagonal: d = a√2 = {diag:.1f}\n"
            elif is_rect:
                analysis += "▭ RECTANGLE\n\n"
                a, b = sides[0], sides[1]
                analysis += f"  Length: a = {a:.1f}\n"
                analysis += f"  Width: b = {b:.1f}\n"
                analysis += f"  Perimeter: P = 2(a+b) = {perim:.1f}\n"
                analysis += f"  Area: A = a×b = {area:.1f}\n\n"
                analysis += "📖 FORMULAS:\n"
                analysis += f"  • Area: A = a × b = {a:.1f} × {b:.1f} = {area:.1f}\n"
                analysis += f"  • Perimeter: P = 2(a + b) = 2({a:.1f} + {b:.1f}) = {perim:.1f}\n"
                diag = math.sqrt(a**2 + b**2)
                analysis += f"  • Diagonal: d = √(a² + b²) = {diag:.1f}\n"
            else:
                analysis += "◈ QUADRILATERAL\n\n"
                analysis += f"  Vertices: {n}\n"
                analysis += f"  Sides: {', '.join([f'{s:.1f}' for s in sides])}\n"
                analysis += f"  Perimeter: P = {perim:.1f}\n"
                analysis += f"  Area: A = {area:.1f}\n"
        else:
            analysis += f"🔷 POLYGON ({n}-sided)\n\n"
            analysis += f"  Vertices: {n}\n"
            analysis += f"  Sides: {', '.join([f'{s:.1f}' for s in sides])}\n"
            analysis += f"  Perimeter: P = {perim:.1f}\n"
            analysis += f"  Area: A = {area:.1f}\n"
        
        analysis += "\n" + "─" * 40 + "\n"
        self.chat_print(analysis)
    
    def set_color(self, color):
        self.current_color = color
        self.redraw_canvas()
    
    def finish_shape(self):
        if len(self.points) >= 3:
            self.shape_finished = True
            self.analyze_shape()
            self.update_status("✓ Finished!")
            self.chat_print(">\n🎯 SHAPE ANALYSIS\n")
            self.analyze_finished_shape()
            
            # Сохраняем фигуру в список
            self.shapes.append((self.points.copy(), self.current_color, self.mode))
            self.selected_shape_idx = len(self.shapes) - 1
            
            # Диалог сохранения
            save = messagebox.askyesno("Save Shape", "Save this shape?")
            if save:
                self.save_data()
        else:
            messagebox.showwarning("Error", "Need 3+ points!")
    
    def select_shape_mode(self):
        """Выбрать фигуру из сохранённых"""
        if not self.shapes:
            messagebox.showwarning("Info", "No saved shapes yet!")
            return
        
        # Циклически переключаемся между фигурами
        if self.selected_shape_idx is None:
            self.selected_shape_idx = 0
        else:
            self.selected_shape_idx = (self.selected_shape_idx + 1) % len(self.shapes)
        
        pts, color, mode = self.shapes[self.selected_shape_idx]
        self.chat_print(f"\n🎯 Selected shape #{self.selected_shape_idx + 1}\n")
        self.update_status(f"Shape #{self.selected_shape_idx + 1}")
        self.redraw_canvas()
    
    def toggle_altitude(self):
        """Включить/выключить рисование высоты"""
        if len(self.points) < 3:
            messagebox.showwarning("Error", "Finish shape first!")
            return
        
        self.show_altitude = not self.show_altitude
        
        if self.show_altitude:
            # Выбираем вершину для высоты
            dialog = simpledialog.askinteger("Altitude", 
                f"Select vertex (1-{len(self.points)}):", 
                initialvalue=1)
            if dialog and 1 <= dialog <= len(self.points):
                self.altitude_vertex = dialog - 1
                self.chat_print(f"🏔️ Altitude from vertex {dialog}\n")
            else:
                self.show_altitude = False
                return
        else:
            self.altitude_vertex = None
            self.chat_print("🏔️ Altitude hidden\n")
        
        self.redraw_canvas()
    
    def draw_altitude(self):
        """Рисует высоту (перпендикуляр от вершины к противоположной стороне)"""
        if not self.points or self.altitude_vertex is None:
            return
        
        pts = self.points
        v = self.altitude_vertex
        
        # Для треугольника: высота из вершины v к противоположной стороне
        if len(pts) == 3:
            # Вершина
            px, py = pts[v]
            # Противоположная сторона
            a = pts[(v + 1) % 3]
            b = pts[(v + 2) % 3]
            
            # Проекция точки на линию ab
            ax, ay = a
            bx, by = b
            dx, dy = bx - ax, by - ay
            
            # Protection against degenerate geometry (identical points)
            denom = dx*dx + dy*dy
            if denom == 0:
                return
            
            t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / denom))
            foot_x = ax + t * dx
            foot_y = ay + t * dy
            
            # Рисуем высоту
            self.canvas.create_line(px, py, foot_x, foot_y, fill='#FF0000', width=2, dash=(2, 2))
            # Отмечаем основание высоты
            self.canvas.create_oval(foot_x - 5, foot_y - 5, foot_x + 5, foot_y + 5, 
                                   fill='#FF0000', outline='#FF0000', width=1)
            
            # Показываем длину высоты
            h = math.sqrt((px - foot_x)**2 + (py - foot_y)**2)
            mid_x, mid_y = (px + foot_x) / 2, (py + foot_y) / 2
            self.canvas.create_text(mid_x + 10, mid_y, text=f"h={h:.0f}", 
                                   fill='#FF0000', font=('Arial', 9, 'bold'))
    
    def toggle_diagonal(self):
        """Включить/выключить рисование диагонали"""
        if len(self.points) < 3:
            messagebox.showwarning("Error", "Finish shape first!")
            return
        
        self.show_diagonal = not self.show_diagonal
        
        if self.show_diagonal:
            self.chat_print(f"📍 Diagonals shown\n")
        else:
            self.chat_print(f"📍 Diagonals hidden\n")
        
        self.redraw_canvas()
    
    def draw_diagonals(self):
        """Рисует диагонали многоугольника"""
        if len(self.points) < 4:
            return
        
        # Для многоугольника рисуем все диагонали
        for i in range(len(self.points)):
            for j in range(i + 2, len(self.points)):
                if j - i != len(self.points) - 1:  # Не рисуем стороны
                    x1, y1 = self.points[i]
                    x2, y2 = self.points[j]
                    self.canvas.create_line(x1, y1, x2, y2, fill='#00FF00', width=1, dash=(3, 3))
                    
                    # Длина диагонали
                    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                    self.canvas.create_text(mid_x, mid_y - 10, text=f"d={d:.0f}", 
                                           fill='#00FF00', font=('Arial', 8))
    
    def rotate_shape(self):
        if len(self.points) < 3:
            messagebox.showwarning("Error", "Finish shape!")
            return
        
        angle = simpledialog.askinteger("Rotate", "Angle (deg):", initialvalue=45)
        if angle is None:
            return
        
        cx = sum(p[0] for p in self.points) / len(self.points)
        cy = sum(p[1] for p in self.points) / len(self.points)
        rad = math.radians(angle)
        
        new_points = []
        for x, y in self.points:
            nx = cx + (x - cx) * math.cos(rad) - (y - cy) * math.sin(rad)
            ny = cy + (x - cx) * math.sin(rad) + (y - cy) * math.cos(rad)
            new_points.append((nx, ny))
        
        self.points = new_points
        self.redraw_canvas()
        self.chat_print(f"> Rotated {angle}°\n")
    
    def move_shape(self):
        if not self.points:
            messagebox.showwarning("Error", "Draw first!")
            return
        
        dx = simpledialog.askinteger("Move", "X offset:", initialvalue=20)
        if dx is None:
            return
        dy = simpledialog.askinteger("Move", "Y offset:", initialvalue=20)
        if dy is None:
            return
        
        self.points = [(x + dx, y + dy) for x, y in self.points]
        if self.circle_center:
            self.circle_center = (self.circle_center[0] + dx, self.circle_center[1] + dy)
        
        self.redraw_canvas()
        self.chat_print(f"> Moved ({dx},{dy})\n")
    
    def mirror_horizontal(self):
        """Зеркалирование относительно горизонтальной оси"""
        if len(self.points) < 3:
            messagebox.showwarning("Error", "Finish shape first!")
            return
        
        cy = sum(p[1] for p in self.points) / len(self.points)
        self.points = [(x, 2*cy - y) for x, y in self.points]
        self.points.reverse()
        self.redraw_canvas()
        self.chat_print("> Mirrored Horizontal\n")
    
    def mirror_vertical(self):
        """Зеркалирование относительно вертикальной оси"""
        if len(self.points) < 3:
            messagebox.showwarning("Error", "Finish shape first!")
            return
        
        cx = sum(p[0] for p in self.points) / len(self.points)
        self.points = [(2*cx - x, y) for x, y in self.points]
        self.points.reverse()
        self.redraw_canvas()
        self.chat_print("> Mirrored Vertical\n")
    
    def scale_shape(self):
        """Масштабирование фигуры"""
        if len(self.points) < 3:
            messagebox.showwarning("Error", "Finish shape first!")
            return
        
        scale = simpledialog.askfloat("Scale", "Scale factor (1.5):", initialvalue=1.5)
        if scale is None or scale <= 0:
            return
        
        cx = sum(p[0] for p in self.points) / len(self.points)
        cy = sum(p[1] for p in self.points) / len(self.points)
        
        self.points = [(cx + (x - cx) * scale, cy + (y - cy) * scale) for x, y in self.points]
        self.redraw_canvas()
        self.chat_print(f"> Scaled {scale}x\n")
    
    def undo(self):
        if self.history:
            self.points, self.circle_center = self.history.pop()
            self.redraw_canvas()
            self.chat_print("> Undo\n")
    
    def clear_all(self):
        self.points = []
        self.circle_center = None
        self.midpoints = []
        self.shape_finished = False
        self.drag_mode = False
        self.midpoint_mode = False
        self.history = []
        self.shapes = []  # Очищаем сохранённые фигуры
        self.selected_shape_idx = None
        self.show_altitude = False
        self.show_diagonal = False
        self.redraw_canvas()
        self.update_info("Ready")
        self.update_status("Ready")
        self.chat_print("> New\n")
    
    def analyze_formula(self):
        formula = self.formula_input.get().strip()
        if not formula:
            return
        
        self.chat_print(f"\n📝 Вы: {formula}\n")
        self.chat_print("-" * 40 + "\n")
        
        response = ""
        formula_lower = formula.lower()
        
        # Определяем тип формулы/задачи
        if any(x in formula_lower for x in ['площадь', 'area', 'a =']):
            response += "📖 ФОРМУЛА ПЛОЩАДИ:\n"
            if any(x in formula_lower for x in ['круг', 'circle', 'π']):
                response += "  • Формула: A = π × r²\n"
                response += "  • Где: r - радиус\n"
                response += "  • π ≈ 3.14159\n"
                response += "\n  Пример: если r = 5\n"
                response += "  A = 3.14 × 25 ≈ 78.5 кв.ед\n"
            elif any(x in formula_lower for x in ['прямоугольник', 'rectangle']):
                response += "  • Формула: A = длина × ширина\n"
                response += "  • Пример: длина=10, ширина=5\n"
                response += "  • A = 10 × 5 = 50 кв.ед\n"
            elif any(x in formula_lower for x in ['треугольник', 'triangle']):
                response += "  • Формула: A = (основание × высота) / 2\n"
                response += "  • Пример: основание=10, высота=6\n"
                response += "  • A = (10 × 6) / 2 = 30 кв.ед\n"
            else:
                response += "  • Укажите тип фигуры (круг, прямоугольник, треугольник)\n"
                response += "  • Или введите конкретные значения\n"
        
        elif any(x in formula_lower for x in ['периметр', 'perimeter', 'p =']):
            response += "📖 ФОРМУЛА ПЕРИМЕТРА:\n"
            if any(x in formula_lower for x in ['круг', 'circle']):
                response += "  • Формула: P = 2πr\n"
                response += "  • Где: r - радиус\n"
            elif any(x in formula_lower for x in ['прямоугольник', 'rectangle']):
                response += "  • Формула: P = 2(a + b)\n"
                response += "  • Где: a, b - длины сторон\n"
            else:
                response += "  • Периметр = сумма всех сторон\n"
        
        elif 'пифагор' in formula_lower or 'a^2' in formula or 'a²' in formula:
            response += "📖 ТЕОРЕМА ПИФАГОРА:\n"
            response += "  • Формула: c² = a² + b²\n"
            response += "  • Где: c - гипотенуза (длинная сторона)\n"
            response += "  • a, b - катеты (короткие стороны)\n"
            response += "\n  Пример: a=3, b=4\n"
            response += "  c² = 9 + 16 = 25\n"
            response += "  c = 5\n"
        
        elif any(x in formula_lower for x in ['диагональ', 'diagonal']):
            response += "📖 ФОРМУЛА ДИАГОНАЛИ:\n"
            response += "  • Формула: d = √(a² + b²)\n"
            response += "  • Где: a, b - стороны прямоугольника\n"
            response += "  • Это применение теоремы Пифагора\n"
        
        elif any(x in formula_lower for x in ['угол', 'angle', 'sin', 'cos', 'tan']):
            response += "📖 ТРИГОНОМЕТРИЯ:\n"
            response += "  • sin(x) = противолежащий / гипотенуза\n"
            response += "  • cos(x) = прилежащий / гипотенуза\n"
            response += "  • tan(x) = противолежащий / прилежащий\n"
            response += "\n  Используется в прямоугольных треугольниках\n"
        
        else:
            response += "💡 РЕКОМЕНДАЦИИ:\n"
            response += "  • Введите формулу (например: A = π r²)\n"
            response += "  • Или спросите о расчёте (например: найти площадь круга)\n"
            response += "  • Приведите числовые значения для вычисления\n"
            response += "\n  Доступные типы задач:\n"
            response += "  - Площадь (круг, треугольник, прямоугольник)\n"
            response += "  - Периметр/Длина окружности\n"
            response += "  - Теорема Пифагора\n"
            response += "  - Диагональ\n"
            response += "  - Тригонометрия\n"
        
        self.chat_print(response)
        self.chat_print("\n" + "-" * 40 + "\n")
        self.formula_input.delete(0, tk.END)
    
    def chat_print(self, text):
        self.chat.config(state=tk.NORMAL)
        self.chat.insert(tk.END, text)
        self.chat.see(tk.END)
        self.chat.config(state=tk.DISABLED)
    
    def update_info(self, text):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)
        self.info_text.config(state=tk.DISABLED)
    
    def update_status(self, msg):
        self.status_label.config(text=msg)
    
    def save_data(self):
        if not self.points:
            messagebox.showwarning("Warning", "Nothing to save!")
            return
        
        filename = f"shape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(f"/Users/olekzhyrko/Desktop/geometry flyer/{filename}", "w") as f:
                f.write("GEOMETRY STUDIO - DATA\n")
                f.write("═════════════════════\n\n")
                f.write(f"Type: {self.mode}\n")
                f.write(f"Points: {len(self.points)}\n\n")
                
                for i, p in enumerate(self.points, 1):
                    rx, ry = self.canvas_to_real(p[0], p[1])
                    f.write(f"P{i}: ({rx:.1f}, {ry:.1f})\n")
            
            messagebox.showinfo("Saved", "✓ OK!")
            self.chat_print(f"> Saved {filename}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = GeometryStudio(root)
    root.mainloop()

if __name__ == "__main__":
    main()
