// askui-owasp-check.ts
// Automated OWASP Top 10 UI checks for https://mabu.red/
// Requires AskUI CLI and environment set up

import { UiController, UiFinder, UiMouse, UiKeyboard, UiAssert, UiScroll, UiClipboard } from 'askui';

async function runOwaspChecks() {
  const controller = await UiController.start();
  try {
    // 1. Open the website
    await controller.run(async (ui) => {
      await ui.open.url('https://mabu.red/');
      await ui.wait(3000); // Wait for load
    });

    // 2. Check for HTTPS (Sensitive Data Exposure)
    // NOTE: AskUI can't check protocol directly, but can check for lock icon or URL bar text
    // This is a placeholder for manual/extension-based check

    // 3. Try inputting XSS payload in all visible input fields (Injection/XSS)
    const xssPayload = "<script>alert('xss')</script>";
    await controller.run(async (ui) => {
      const inputs = await ui.find.elements({ role: 'textbox' });
      for (const input of inputs) {
        await ui.click(input);
        await ui.keyboard.type(xssPayload);
        await ui.keyboard.press('Enter');
        await ui.wait(1000);
      }
    });

    // 4. Try SQLi payload in input fields (Injection)
    const sqliPayload = "' OR '1'='1";
    await controller.run(async (ui) => {
      const inputs = await ui.find.elements({ role: 'textbox' });
      for (const input of inputs) {
        await ui.click(input);
        await ui.keyboard.type(sqliPayload);
        await ui.keyboard.press('Enter');
        await ui.wait(1000);
      }
    });

    // 5. Look for error messages (Security Misconfiguration, Broken Auth)
    await controller.run(async (ui) => {
      const errorTexts = [
        'error', 'not allowed', 'forbidden', 'sql', 'exception', 'denied', 'unauthorized', 'failed', 'invalid'
      ];
      for (const text of errorTexts) {
        const found = await ui.find.text(text).exists();
        if (found) {
          console.log(`Potential issue: Found error message '${text}' on page.`);
        }
      }
    });

    // 6. Check for login/logout (Broken Auth, Broken Access Control)
    await controller.run(async (ui) => {
      const loginExists = await ui.find.text('login').exists();
      const logoutExists = await ui.find.text('logout').exists();
      if (loginExists) {
        console.log('Login functionality detected. Manual auth checks recommended.');
      }
      if (logoutExists) {
        console.log('Logout functionality detected. Manual session checks recommended.');
      }
    });

    // 7. Check for cookies with secure/httponly flags (Sensitive Data Exposure)
    // NOTE: AskUI cannot directly access cookies; use browser devtools or extensions for this

    // 8. Try accessing admin/restricted URLs (Broken Access Control)
    // NOTE: UI automation can attempt to visit /admin or /dashboard if links are present
    await controller.run(async (ui) => {
      const adminLink = await ui.find.text('admin').exists();
      if (adminLink) {
        await ui.click(await ui.find.text('admin'));
        await ui.wait(2000);
        // Check for forbidden/allowed
        const forbidden = await ui.find.text('forbidden').exists();
        if (forbidden) {
          console.log('Admin area is properly restricted.');
        }
      }
    });

    // 9. General: Look for visible stack traces or debug info (Security Misconfiguration)
    await controller.run(async (ui) => {
      const debugTexts = ['stack trace', 'traceback', 'debug', 'exception'];
      for (const text of debugTexts) {
        const found = await ui.find.text(text).exists();
        if (found) {
          console.log(`Potential misconfiguration: Found debug info '${text}' on page.`);
        }
      }
    });

    // 10. Logging/Monitoring (Not testable via UI)
    // 11. Insecure Deserialization/Components with Known Vulns (Not testable via UI)

    console.log('OWASP Top 10 UI checks completed.');
  } finally {
    await UiController.shutdown();
  }
}

runOwaspChecks();
