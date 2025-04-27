import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
from PIL.Image import Resampling
import os
class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes Moderno")
        self.root.geometry("700x600")
        self.root.configure(bg='#2e2e2e')
        self.image = None
        self.history = []
        self.setup_ui()
    def setup_ui(self):
        toolbar = tk.Frame(self.root, bg='#1e1e1e', pady=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.buttons = {}
        actions = [
            ("Abrir", self.open_image, "icons/open.png", "Abrir Imagen"),
            ("Guardar", self.save_image, "icons/save.png", "Guardar Imagen"),
            ("Deshacer", self.undo, "icons/undo.png", "Deshacer Cambios"),
            ("Trasladar", self.translate_image, "icons/move.png", "Trasladar Imagen"),
            ("Rotar", self.rotate_image, "icons/rotate.png", "Rotar Imagen"),
            ("Redimensionar", self.resize_image, "icons/resize.png", "Redimensionar Imagen"),
            ("Reflejar", self.reflect_image, "icons/mirror.png", "Reflejar Imagen"),
            ("Recortar", self.crop_image, "icons/cut.png", "Recortar Imagen"),
            ("Ecualizar", self.equalize_image, "icons/equalize.png", "Ecualizar Imagen"),
            ("Suavizar", self.smooth_image, "icons/blur.png", "Suavizar Imagen")
        ]
        for (name, command, icon_path, tooltip) in actions:
            img = Image.open(icon_path).resize((32,32), Resampling.LANCZOS)
            icon = ImageTk.PhotoImage(img)
            btn = tk.Button(toolbar, image=icon, command=command, bg='#1e1e1e', bd=0, highlightthickness=0)
            btn.image = icon
            btn.pack(side=tk.LEFT, padx=4)
            self.buttons[name] = btn
            self.add_tooltip(btn, tooltip)
        self.canvas = tk.Label(self.root, bg="#2e2e2e")
        self.canvas.pack(expand=True)
    def add_tooltip(self, widget, text):
        tooltip = tk.Label(self.root, text=text, bg="#f0f0f0", font=("Arial", 10), relief="solid", bd=1, padx=5, pady=2)
        def show_tooltip(event):
            x = widget.winfo_rootx()
            y = widget.winfo_rooty()
            tooltip.place(x=x - widget.winfo_width(),
                        y=widget.winfo_height() + 6)
        def hide_tooltip(event):
            tooltip.place_forget()
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            img = Image.open(file_path).convert("RGB")
            img.thumbnail((500, 500), Resampling.LANCZOS)
            self.image = img
            self.history.clear()
            self.update_canvas()
    def save_image(self):
        if self.image:
            path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if path:
                self.image.save(path)
    def undo(self):
        if self.history:
            self.image = self.history.pop()
            self.update_canvas()
    def add_history(self):
        if self.image:
            self.history.append(self.image.copy())
    def translate_image(self):
        if self.image:
            x_offset = simpledialog.askinteger("Traslación", "Desp X (max 500px):", minvalue=-500, maxvalue=500)
            y_offset = simpledialog.askinteger("Traslación", "Desp Y (max 500px):", minvalue=-500, maxvalue=500)
            if x_offset is not None and y_offset is not None:
                self.add_history()
                new_img = Image.new("RGB", self.image.size, (0, 0, 0))
                new_img.paste(self.image, (x_offset, y_offset))
                self.image = new_img
                self.update_canvas()
    def rotate_image(self):
        if self.image:
            angle = simpledialog.askinteger("Rotación", "Ángulo de Rotación (en grados):", minvalue=-360, maxvalue=360)
            if angle is not None:
                self.add_history()
                self.image = self.image.rotate(angle, expand=True)
                self.update_canvas()
    def resize_image(self):
        if self.image:
            width = simpledialog.askinteger("Redimensionar", "Nuevo Ancho (en píxeles):", minvalue=1)
            height = simpledialog.askinteger("Redimensionar", "Nuevo Alto (en píxeles):", minvalue=1)
            if width is not None and height is not None:
                self.add_history()
                self.image = self.image.resize((width, height), Resampling.LANCZOS)
                self.update_canvas()
    def reflect_image(self):
        if self.image:
            self.add_history()
            self.image = ImageOps.mirror(self.image)
            self.update_canvas()
    def crop_image(self):
        if self.image:
            w, h = self.image.size
            x1 = simpledialog.askinteger("Recorte", "Coordenada X1 (izquierda):", minvalue=0, maxvalue=w)
            y1 = simpledialog.askinteger("Recorte", "Coordenada Y1 (arriba):", minvalue=0, maxvalue=h)
            x2 = simpledialog.askinteger("Recorte", "Coordenada X2 (derecha):", minvalue=0, maxvalue=w)
            y2 = simpledialog.askinteger("Recorte", "Coordenada Y2 (abajo):", minvalue=0, maxvalue=h)
            if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
                self.add_history()
                self.image = self.image.crop((x1, y1, x2, y2))
                self.update_canvas()
    def equalize_image(self):
        if self.image:
            self.add_history()
            r, g, b = self.image.split()
            r = ImageOps.equalize(r)
            g = ImageOps.equalize(g)
            b = ImageOps.equalize(b)
            self.image = Image.merge("RGB", (r, g, b))
            self.update_canvas()
    def smooth_image(self):
        if self.image:
            def apply_smoothing(method):
                self.add_history()
                if method == "Promedio":
                    self.image = self.image.filter(ImageFilter.BoxBlur(2))
                elif method == "Gaussiano":
                    self.image = self.image.filter(ImageFilter.GaussianBlur(radius=2))
                elif method == "Mediana":
                    self.image = self.image.filter(ImageFilter.MedianFilter(size=3))
                elif method == "Bilateral":
                    self.image = self.image.filter(ImageFilter.GaussianBlur(radius=2))
                else:
                    messagebox.showerror("Error", "Método no válido.")
                self.update_canvas()
            top = tk.Toplevel(self.root)
            top.title("Seleccionar Método de Suavizado")
            top.geometry("350x110")
            frame = tk.Frame(top)
            frame.pack(pady=5)
            methods = ["Promedio", "Gaussiano", "Mediana", "Bilateral"]
            method_menu = ttk.Combobox(frame, values=methods, state="readonly", width=15)
            method_menu.set("Promedio")
            method_menu.pack(side=tk.LEFT, padx=5)
            apply_btn = tk.Button(frame, text="Aplicar", command=lambda: apply_smoothing(method_menu.get()))
            apply_btn.pack(side=tk.LEFT, padx=5)
    def update_canvas(self):
        if self.image:
            img = self.image.copy()
            img.thumbnail((500, 500), Resampling.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.configure(image=self.tk_img)
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
