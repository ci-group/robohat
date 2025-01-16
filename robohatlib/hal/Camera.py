from __future__ import annotations

try:
    import subprocess
    import time as tm
    import numpy.typing

except ImportError:
    raise ImportError("Failed to import subprocess or time for the Camera class, make sure picamera2 is installed")

try:
    from picamera2 import Picamera2, Preview

except ImportError:
    raise ImportError("Failed to import needed dependencies for the Camera class, make sure picamera2 is installed")

from numpy.typing import NDArray
    # --------------------------------------------------------------------------------------

class Camera:
    def __init__(self, cam_res: tuple[int, int] = (160, 120)):
        """!
        Constructor of the Camera class
        """
        self.__picam2 = None
        self.__cam_is_not_available = False

        if self.__check_ffmpeg() is False:
            print("No FFMpeg found. Camera can not work.. please install needed libraries")
            return

        try:
            self.picam2 = Picamera2()
            self.picam2.set_logging(Picamera2.ERROR)

            camera_config = self.picam2.create_video_configuration(main={"size": (cam_res[0], cam_res[1])})
            self.__conf: CameraConfiguration = camera_config

            self.picam2.configure(self.__conf)
            self.picam2.start_preview(Preview.NULL)
            self.picam2.start()
            tm.sleep(1)
            # self.picam2.close()

            self.__cam_is_not_available = True                  # cam is available
        except (RuntimeError, IndexError) as e:
            print("Error when trying to initialize camera:", e)
            print("No attached camera found")
            print("Is user member of the vide group? ( usermod -a -G video [username] )")

    # --------------------------------------------------------------------------------------
    def init_camera(self) -> None:
        """!
        Nothing yet
        @return: None
        """

    # --------------------------------------------------------------------------------------

    def get_capture_array(self) -> NDArray[np.uint8]:
        """!
        return numpy arrays of captured data. Makes a copt before leaving
        @return: None or array
        """

        if self.is_cam_available() is False:
            #print("No attached camera found")
            return None

        array =  self.picam2.capture_array()
        if array is None:
            print("Error, camera array is none")
            self.picam2.close()
            return None
        else:
            new_array = array.copy()
            return new_array

    # --------------------------------------------------------------------------------------

    def test_camera(self) -> None:
        """!
        Makes a small movie and saves it to disk
        @return: None
        """
        if self.is_cam_available() is False:
            print("No attached camera found")
            return False

        print("Going to capture some video")

        picam2 = Picamera2()
        picam2.set_logging(Picamera2.ERROR)
        picam2.configure(self.__conf)
        picam2.start_preview(Preview.NULL)
        picam2.start_and_record_video("test_video.mp4", duration=5)
        tm.sleep(1)
        picam2.close()

        print("Capture video is saved as test_video.mp4, in the directory whereas the robohatlib resides")

    # --------------------------------------------------------------------------------------
    def set_configuration(self, conf: CameraConfiguration) -> None:
        """!cam is available
        Sets used configuration.
        @param conf: The Camera configuration
        @return: None
        """
        self.__conf = conf

    # --------------------------------------------------------------------------------------
    def is_cam_available(self) -> bool:
        """!
        Return boolean if cam is available
        @return: bool
        """
        return self.__cam_is_not_available

    # --------------------------------------------------------------------------------------

    @staticmethod
    def __check_ffmpeg() -> bool:
        """!
        Check if ffmpeg is installed
        @return: bool
        """
        ffmpeg_available = True
        print('check_ffmpeg')
        try:
            subprocess.check_output(['which', 'ffmpeg'])
        except Exception as e:
            ffmpeg_available = False
        if not ffmpeg_available:
            print("FFMPEG not installed. Use sudo apt install ffmpeg")
            return False
        return True

    # --------------------------------------------------------------------------------------
