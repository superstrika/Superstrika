import argparse
import time

from robot.abstracts.IAICamera import IAICamera
from picamera2 import Picamera2, controls
import cv2

class RaspiCamera(IAICamera):

    def __init__(self,
                 modelPath: str,
                 objectNames = None,
                 focalLength: float = 0.0,
                 imageRes: tuple[int, int] = (2592, 2592),
                 outputDir: str = "saved_frames",
                 cameraIndex: int = 0,
                 showLiveFeed: bool = False,
                 ):

        super().__init__(modelPath=modelPath, imageRes=imageRes, focalLength=focalLength, objectNames=objectNames,
                         outputDir=outputDir, showLiveFeed=showLiveFeed)

        # camera configuration:
        self._picam = Picamera2(camera_num=cameraIndex)
        previewConfig = self._picam.preview_configuration
        previewConfig.main.size = imageRes
        previewConfig.main.format = "RGB888"
        self._picam.configure("preview")

        self._picam.start()

        self._picam.set_controls({
            "AfMode": 0,  # manual focus
            "LensPosition": 50.0,  # focus to infinity
        })

        # calibration:
        if self._focalLength == 0.0:
            self.calibrate(50)

    def captureFrame(self) -> None:
        """Updates the object information by capturing an image,
        and making the model look for the objects in it.
        """

        # Picamera2's "RGB888" format is stored in memory as B,G,R per pixel,
        # which is already the channel order OpenCV expects - no conversion needed.
        return self._picam.capture_array()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Raspberry Pi camera object detection.")
    parser.add_argument("--showLiveFeed", action="store_true",
                        help="Show a live window with the detected objects boxed.")
    parser.add_argument("--camera", type=int, default=0,
                        help="Camera index to use (default: 0).")
    args = parser.parse_args()

    cam = RaspiCamera("robot/models/best-V3.0.onnx",
                      cameraIndex=args.camera,
                      showLiveFeed=args.showLiveFeed)

    try:
        while True:
            print(cam.getObjects())
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
