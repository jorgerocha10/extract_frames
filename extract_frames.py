import cv2
import os
import threading
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, IntVar
from tkinter.ttk import Progressbar  # Corrected import for Progressbar


class FrameExtractorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Frame Extractor")

        self.label_video_path = Label(master, text="Video Path:")
        self.label_video_path.grid(row=0, column=0)

        self.entry_video_path = Entry(master, width=50)
        self.entry_video_path.grid(row=0, column=1)

        self.button_browse_video = Button(master, text="Browse", command=self.browse_video)
        self.button_browse_video.grid(row=0, column=2)

        self.label_output_folder = Label(master, text="Output Folder:")
        self.label_output_folder.grid(row=1, column=0)

        self.entry_output_folder = Entry(master, width=50)
        self.entry_output_folder.grid(row=1, column=1)

        self.button_browse_folder = Button(master, text="Browse", command=self.browse_folder)
        self.button_browse_folder.grid(row=1, column=2)

        self.extract_button = Button(master, text="Extract Frames", command=self.start_extraction)
        self.extract_button.grid(row=2, column=1)

        self.progress = IntVar()
        self.progress_bar = Progressbar(master, orient="horizontal", length=300, mode="determinate", variable=self.progress)
        self.progress_bar.grid(row=3, column=0, columnspan=3, pady=10)

    def browse_video(self):
        self.entry_video_path.delete(0, "end")
        file_path = filedialog.askopenfilename()
        if file_path:
            self.entry_video_path.insert(0, file_path)

    def browse_folder(self):
        self.entry_output_folder.delete(0, "end")
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.entry_output_folder.insert(0, folder_path)

    def start_extraction(self):
        video_path = self.entry_video_path.get()
        output_folder = self.entry_output_folder.get()
        if not video_path or not output_folder:
            messagebox.showwarning("Warning", "Please select a video file and output folder.")
            return
        threading.Thread(target=self.extract_frames, args=(video_path, output_folder), daemon=True).start()

    def extract_frames(self, video_path, output_folder):
        video = cv2.VideoCapture(video_path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps
        interval = duration / 72
        current_frame = 0
        frame_id = 0

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        self.progress.set(0)

        while True:
            video.set(cv2.CAP_PROP_POS_FRAMES, round(current_frame))
            success, frame = video.read()
            if not success or frame_id >= 72:
                break

            output_path = os.path.join(output_folder, f"frame_{frame_id+1:03}.jpg")
            cv2.imwrite(output_path, frame)
            current_frame += interval * fps
            frame_id += 1
            self.progress.set(int((frame_id / 72) * 100))
            self.master.update_idletasks()

        video.release()
        messagebox.showinfo("Done", "All frames have been saved successfully!")

def main():
    root = Tk()
    gui = FrameExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
