import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal

# --- Display setup ---
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)

# Create a new label with the color and text selected
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(0, (matrixportal.graphics.display.height // 2) - 1),
    scrolling=True,  # Enable scrolling
)

# Static 'Connecting' Text
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(2, (matrixportal.graphics.display.height // 2) - 1),
)

# Update these to your new text feeds
TEXT_FEED = "hello"
RESET_FEED = "reset"
SCROLL_DELAY = 0.02
UPDATE_DELAY = 600

def get_last_data(feed_key):
    try:
        # Fetch the most recent data from the specified feed
        data = matrixportal.get_io_data(feed_key)
        if data:
            # Return the value of the most recent data point
            return data[0]["value"]
    except Exception as e:
        print(f"Error fetching data from feed {feed_key}: {e}")
    return None

def update_display():
    text_value = get_last_data(TEXT_FEED)

    if text_value:
        matrixportal.set_text(text_value)
        matrixportal.set_text_color(0x00FF00)  # Set the text color to green
    else:
        print("Failed to retrieve data from feed")
        matrixportal.set_text("No Data", 0)

def check_reset():
    reset_value = get_last_data(RESET_FEED)

    if reset_value:
        try:
            reset_interval = int(reset_value)
            return reset_interval
        except ValueError:
            print(f"Invalid reset value: {reset_value}")
    return UPDATE_DELAY  # Default reset interval if the feed is empty or invalid

last_update = time.monotonic()
update_display()

# Main loop
while True:
    matrixportal.scroll_text(SCROLL_DELAY)  # Continuously scroll text
    current_time = time.monotonic()
    reset_interval = check_reset()

    if current_time - last_update > reset_interval:
        update_display()
        last_update = current_time
