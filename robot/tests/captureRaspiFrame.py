import time
import os
from picamera2 import Picamera2
import cv2

# Camera configuration
IMAGE_RES = (2592, 2592)

# Directory where captured frames will be saved
output_dir = "saved_frames"
os.makedirs(output_dir, exist_ok=True)


def main() -> None:

    # Initialize PiCamera 2
    picam = Picamera2()
    previewConfig = picam.preview_configuration
    previewConfig.main.size = IMAGE_RES
    previewConfig.main.format = "RGB888"
    picam.configure("preview")

    picam.start()

    # Set manual focus to infinity
    picam.set_controls({
        "AfMode": 0,  # manual focus
        "LensPosition": 50.0,  # focus to infinity
    })

    print(f"Camera started. Resolution: {IMAGE_RES[0]}x{IMAGE_RES[1]}")
    print(f"Captured frames will be saved to '{output_dir}/' directory.")
    print("Press 'Enter' to capture and save the current frame.")
    print("Press 'q' to quit.")

    frame_count = 0

    try:
        while True:
            # Capture the current frame
            frame = picam.capture_array()

            # Display the live feed
            cv2.imshow("Raspberry Pi Camera - Press Enter to Capture", frame)

            # Check for key press (non-blocking with 1ms delay)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                # Quit
                break
            elif key in (13, 10):  # Enter key (carriage return / line feed)
                # Capture and save frame
                frame_count += 1
                timestamp = time.strftime("%Y%m%d_%H%M%S_%f")
                filename = os.path.join(output_dir, f"frame_{timestamp}.jpg")

                cv2.imwrite(filename, frame)
                print(f"[{frame_count}] Saved: {filename}")

    except KeyboardInterrupt:
        print("\nCapture stopped by user (Ctrl+C).")

    finally:
        picam.close()
        cv2.destroyAllWindows()
        print(f"\nSession complete. Total frames captured: {frame_count}")
        print(f"Frames saved in: {os.path.abspath(output_dir)}/")


if __name__ == "__main__":
    main()
