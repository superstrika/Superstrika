import time
import os
import cv2

# Directory where captured frames will be saved
output_dir = "saved_frames_raw"
os.makedirs(output_dir, exist_ok=True)


def main() -> None:

    # Initialize webcam (0 is usually the default built-in/USB camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Camera started. Resolution: {width}x{height}")
    print(f"Captured frames will be saved to '{output_dir}/' directory.")
    print("Press 'Enter' to capture and save the current frame.")
    print("Press 'q' to quit.")

    frame_count = 0

    try:
        while True:
            # Capture the current frame
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            # Display the live feed
            cv2.imshow("Webcam - Press Enter to Capture", frame)

            # Check for key press (non-blocking with 1ms delay)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                # Quit
                break
            elif key in (13, 10):  # Enter key (carriage return / line feed)
                # Capture and save frame
                frame_count += 1
                timestamp = time.strftime("%Y%m%d_%H%M%S_%f")
                filename = os.path.join(output_dir, f"raw_frame_{timestamp}.jpg")

                cv2.imwrite(filename, frame)
                print(f"[{frame_count}] Saved: {filename}")

    except KeyboardInterrupt:
        print("\nCapture stopped by user (Ctrl+C).")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"\nSession complete. Total frames captured: {frame_count}")
        print(f"Frames saved in: {os.path.abspath(output_dir)}/")


if __name__ == "__main__":
    main()
