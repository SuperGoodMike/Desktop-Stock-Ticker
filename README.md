# ESP32-S3 Desktop-Stock-Ticker
Desktop Stock Ticker Project
This project displays real-time stock prices on a **Waveshare ESP32-S3 Touch LCD 1.28** device. The stock data is fetched from a Google Sheets document published as a CSV file, and the display is updated periodically.

## Hardware
- **Device**: [Waveshare ESP32-S3 Touch LCD 1.28](https://www.waveshare.com/wiki/ESP32-S3-Touch-LCD-1.28)
  - 1.28-inch LCD display with 240x240 resolution
  - ESP32-S3 microcontroller with Wi-Fi and Bluetooth
  - Touchscreen support
  - Built-in RGB LED and accelerometer

## Features
- Fetches stock data from a Google Sheets document published as a CSV.
- Displays stock symbols, prices, changes, and friendly names.
- Automatically cycles through multiple stocks.
- Updates stock data periodically.
- Garbage collection integrated to prevent memory leaks and crashes.

## Prerequisites
- **MicroPython Firmware**: Ensure your ESP32-S3 is flashed with MicroPython. Follow the [official MicroPython guide](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html) for installation or use the firmware included in this project.
- **Google Sheets**: Publish your stock data as a CSV file. Replace the `GOOGLE_SHEETS_URL` in the script with your published CSV URL.
- **Wi-Fi Credentials**: Update the `WIFI_SSID` and `WIFI_PASSWORD` in the script with your Wi-Fi credentials.

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SuperGoodMike/Desktop-Stock-Ticker.git
   cd Desktop-Stock-Ticker
   # Upload the Code

Use a tool like Thonny IDE or ampy to upload the script to your ESP32-S3.

The main script is `main.py`.

# Install Required Libraries

Ensure the following libraries are available on your ESP32-S3:

- `gc9a01`: For controlling the LCD display.
- `vga1_bold_16x32`: Font for rendering text on the display.
- `urequests`: For making HTTP requests to fetch stock data.

These libraries are included in the `lib/` folder of this repository. Upload them to your device.

# Configure Google Sheets

Create a Google Sheets document with the following columns:

- **Column A**: Stock symbol (e.g., AAPL)
- **Column B**: Stock price (use the formula below)
- **Column C**: Price change (use the formula below)
- **Column D**: Friendly name (e.g., Apple Inc.)

Publish the sheet as a CSV file and update the `GOOGLE_SHEETS_URL` in the script.

# Run the Script

Power on the ESP32-S3. The device will connect to Wi-Fi, fetch stock data, and display it on the LCD.

# Code Overview

- **`main.py`**: The main script that initializes the display, connects to Wi-Fi, fetches stock data, and updates the display.
- **`fetch_stock_data()`**: Fetches stock data from the Google Sheets URL.
- **`display_stock_data()`**: Parses and displays stock data on the LCD.
- **Garbage Collection**: Integrated to prevent memory leaks and crashes.

# Customization

- **Update Frequency**: Adjust the `time.sleep(10)` in the main loop to change how often the stock data is updated.
- **Display Layout**: Modify the `display_stock_data()` function to change how the stock data is displayed.
- **Additional Features**: Add support for touchscreen input or use the built-in accelerometer for interactive features.

# Troubleshooting

- **No Data Displayed**: Ensure the Google Sheets URL is correct and the sheet is published as a CSV.
- **Wi-Fi Connection Issues**: Double-check the `WIFI_SSID` and `WIFI_PASSWORD` in the script.
- **Memory Issues**: If the device crashes, try increasing the frequency of `gc.collect()` calls or reduce the amount of data being processed.

# How to Share a Google Sheet

## Create a Google Sheet

1. Go to [Google Sheets](https://sheets.google.com) and create a new sheet.
2. Add the following columns:
   - **Column A**: Stock symbol (e.g., AAPL)
   - **Column B**: Stock price (use the formula below)
   - **Column C**: Price change (use the formula below)
   - **Column D**: Friendly name (e.g., Apple Inc.)

## Add Formulas

- In **Column B (Price)**, use the formula:
  ```plaintext
  =GOOGLEFINANCE(A2, "price")
  # Example

| A    | B                                | C                                          | D         |
|------|----------------------------------|--------------------------------------------|-----------|
| IVW  | `=GOOGLEFINANCE(A2, "price")`    | `=GOOGLEFINANCE(A2, "changepct")/100`      | S&P 500   |
| AAPL | `=GOOGLEFINANCE(A3, "price")`    | `=GOOGLEFINANCE(A3, "changepct")/100`      | Apple Inc.|

## Publish the Sheet

1. Click on **File > Share > Publish to web**.
2. Select the sheet and choose **CSV** as the format.
3. Click **Publish** and copy the generated URL.

## Update the Script

Replace the `GOOGLE_SHEETS_URL` in the script with the published CSV URL.

## Example Google Sheet Layout

| A    | B                                | C                                          | D             |
|------|----------------------------------|--------------------------------------------|---------------|
| IVW  | `=GOOGLEFINANCE(A2, "price")`    | `=GOOGLEFINANCE(A2, "changepct")/100`      | S&P 500       |
| AAPL | `=GOOGLEFINANCE(A3, "price")`    | `=GOOGLEFINANCE(A3, "changepct")/100`      | Apple Inc.    |
| GOOG | `=GOOGLEFINANCE(A4, "price")`    | `=GOOGLEFINANCE(A4, "changepct")/100`      | Alphabet Inc. |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
