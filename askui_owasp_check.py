"""
askui_owasp_check.py - Automated OWASP Top 10 UI checks using AskUI Vision Agent (Python)

Requirements:
- askui (pip install askui)  # Use the latest version
- python-dotenv (pip install python-dotenv)
- AskUI Agent OS running
- Environment variables: ASKUI_WORKSPACE_ID, ASKUI_TOKEN, ANTHROPIC_API_KEY, ASKUI_INSTALLATION_DIRECTORY

See https://github.com/askui/vision-agent for details
"""

import os
import sys
import time
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("[AskUI OWASP Check] Optional: Install python-dotenv to load .env files automatically.")

REQUIRED_ENV_VARS = [
    "ASKUI_WORKSPACE_ID",
    "ASKUI_TOKEN",
    "ANTHROPIC_API_KEY",
    "ASKUI_INSTALLATION_DIRECTORY"
]
missing = [var for var in REQUIRED_ENV_VARS if not os.environ.get(var)]
if missing:
    print("\n[ERROR] The following required environment variables are missing:\n")
    for var in missing:
        print(f"  - {var}")
    print("\nPlease set them in your environment or in a .env file before running this script.\n")
    sys.exit(1)

from askui import VisionAgent

# Payloads for security testing
XSS_PAYLOAD = "<script>alert('xss')</script>"
SQLI_PAYLOAD = "' OR '1'='1"


def run_owasp_security_check(url="https://mabu.red/"):
    results = []
    with VisionAgent() as agent:
        # Step 2: Open Site
        print(f"[AskUI OWASP Check] Opening {url}")
        agent.tools.webbrowser.open_new(url)
        # Step 3: Wait
        time.sleep(4)  # Wait for page load

        # Step 4: Find Inputs
        print("[AskUI OWASP Check] Locating input fields...")
        inputs = agent.locate(role="textbox")
        print(f"[AskUI OWASP Check] Found {len(inputs)} input fields.")

        # Step 5: XSS Test
        for idx, input_field in enumerate(inputs):
            print(f"[AskUI OWASP Check] Testing XSS in input #{idx+1}")
            agent.click(input_field)
            agent.type(XSS_PAYLOAD)
            agent.keyboard("enter")
            time.sleep(1)

        # Step 6: SQLi Test
        for idx, input_field in enumerate(inputs):
            print(f"[AskUI OWASP Check] Testing SQLi in input #{idx+1}")
            agent.click(input_field)
            agent.type(SQLI_PAYLOAD)
            agent.keyboard("enter")
            time.sleep(1)

        # Step 7: Check Errors
        errors = agent.get("Are there any error messages or debug traces visible?")
        print(f"[AskUI OWASP Check] Error/debug scan: {errors}")
        results.append(("Error/debug scan", errors))

        # Step 8: Admin Link?
        admin_present = agent.get("Is there an admin, login, or logout link visible?")
        print(f"[AskUI OWASP Check] Admin/Login/Logout link present: {admin_present}")
        results.append(("Admin/Login/Logout link present", admin_present))

        # Step 9: Admin Test
        if admin_present:
            agent.act("Click on the admin link and check for access or error messages.")
            admin_access = agent.get("Was access to the admin area successful or blocked?")
            print(f"[AskUI OWASP Check] Admin area access result: {admin_access}")
            results.append(("Admin area access", admin_access))

        # Step 11: Log Results
        print("\n[AskUI OWASP Check] --- Summary ---")
        for label, result in results:
            print(f"{label}: {result}")

if __name__ == "__main__":
    run_owasp_security_check()
