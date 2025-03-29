## Setting a Static IP Address Using `nmcli`

### 1. Identify the Network Connection
First, you'll need to identify the network connection you want to configure.

List all network connections:

```sh
nmcli connection show
```

This will list all active and inactive connections. Look for the name of the connection you want to change (e.g., `Wired connection 1`, `Wi-Fi connection 1`, or any other interface you're using).

---

### 2. Set a Static IP Address
To configure the static IP, use the following command structure:

```sh
sudo nmcli con mod <connection-name> ipv4.method manual ipv4.addresses <static-ip>/<subnet> ipv4.gateway <gateway-ip> ipv4.dns <dns-ip>
```

#### Parameter Explanations:
- `<connection-name>`: The name of the network connection you want to modify (e.g., `Wired connection 1`).
- `<static-ip>`: The static IP address you want to assign (e.g., `192.168.1.100`).
- `<subnet>`: The subnet mask (e.g., `24` for a `255.255.255.0` mask).
- `<gateway-ip>`: The default gateway IP (usually your router's IP, e.g., `192.168.1.1`).
- `<dns-ip>`: The DNS server IP you want to use (e.g., `8.8.8.8` for Google DNS or your local DNS server).

#### Example:
```sh
sudo nmcli con mod "Wired connection 1" ipv4.method manual ipv4.addresses 192.168.1.100/24 ipv4.gateway 192.168.1.1 ipv4.dns 8.8.8.8
```

---

### 3. Apply the Changes
After modifying the connection settings, apply the changes by deactivating and reactivating the connection:

```sh
sudo nmcli con down <connection-name> && sudo nmcli con up <connection-name>
```

#### Example:
```sh
sudo nmcli con down "Wired connection 1" && sudo nmcli con up "Wired connection 1"
```

This will restart the connection with the new static IP configuration.

---

### 4. Verify the Configuration
To verify the static IP settings, run:

```sh
nmcli con show <connection-name>
```

You should see the updated settings, including the static IP, gateway, and DNS configuration.

You can also check the IP address with:

```sh
ip a
```
