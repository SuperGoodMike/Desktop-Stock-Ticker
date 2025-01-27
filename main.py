import time
from machine import Pin, SPI
import gc9a01
import vga1_bold_16x32 as font
import network
import urequests
import gc  # Import the garbage collection module

# Wi-Fi credentials (replace with your WIFI Settings)
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

# Google Sheets URL (replace with your published CSV URL)
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/your_google_sheet_id/pub?gid=0&single=true&output=csv"

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("Connected to Wi-Fi")
    print("IP:", wlan.ifconfig()[0])

# Fetch stock data from Google Sheets
def fetch_stock_data():
    try:
        response = urequests.get(GOOGLE_SHEETS_URL)
        if response.status_code == 200:
            print("Data fetched successfully")
            return response.text
        else:
            print("Failed to fetch data. Status code:", response.status_code)
            return None
    except Exception as e:
        print("Error fetching data:", e)
        return None
    finally:
        gc.collect()  # Run garbage collection after fetching data

# Parse and display stock data
def display_stock_data(tft, data, index):
    try:
        tft.fill(gc9a01.BLACK)  # Clear the screen
        lines = data.split('\n')
        if index >= len(lines):
            index = 0  # Wrap around to the first stock

        if ',' in lines[index]:  # Ensure the line contains valid data
            symbol, price, change, friendly_name = lines[index].strip().split(',')
            print(f"Stock: {symbol}, Price: {price}, Change: {change}, Name: {friendly_name}")

            # Calculate the X position to center the text
            def center_x(text):
                text_width = len(text) * font.WIDTH  # Calculate total width of the text
                return (tft.width() - text_width) // 2  # Center the text horizontally

            # Display change (Column C) at the top
            change_x = center_x(change)
            try:
                change_value = float(change.strip('%'))  # Convert change to a numeric value
                change_color = gc9a01.GREEN if change_value >= 0 else gc9a01.RED
            except ValueError:
                change_color = gc9a01.WHITE  # Default to white if change is invalid
            tft.text(font, change, change_x, 40, change_color, gc9a01.BLACK)

            # Display friendly name (Column D) in the middle
            friendly_name_x = center_x(friendly_name)
            tft.text(font, friendly_name, friendly_name_x, 90, gc9a01.WHITE, gc9a01.BLACK)

            # Display price (Column B) at the bottom
            price_x = center_x(price)
            tft.text(font, price, price_x, 140, gc9a01.WHITE, gc9a01.BLACK)
    except Exception as e:
        print("Error displaying stock data:", e)
    finally:
        gc.collect()  # Run garbage collection after displaying data

def main():
    # Initialize display
    spi = SPI(2, baudrate=80000000, polarity=0, sck=Pin(10), mosi=Pin(11))
    tft = gc9a01.GC9A01(
        spi,
        240,
        240,
        reset=Pin(14, Pin.OUT),
        cs=Pin(9, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        backlight=Pin(2, Pin.OUT),
        rotation=0,
        buffer_size=16*32*2
    )

    tft.init()
    tft.fill(gc9a01.BLACK)
    time.sleep(1)

    # Connect to Wi-Fi
    connect_wifi()

    # Main loop
    index = 0
    while True:
        # Fetch stock data
        data = fetch_stock_data()
        if not data:
            print("No data fetched. Retrying in 10 seconds...")
            time.sleep(10)
            continue

        # Display the current stock
        display_stock_data(tft, data, index)

        # Move to the next stock
        index += 1
        if index >= len(data.split('\n')):
            index = 0  # Wrap around to the first stock

        # Wait before switching to the next stock
        time.sleep(10)  # Change every 10 seconds

        gc.collect()  # Run garbage collection periodically in the main loop

# Run the program
if __name__ == "__main__":
    main()