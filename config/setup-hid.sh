#!/bin/bash
# Setup USB HID Gadget on Raspberry Pi
# Run with: sudo bash setup-hid.sh

set -e

echo "[*] Setting up USB HID Gadget..."

# 1. Enable dwc2 in device tree
echo "[*] Configuring device tree overlay..."
if grep -q "dtoverlay=dwc2" /boot/firmware/usercfg.txt 2>/dev/null || grep -q "dtoverlay=dwc2" /boot/usercfg.txt 2>/dev/null; then
    echo "[OK] dwc2 overlay already enabled"
else
    echo "dtoverlay=dwc2" | sudo tee -a /boot/firmware/usercfg.txt > /dev/null 2>&1 || \
    echo "dtoverlay=dwc2" | sudo tee -a /boot/usercfg.txt > /dev/null 2>&1
    echo "[OK] dwc2 overlay added to boot config"
fi

# 2. Enable libcomposite module on startup
echo "[*] Configuring libcomposite module..."
if grep -q "libcomposite" /etc/modules 2>/dev/null; then
    echo "[OK] libcomposite already in /etc/modules"
else
    echo "libcomposite" | sudo tee -a /etc/modules > /dev/null
    echo "[OK] libcomposite added to /etc/modules"
fi

# 3. Create HID gadget startup script
echo "[*] Creating HID gadget initialization script..."
sudo tee /usr/local/bin/setup-gadget.sh > /dev/null << 'GADGET_SCRIPT'
#!/bin/bash
# Initialize USB HID gadget

set -x  # Debug mode
GADGET_PATH="/sys/kernel/config/usb_gadget"
GADGET_NAME="g1"

# Wait for system to be ready
sleep 2

# Remove old gadget if it exists
if [ -d "$GADGET_PATH/$GADGET_NAME" ]; then
    echo "Removing old gadget..."
    cd "$GADGET_PATH/$GADGET_NAME"
    [ -f "UDC" ] && echo "" > UDC 2>/dev/null || true
    cd /
    rm -rf "$GADGET_PATH/$GADGET_NAME" 2>/dev/null || true
    sleep 1
fi

# Create gadget root
mkdir -p "$GADGET_PATH/$GADGET_NAME"
cd "$GADGET_PATH/$GADGET_NAME"

# Set USB device information
echo 0x1d6b > idVendor
echo 0x0109 > idProduct
echo 0x0100 > bcdDevice

# Create strings directory and set them
mkdir -p strings/0x409
echo "0000000012345678" > strings/0x409/serialnumber
echo "Custom" > strings/0x409/manufacturer
echo "USB Keyboard" > strings/0x409/product

# Create configuration structure FIRST
mkdir -p configs/c.1/strings/0x409
echo "HID Keyboard" > configs/c.1/strings/0x409/configuration
echo 100 > configs/c.1/MaxPower

# Create HID function AFTER config exists
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length

# Create HID report descriptor (keyboard)
printf '\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x03\x95\x05\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x03\x95\x06\x75\x08\x15\x00\x25\x65\x05\x07\x19\x00\x29\x65\x81\x00\xc0' > functions/hid.usb0/report_desc

# NOW link function to config (both should exist now)
ln -sf ../../functions/hid.usb0 configs/c.1/hid.usb0 || exit 1

# Bind to UDC
UDC=$(ls /sys/class/udc/ | head -1)
if [ -n "$UDC" ]; then
    echo "$UDC" > UDC
    echo "Bound to UDC: $UDC"
else
    echo "ERROR: No UDC found"
    exit 1
fi

echo "HID gadget initialized successfully"
ls -la
GADGET_SCRIPT

sudo chmod +x /usr/local/bin/setup-gadget.sh
echo "[OK] Gadget initialization script created"

# 4. Create systemd service to auto-start gadget
echo "[*] Creating systemd service..."
sudo tee /etc/systemd/system/usb-gadget.service > /dev/null << 'SERVICE_SCRIPT'
[Unit]
Description=USB HID Gadget
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/setup-gadget.sh
RemainAfterExit=yes
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SERVICE_SCRIPT

echo "[OK] Systemd service created"

# 5. Enable and start the service
echo "[*] Enabling USB gadget service..."
sudo systemctl daemon-reload
sudo systemctl enable usb-gadget.service
echo "[OK] Service enabled"

echo ""
echo "[*] Setup complete!"
echo "[*] Please REBOOT the Raspberry Pi for changes to take effect:"
echo "    sudo reboot"
echo ""
echo "[*] After reboot, verify setup with:"
echo "    ls -la /dev/hidg0"
echo ""
