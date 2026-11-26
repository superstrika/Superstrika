import argparse

from robot.abstracts.IAICamera import IAICamera
import cv2

class WebCamera(IAICamera):

    def __init__(self,
                 modelPath: str,
                 objectNames = None,
                 focalLength: float = 0.0,
                 imageRes: tuple[int, int] = (256, 256),
                 outputDir: str = "saved_frames",
                 cameraIndex: int = 0,
                 showLiveFeed: bool = False,
                 saveFrames: bool = False
                 ) -> None:

        super().__init__(modelPath=modelPath, imageRes=imageRes, focalLength=focalLength, objectNames=objectNames,
                         outputDir=outputDir, showLiveFeed=showLiveFeed, saveFrames=saveFrames)

        # Camera configuration
        self._webcam = cv2.VideoCapture(cameraIndex)
        if not self._webcam.isOpened():
            raise RuntimeError(f"Could not open camera {cameraIndex}")

        # Keep only the newest frame. By default OpenCV queues a few frames, so when detection is
        # slower than the camera, read() returns an old frame and the robot reacts late.
        self._webcam.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # Calibration
        if self._focalLength == 0.0:
            self.calibrate(50)

    def captureFrame(self) -> None:
        ret, frame = self._webcam.read()
        if not ret:
            return None

        # Cut the sides to a square, then scale the whole square down to imageRes.
        return self._cropAndScale(frame)

if __name__ == "__main__":
    import time

    parser = argparse.ArgumentParser(description="Run the webcam object detection.")
    parser.add_argument("--showLiveFeed", action="store_true",
                        help="Show a live window with the detected objects boxed.")
    parser.add_argument("--camera", type=int, default=0,
                        help="Camera index to use (default: 0).")
    parser.add_argument("--saveFrames", action="store_true",
                        help="Save every annotated frame to saved_frames/.")
    args = parser.parse_args()

    VERSION = 7.0
    c = WebCamera(f"/home/admin/Superstrika/robot/models/best-V{VERSION}.onnx",
                  cameraIndex=args.camera,
                  focalLength=194.487,
                  showLiveFeed=args.showLiveFeed,
                  saveFrames=args.saveFrames)
    c.calibrate(75)
    try:
        while True:
            distances = c.getObjects()
            print(distances)
            time.sleep(0.05)  # Slight pause between captures to control saved image rate
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
