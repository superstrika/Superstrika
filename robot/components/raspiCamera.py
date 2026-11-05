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
                 imageRes: tuple[int, int] = (512, 512),
                 outputDir: str = "saved_frames",
                 cameraIndex: int = 0,
                 showLiveFeed: bool = False,
                 ):

        super().__init__(modelPath=modelPath, imageRes=imageRes, focalLength=focalLength, objectNames=objectNames,
                         outputDir=outputDir, showLiveFeed=showLiveFeed)

        # camera configuration:
        self._picam = Picamera2(camera_num=cameraIndex)

        # Use the full-sensor mode so we get the entire FOV (smaller modes are often cropped).
        sensorW, sensorH = self._picam.sensor_resolution

        # Ask the ISP for a frame with the SENSOR's aspect ratio (a square main size would make
        # libcamera crop the sides). Scale it down so its short side is just big enough
        # for the target resolution - the final square crop + resize happens in captureFrame().
        targetDim = max(imageRes)
        scale = min(1.0, targetDim / min(sensorW, sensorH))
        mainSize = (int(sensorW * scale) // 2 * 2, int(sensorH * scale) // 2 * 2)

        config = self._picam.create_preview_configuration(
            main={"size": mainSize, "format": "RGB888"},
            raw={"size": (sensorW, sensorH)},
        )
        self._picam.align_configuration(config)
        self._picam.configure(config)

        self._picam.start()

        cameraControls = {
            "AfMode": 0,  # manual focus
            "LensPosition": 50.0,  # focus to infinity
        }
        # Make sure the ISP reads the whole sensor area (no digital zoom/crop).
        if "ScalerCrop" in self._picam.camera_controls:
            cameraControls["ScalerCrop"] = self._picam.camera_controls["ScalerCrop"][1]
        self._picam.set_controls(cameraControls)

        # calibration:
        if self._focalLength == 0.0:
            self.calibrate(50)

    def captureFrame(self) -> None:
        """Updates the object information by capturing an image,
        and making the model look for the objects in it.
        """

        # Picamera2's "RGB888" format is stored in memory as B,G,R per pixel,
        # which is already the channel order OpenCV expects - no conversion needed.
        # Cut the sides to a square, then scale the whole square down to imageRes.
        return self._cropAndScale(self._picam.capture_array())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Raspberry Pi camera object detection.")
    parser.add_argument("--showLiveFeed", action="store_true",
                        help="Show a live window with the detected objects boxed.")
    parser.add_argument("--camera", type=int, default=0,
                        help="Camera index to use (default: 0).")
    args = parser.parse_args()

    cam = RaspiCamera("robot/models/best-V4.5.onnx",
                      cameraIndex=args.camera,
                      showLiveFeed=args.showLiveFeed)

    try:
        while True:
            print(cam.getObjects(mirror=True))
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
