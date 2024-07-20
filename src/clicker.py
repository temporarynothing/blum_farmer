import pyautogui
import time

class Clicker:
    def __init__(self):
        # Initialize the clicker class if needed
        pass

    def click(self, x, y):
        # Implement the click functionality at (x, y) coordinates
        print(f"Clicking at ({x}, {y})")
        pyautogui.onScreen(x, y)
        time.sleep(0.1)
        pyautogui.click(x, y)
        time.sleep(0.3)  # Small delay to ensure the click is registered

    def write(self, text):
        # I
        # mplement the write functionality
        print(f"Writing text: {text}")
        pyautogui.typewrite(text, interval=0.05)
        time.sleep(0.5)  # Small delay to ensure the text is written

    def enter(self):
        # Implement the e
        # nter key functionality
        print("Pressing Enter")
        pyautogui.press('enter')
        time.sleep(0.5)  # Small delay to ensure the key press is registered

# Example usage
if __name__ == "__main__":
    clicker = Clicker()
    clicker.click(940, 600)
    # clicker.click(30, 230)
    # clicker.click(30, 280)
    # clicker.click(30, 330)
    # clicker.write("Hello, World!")
    # clicker.enter()
