import argparse

parser = argparse.ArgumentParser(description="Run the hunter robot.")
parser.add_argument("--showLiveFeed", action="store_true",
                    help="Show a live window with the detected objects boxed.")
parser.add_argument("--saveFrames", action="store_true",
                    help="Save every annotated camera frame to saved_frames/ (slows the control loop).")
parser.add_argument("--camera", type=int, default=0,
                    help="Camera index to use (default: 0).")
parser.add_argument("--i2c", type=int, default=1,
                    help="I2C device index (default: 1).")
parser.add_argument("--chipid", type=int, default=0,
                    help="Chip ID (default: 0).")
parser.add_argument("--debug", action="store_true",
                    help="Enable debug mode.")
parser.add_argument("--modelVersion", type=float, default=4.5,
                    help = "Model version (default: 4.5).")
args = parser.parse_args()