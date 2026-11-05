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
                 showLiveFeed: bool = False
                 ) -> None:

        super().__init__(modelPath=modelPath, imageRes=imageRes, focalLength=focalLength, objectNames=objectNames,
                         outputDir=outputDir, showLiveFeed=showLiveFeed)

        # Camera configuration
        self._webcam = cv2.VideoCapture(cameraIndex)
        if not self._webcam.isOpened():
            raise RuntimeError(f"Could not open camera {cameraIndex}")

        # Calibration
        if self._focalLength == 0.0:
            self.calibrate(50)

    def captureFrame(self) -> None:
        ret, frame = self._webcam.read()
        if not ret:
            return None

        # Frame dimensions
        frame_h, frame_w, _ = frame.shape

        min_dim = min(frame_h, frame_w)
        start_x = (frame_w - min_dim) // 2
        start_y = (frame_h - min_dim) // 2

        return cv2.resize(frame[start_y:start_y + min_dim, start_x:start_x + min_dim], self._imageRes,
                          interpolation=cv2.INTER_AREA)

if __name__ == "__main__":
    import time

    parser = argparse.ArgumentParser(description="Run the webcam object detection.")
    parser.add_argument("--showLiveFeed", action="store_true",
                        help="Show a live window with the detected objects boxed.")
    parser.add_argument("--camera", type=int, default=0,
                        help="Camera index to use (default: 0).")
    args = parser.parse_args()

    VERSION = 4.5
    c = WebCamera(f"/home/admin/Superstrika/robot/models/best-V{VERSION}.onnx",
                  focalLength=594.8065824286882,
                  cameraIndex=args.camera,
                  showLiveFeed=args.showLiveFeed)

    try:
        while True:
            distances = c.getObjects()
            print(distances)
            time.sleep(0.05)  # Slight pause between captures to control saved image rate
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
