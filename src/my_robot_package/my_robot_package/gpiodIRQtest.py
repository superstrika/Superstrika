import gpiod
from gpiod.line import Direction, Edge, Bias
import threading
import time
import datetime

class GPIOD_IRQ:
    def __init__(self, pin: int, escape_func, rising: bool, chip_path="/dev/gpiochip0"):
        self.pin = pin
        self.escape_func = escape_func
        self.chip_path = chip_path
        
        # Determine target event type: 1 is RISING, 2 is FALLING
        self.target_event_type = Edge.FALLING
        
        self._last_interrupt_time = 0
        self._debounce_ns = 1_000_000_000  # 100ms
        
        self._running = False
        self.start()

        self.first = True
        self.count = 0

    def start(self):
        self._running = True
        # Explicitly naming the thread for debugging
        self._thread = threading.Thread(target=self._worker, name=f"IRQ_Pin_{self.pin}", daemon=True)
        self._thread.start()
        print(f"Background IRQ thread started for BCM {self.pin}")

    def _worker(self):
        # Using the absolute path to the chip
        try:
            with gpiod.request_lines(
                self.chip_path,
                consumer=f"robot_sensor_{self.pin}",
                config={
                    self.pin: gpiod.LineSettings(
                        direction=Direction.INPUT,
                        bias=Bias.PULL_UP,
                        edge_detection=Edge.FALLING
                    )
                }
            ) as request:
                while self._running:
                    # We use a short timeout (0.1s) so the thread can check self._running frequently
                    if request.wait_edge_events(datetime.timedelta(seconds=0.1)):
                        for event in request.read_edge_events():
                            # DEBUG: Uncomment the line below to see EVERY edge detected
                            # print(f"DEBUG: Edge detected: {event.event_type}")
                            # print(f"DEBUG: Edge detected: {self.target_event_type}")

                            if self.first:
                                print("Calibrating...")
                                self.first = False
                                self.target_event_type = event.event_type
                                time.sleep(1)
                                break
                            
                            if event.event_type == self.target_event_type:
                                dt = event.timestamp_ns - self._last_interrupt_time
                                if dt > self._debounce_ns:
                                    self.count += 1
                                    self.escape_func(self.count)
                                    self._last_interrupt_time = event.timestamp_ns
        except Exception as e:
            print(f"\n[FATAL ERROR] IRQ Thread for pin {self.pin} died: {e}")

    def stop(self):
        self._running = False
        if self._thread.is_alive():
            self._thread.join(timeout=1.0)

# --- Test Execution ---
def action(count):
    print(f"\n{count} >>> SENSOR TRIGGERED! <<<")

if __name__ == "__main__":
    # Test with BCM 4
    # Set rising=False for TCRT5000 (Falling edge = detection)
    sensor = GPIOD_IRQ(pin=4, escape_func=action, rising=False)

    try:
        print("Robot logic running. Trigger the sensor...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        sensor.stop()