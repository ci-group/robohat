from __future__ import annotations

try:
    import subprocess
    import time as tm
except ImportError:
    raise ImportError("Failed to import subprocess or time for the Camera class, make sure picamera2 is installed")

try:
    from picamera2 import Picamera2, Preview

except ImportError:
    raise ImportError("Failed to import needed dependencies for the Camera class, make sure picamera2 is installed")

    # --------------------------------------------------------------------------------------

class Camera:
    def __init__(self):
        """!
        Constructor of the Camera class
        """
        self.__picam2 = None
        self.__cam_is_not_available = False

        if self.__check_ffmpeg() is False:
            print("No FFMpeg found. Camera can not work.. please install needed libraries")
            return

        try:
            picam2 = Picamera2()
            picam2.set_logging(Picamera2.ERROR)
            camera_config = picam2.create_preview_configuration()

            self.__conf: CameraConfiguration = camera_config

            picam2.configure(self.__conf)
            picam2.start_preview(Preview.NULL)
            picam2.start()
            tm.sleep(1)
            picam2.close()

            self.__cam_is_not_available = True                  # cam is available
        except RuntimeError:
            print("No attached camera found")

    # --------------------------------------------------------------------------------------
    def init_camera(self) -> None:
        """!
        Nothing yet
        @return: None
        """

    # --------------------------------------------------------------------------------------

    def get_capture_array(self):
        """!
        return numpy arrays of captured data. Makes a copt before leaving
        @return: None or array
        """

        if self.is_cam_available() is False:
            print("No attached camera found")
            return None

        picam2 = Picamera2()
        picam2.set_logging(Picamera2.ERROR)
        picam2.configure(self.__conf)
        picam2.start_preview(Preview.NULL)
        picam2.start()
        tm.sleep(1)

        array =  picam2.capture_array();
        if array is None:
            print("Error, camera array is none")
            picam2.close()
            return None
        else:
            new_array = array.copy()
            picam2.close()
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
        """!
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