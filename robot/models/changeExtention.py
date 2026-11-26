from ultralytics import YOLO

# Load your custom or pretrained .pt model
model = YOLO("/home/admin/Superstrika/robot/models/best-V7.0.pt")  # replace with your model path

# Export the model to ONNX format
model.export(format="onnx", dynamic=True)