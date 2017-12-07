import digitalio
import board
import storage

switch = digitalio.DigitalInOut(board.D11)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# If the D0 is connected to ground with a wire
# CircuitPython can write to the drive
storage.remount("/", not switch.value)
