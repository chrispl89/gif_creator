import glob
import cv2
from PIL import Image


class Gif:
    # create the directory with the same name as the one below
    TEMP_DIR = 'tmp/'

    def __init__(self, path: str):
        self.movie = cv2.VideoCapture(path)

    def read_frame(self, time: int):
        self.movie.set(cv2.CAP_PROP_POS_MSEC, time)
        return self.movie.read()

    def _get_frames(self, fps):
        time = 1
        success, frame = self.read_frame(time)

        while success:
            cv2.imwrite(f'{Gif.TEMP_DIR}{time}.jpg', frame)
            success, frame = self.read_frame(time / fps * 1000)
            time += 1

    def save(self, target: str, fps):
        self._get_frames(fps)
        # for this moment we have some files saved as .jpg files
        # below is the code responsible to change jpg files to gif
        images = glob.glob(f'{Gif.TEMP_DIR}*.jpg')
        frames = [Image.open(image) for image in images]
        frames[0].save(
            target,
            format='GIF',
            append_images=frames,
            save_all=True,
            # you can change duration and loop to get more reliable gif
            duration=300,
            loop=5
        )


# The source file. Important! The file must be in the same folder as program
gif = Gif('YOUR_FILE')

# number below defines how many fps you want to capture to save the files
gif.save('movie.gif', 10)
