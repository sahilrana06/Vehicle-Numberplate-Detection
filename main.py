import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from number_plate import extract_num

def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp():
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:

            print("Escape hit, closing...")
            break
        elif k % 256 == 32:

            if not os.path.isdir('temp'):
                os.mkdir('temp')

            img_name = "./temp/test_img1.png"

            print('imwrite=', cv2.imwrite(filename=img_name, img=frame))
            print("{} written!".format(img_name))

    cam.release()
    cv2.destroyAllWindows()
    return True


def captureImage(ent):

    filename = os.getcwd() + '\\temp\\test_img1.png'

    res = None
    res = messagebox.askquestion(
        'Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp()
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
    return True

def check(window, path1):
    result = extract_num(path1)
    if result is None:
        messagebox.showerror("Failure", "Unable to extract number!")
        return False

    result1, result2 = result
    if result2 == '':
        messagebox.showerror("Failure", "State not recognized!!")
        return False

    messagebox.showinfo("Success", f"Number: {result1}\n\nCar belongs to {result2}")
    return True


root = tk.Tk()
root.title("Number detection")
root.geometry("500x700")
uname_label = tk.Label(root, text="Number plate detection:", font=10)  # type: ignore
uname_label.place(x=90, y=50)

img1_message = tk.Label(root, text="Insert image", font=10)  # type: ignore
img1_message.place(x=10, y=120)

image1_path_entry = tk.Entry(root, font=10)  # type: ignore
image1_path_entry.place(x=150, y=120)

img1_capture_button = tk.Button(
    root, text="Capture", font=10, command=lambda: captureImage(ent=image1_path_entry))  # type: ignore
img1_capture_button.place(x=400, y=90)

img1_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image1_path_entry))  # type: ignore
img1_browse_button.place(x=400, y=140)


compare_button = tk.Button(
    root, text="Recognize", font=10, command=lambda: check(window=root,  # type: ignore
                                                                   path1=image1_path_entry.get(), ))

compare_button.place(x=200, y=320)
root.mainloop()
