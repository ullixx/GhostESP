// Minimal board interface for the display-less HW6728 ESP32-S3 N16R8.
#include <interface.h>
#include <globals.h>

// GPIO assignments are intentionally left unset until the exact HW6728 pinout
// is verified. This avoids accidentally driving flash/PSRAM or antenna-related pins.
void _setup_gpio() {
    bruceConfig.startupApp = "";
}

// The board has no navigation buttons or display.
void InputHandler(void) {}
