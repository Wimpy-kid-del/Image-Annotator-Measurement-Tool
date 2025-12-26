import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

image = None
clone = None
drawing = False
start_point = None
current_tool = None

def mouse_events(event, x, y, flags, param):
    global drawing, start_point, image

    if current_tool in ["rectangle", "line", "circle", "measure"]:
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            start_point = (x, y)

        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            temp = image.copy()
            if current_tool == "rectangle":
                cv2.rectangle(temp, start_point, (x, y), (0, 255, 0), 2)
            elif current_tool in ["line", "measure"]:
                cv2.line(temp, start_point, (x, y), (255, 0, 0), 2)
            elif current_tool == "circle":
                radius = int(np.linalg.norm(np.array(start_point) - np.array((x, y))))
                cv2.circle(temp, start_point, radius, (0, 0, 255), 2)
            cv2.imshow("Image Annotator", temp)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            if current_tool == "rectangle":
                cv2.rectangle(image, start_point, (x, y), (0, 255, 0), 2)
            elif current_tool == "line":
                cv2.line(image, start_point, (x, y), (255, 0, 0), 2)
            elif current_tool == "circle":
                radius = int(np.linalg.norm(np.array(start_point) - np.array((x, y))))
                cv2.circle(image, start_point, radius, (0, 0, 255), 2)
            elif current_tool == "measure":
                distance = int(np.linalg.norm(np.array(start_point) - np.array((x, y))))
                cv2.line(image, start_point, (x, y), (255, 0, 0), 2)
                mid = ((start_point[0] + x) // 2, (start_point[1] + y) // 2)
                cv2.putText(image, f"{distance}px", mid,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.imshow("Image Annotator", image)

    elif current_tool == "text":
        if event == cv2.EVENT_LBUTTONDOWN:
            text = simpledialog.askstring("Add Text", "Enter text:")
            if text:
                cv2.putText(image, text, (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                cv2.imshow("Image Annotator", image)

def load_image():
    global image, clone
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if path:
        image = cv2.imread(path)
        clone = image.copy()
        cv2.namedWindow("Image Annotator")
        cv2.setMouseCallback("Image Annotator", mouse_events)
        cv2.imshow("Image Annotator", image)

def save_image():
    if image is None:
        messagebox.showerror("Error", "No image to save.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".png",
                                        filetypes=[("PNG Files", "*.png"),
                                                   ("JPG Files", "*.jpg")])
    if path:
        cv2.imwrite(path, image)
        messagebox.showinfo("Saved", "Image saved successfully.")

def set_tool(tool):
    global current_tool
    current_tool = tool

root = tk.Tk()
root.title("Image Annotator & Measurement Tool")

tk.Button(root, text="Load Image", width=20, command=load_image).pack(pady=2)
tk.Button(root, text="Draw Rectangle", width=20, command=lambda: set_tool("rectangle")).pack(pady=2)
tk.Button(root, text="Draw Line", width=20, command=lambda: set_tool("line")).pack(pady=2)
tk.Button(root, text="Draw Circle", width=20, command=lambda: set_tool("circle")).pack(pady=2)
tk.Button(root, text="Add Text", width=20, command=lambda: set_tool("text")).pack(pady=2)
tk.Button(root, text="Measure Distance", width=20, command=lambda: set_tool("measure")).pack(pady=2)
tk.Button(root, text="Save Image", width=20, command=save_image).pack(pady=10)

root.mainloop()
cv2.destroyAllWindows()
