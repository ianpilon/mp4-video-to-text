import os
from tkinter import *
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip

class MP4ToMP3Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("MP4 to MP3 Converter")
        self.root.geometry("400x200")
        
        # Create main frame
        self.main_frame = Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill='both')
        
        # Create and pack widgets
        Label(self.main_frame, text="MP4 to MP3 Converter", font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.select_button = Button(self.main_frame, text="Select MP4 File", command=self.select_file)
        self.select_button.pack(pady=10)
        
        self.status_label = Label(self.main_frame, text="No file selected", wraplength=350)
        self.status_label.pack(pady=10)

    def select_file(self):
        # Open file dialog for MP4 files
        file_path = filedialog.askopenfilename(
            title="Select MP4 File",
            filetypes=[("MP4 files", "*.mp4")]
        )
        
        if file_path:
            self.status_label.config(text="Converting...")
            self.root.update()
            
            try:
                # Get the output path
                output_path = os.path.splitext(file_path)[0] + '.mp3'
                
                # Convert video to audio
                video = VideoFileClip(file_path)
                video.audio.write_audiofile(output_path)
                video.close()
                
                self.status_label.config(text=f"Successfully converted!\nSaved to: {output_path}")
                messagebox.showinfo("Success", "Conversion completed successfully!")
                
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = Tk()
    app = MP4ToMP3Converter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
