# ==============================================================================
#           MYSTIC GLASSMORPHIC CLOCK WIDGET & SCREEN SAVER
# ==============================================================================
# A premium, interactive desktop widget built on Dark Glassmorphism principles.
# Designed with concentric glowing starlight tracks, frosted glass overlays,
# and fine technical blueprint gridlines. No hands, purely stellar-kinetic.
# ==============================================================================

import tkinter as tk
import math
import time
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw, ImageFilter

class GlassmorphicClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chronos Pillar: Mystical HMI Clock Widget")
        
        # Widescreen 16:9 standard window or full-screen screensaver capability
        self.width = 1024
        self.height = 576
        
        # Center on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.resizable(True, True)
        self.root.configure(bg="#0f1012")
        
        # Interactive full-screen toggler via double click or 'F11'
        self.is_fullscreen = False
        self.root.bind("<Double-Button-1>", self.toggle_fullscreen)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        
        # Initialize Canvas
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg="#0f1012")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Design Constants (Grounded in HMI & Orizon Glassmorphic Playbook)
        self.COLOR_BG_START = (30, 32, 38)     # Slate Grey-Blue
        self.COLOR_BG_END = (10, 11, 13)       # Deep Charcoal Sump
        self.COLOR_GLASS_FILL = (45, 49, 58, 100) # 40% opaque frosted grey
        self.COLOR_GLOW_WHITE = (255, 255, 255, 120) # 50% opaque sheen
        
        self.NEON_CYAN = "#00f0ff"    # Seconds Arc
        self.NEON_MAGENTA = "#ff007f" # Minutes Arc
        self.NEON_GREEN = "#39ff14"   # Hours Arc
        self.TEXT_BUTTERCREAM = "#f8f5ee"
        self.TEXT_SLATE = "#96a0af"
        self.CORP_RED = "#d32f2f"
        
        # Physics rotation angles for backing mechanics
        self.angle_offset = 0.0
        
        # Force initial draw
        self.root.update()
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        
        self.root.bind("<Configure>", self.on_resize)
        self.update_clock()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def exit_fullscreen(self, event=None):
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes("-fullscreen", False)
        return "break"

    def on_resize(self, event):
        # Prevent math division errors on minimizes
        if event.width > 10 and event.height > 10:
            self.width = event.width
            self.height = event.height

    def draw_glass_panel(self, draw, cx, cy, radius, blur_radius=20):
        """
        Generates realistic background frosted glass with shadow, border sheen, and depth.
        """
        # 1. Subtle Outer Drop Shadow (Simulating ambient depth elevation)
        shadow_padding = 15
        shadow_img = Image.new("RGBA", (radius * 2 + shadow_padding * 2, radius * 2 + shadow_padding * 2), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow_img)
        s_draw.ellipse(
            [shadow_padding, shadow_padding, shadow_padding + radius * 2, shadow_padding + radius * 2], 
            fill=(0, 0, 0, 160)
        )
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(10))
        
        # Paste shadow onto canvas image first
        self.base_image.paste(shadow_img, (cx - radius - shadow_padding, cy - radius - shadow_padding), shadow_img)
        
        # 2. Main Frosted Glass Base Shape
        glass_overlay = Image.new("RGBA", (radius * 2, radius * 2), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(glass_overlay)
        g_draw.ellipse([0, 0, radius * 2, radius * 2], fill=self.COLOR_GLASS_FILL)
        
        # 3. Fine glowing edge border sheen (simulates light diffraction on edges)
        border_width = 2
        g_draw.ellipse([border_width, border_width, radius * 2 - border_width, radius * 2 - border_width], 
                       outline=self.COLOR_GLOW_WHITE, width=1)
        
        # Apply slight blur to glass to simulate scattering
        glass_overlay = glass_overlay.filter(ImageFilter.GaussianBlur(1))
        
        # Composite glass onto background
        self.base_image.paste(glass_overlay, (cx - radius, cy - radius), glass_overlay)

    def draw_blueprint_lines(self, draw):
        """
        Renders a beautiful technical blueprint grid with diagonal focal vectors.
        """
        grid_size = 40
        # Draw horizontal and vertical fine gridlines
        for x in range(0, self.width, grid_size):
            draw.line([(x, 0), (x, self.height)], fill=(255, 255, 255, 8), width=1)
        for y in range(0, self.height, grid_size):
            draw.line([(0, y), (self.width, y)], fill=(255, 255, 255, 8), width=1)
            
        # Draw central structural crosshairs
        cx, cy = self.width // 2, self.height // 2
        draw.line([(cx, 0), (cx, self.height)], fill=(255, 255, 255, 15), width=1)
        draw.line([(0, cy), (self.width, cy)], fill=(255, 255, 255, 15), width=1)
        
        # Large decorative geometric calibration rings
        draw.ellipse([cx - 300, cy - 300, cx + 300, cy + 300], outline=(255, 255, 255, 12), width=1)
        draw.ellipse([cx - 180, cy - 180, cx + 180, cy + 180], outline=(255, 255, 255, 8), width=1)

    def update_clock(self):
        # 1. Re-initialize raw canvas image frame
        self.base_image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.base_image)
        
        # 2. Draw Smooth Radial Background Gradient
        cx, cy = self.width // 2, self.height // 2
        max_dist = math.sqrt(cx**2 + cy**2)
        for r in range(0, int(max_dist), 4):
            factor = min(1.0, r / max_dist)
            # Interpolate background color layers
            r_c = int(self.COLOR_BG_START[0] * (1 - factor) + self.COLOR_BG_END[0] * factor)
            g_c = int(self.COLOR_BG_START[1] * (1 - factor) + self.COLOR_BG_END[1] * factor)
            b_c = int(self.COLOR_BG_START[2] * (1 - factor) + self.COLOR_BG_END[2] * factor)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(r_c, g_c, b_c, 255), width=4)
            
        # 3. Add Blueprint aesthetics
        self.draw_blueprint_lines(draw)
        
        # 4. Render main frosted glass cockpit dial
        clock_radius = min(self.width, self.height) // 3
        self.draw_glass_panel(draw, cx, cy, clock_radius)
        
        # 5. Extract system time parameters
        now = datetime.now()
        hours = now.hour % 12
        minutes = now.minute
        seconds = now.second
        microseconds = now.microsecond
        
        # Calculate real-time smooth float parameters
        sec_float = seconds + microseconds / 1000000.0
        min_float = minutes + sec_float / 60.0
        hour_float = hours + min_float / 12.0
        
        # Shifting offsets for celestial rotation tracking (behind dials)
        self.angle_offset += 0.005
        
        # Convert image to TK frame
        self.tk_image = ImageTk.PhotoImage(self.base_image)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)
        
        # 6. Draw Concentric Neon Activity Tracks (conforming to hands-free tower aesthetic)
        # Tkinter native canvas is superior at drawing anti-aliased arcs with custom widths
        # Seconds track (Outer Neon Cyan)
        sec_angle = (sec_float / 60.0) * 360 - 90
        self.draw_glowing_arc(cx, cy, clock_radius - 20, -90, sec_angle, self.NEON_CYAN, 4)
        
        # Minutes track (Middle Neon Magenta)
        min_angle = (min_float / 60.0) * 360 - 90
        self.draw_glowing_arc(cx, cy, clock_radius - 40, -90, min_angle, self.NEON_MAGENTA, 6)
        
        # Hours track (Inner Neon Green)
        hour_angle = (hour_float / 12.0) * 360 - 90
        self.draw_glowing_arc(cx, cy, clock_radius - 60, -90, hour_angle, self.NEON_GREEN, 8)
        
        # 7. Draw rotating orbital star-beacons instead of hands
        self.draw_orbital_node(cx, cy, clock_radius - 20, sec_angle, self.NEON_CYAN, 6)
        self.draw_orbital_node(cx, cy, clock_radius - 40, min_angle, self.NEON_MAGENTA, 8)
        self.draw_orbital_node(cx, cy, clock_radius - 60, hour_angle, self.NEON_GREEN, 10)
        
        # 8. Render Center Glass Hub Core
        self.canvas.create_oval(cx - 30, cy - 30, cx + 30, cy + 30, fill="#1c1f26", outline="#ffffff", width=1)
        self.canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill=self.NEON_CYAN, outline="")
        
        # 9. Render digital clock readout inside the hub (using buttercream technical text)
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%A, %d %B %Y").upper()
        
        # Place digital panel above the hub for clear Orizon UX hierarchy
        self.canvas.create_text(cx, cy + (clock_radius // 2), text=time_str, 
                                font=("Trebuchet MS", 28, "bold"), fill=self.TEXT_BUTTERCREAM)
        self.canvas.create_text(cx, cy + (clock_radius // 2) + 28, text=date_str, 
                                font=("Calibri", 10, "bold"), fill=self.TEXT_SLATE, letterspacing=2)
        
        # Brand alignment details on background (RED NK, RED ITI)
        self.draw_branding_elements(cx, cy, clock_radius)
        
        # Refresh screen every 50ms for hyper-smooth fluid performance
        self.root.after(50, self.update_clock)

    def draw_glowing_arc(self, cx, cy, r, start_ang, end_angle, color, width):
        # Draw background dim track (simulating glass-recess channel)
        self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=start_ang, extent=-(end_angle - start_ang),
                               style=tk.ARC, outline="#1a1c22", width=width + 2)
                               
        # Draw neon bright track
        self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=start_ang, extent=-(end_angle - start_ang),
                               style=tk.ARC, outline=color, width=width)

    def draw_orbital_node(self, cx, cy, r, angle, color, size):
        rad = math.radians(angle)
        nx = cx + r * math.cos(rad)
        ny = cy + r * math.sin(rad)
        # Glowing shadow aura around node
        self.canvas.create_oval(nx - size - 4, ny - size - 4, nx + size + 4, ny + size + 4, fill="", outline=color, width=1)
        self.canvas.create_oval(nx - size, ny - size, nx + size, ny + size, fill=color, outline="#ffffff", width=1)

    def draw_branding_elements(self, cx, cy, clock_radius):
        # Top branding header
        self.canvas.create_text(self.width // 2, 40, text="C H R O N O S   P I L L A R", 
                                font=("Trebuchet MS", 14, "bold"), fill=self.TEXT_BUTTERCREAM)
        self.canvas.create_text(self.width // 2, 60, text="NK HIGH-PRESSURE STARTING SYSTEMS", 
                                font=("Calibri", 9, "bold"), fill=self.TEXT_SLATE)
                                
        # Bottom left: PT ITI
        self.canvas.create_text(80, self.height - 40, text="PT. ITI MARINE & OILFIELD Utama", 
                                font=("Trebuchet MS", 10, "bold"), fill=self.TEXT_SLATE, anchor=tk.W)
        # Highlight "ITI" in red run
        self.canvas.create_text(101, self.height - 40, text="ITI", 
                                font=("Trebuchet MS", 10, "bold"), fill=self.CORP_RED, anchor=tk.W)
                                
        # Bottom right: NK Germany logo
        self.canvas.create_text(self.width - 120, self.height - 40, text="NK", 
                                font=("Arial", 14, "bold"), fill=self.CORP_RED, anchor=tk.E)
        self.canvas.create_text(self.width - 115, self.height - 40, text="Neuenhauser Starting Air Systems", 
                                font=("Trebuchet MS", 10, "bold"), fill=self.TEXT_SLATE, anchor=tk.W)

if __name__ == "__main__":
    root = tk.Tk()
    app = GlassmorphicClockApp(root)
    root.mainloop()
