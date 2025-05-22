import time
import subprocess
from test_my_test import (
    tests_winning_in_Tic_Tac_Toe,
    tests_water_tank_manual_slider_test,
    tests_auto_mode,
)

# Minimal VisionAgent mock for demonstration
class VisionAgent:
    def __init__(self):
        self.tools = self
    def webbrowser(self):
        return self
    def open_new(self, url):
        print(f"[Agent] Opening URL: {url}")
    def act(self, prompt):
        print(f"[Agent] Acting with prompt:\n{prompt}")
    def get(self, question, response_schema=None):
        print(f"[Agent] Getting: {question}")
        # For demo, always return True
        return True

if __name__ == "__main__":
    agent = VisionAgent()
    print("Running Tic Tac Toe test...")
    try:
        tests_winning_in_Tic_Tac_Toe(agent)
        print("Tic Tac Toe test passed!\n")
    except Exception as e:
        print(f"Tic Tac Toe test failed: {e}\n")

    print("Running Water Tank Manual Slider test...")
    try:
        tests_water_tank_manual_slider_test(agent)
        print("Water Tank Manual Slider test passed!\n")
    except Exception as e:
        print(f"Water Tank Manual Slider test failed: {e}\n")

    print("Running Water Tank Auto Mode test...")
    try:
        tests_auto_mode(agent)
        print("Water Tank Auto Mode test passed!\n")
    except Exception as e:
        print(f"Water Tank Auto Mode test failed: {e}\n")
