# Network Connectivity Troubleshooting Guide

## Issue Analysis
The network server is running successfully locally, but external access through the peanut shell domain is timing out. This indicates a port forwarding or firewall issue.

## Step 1: Verify Local Server Status
First, confirm the server is running and accessible locally:

```powershell
# Check if the server is running
tasklist | findstr "python"

# Test local health check
curl.exe -s http://localhost:8700/api/health
```

## Step 2: Check Network Binding Configuration
Ensure the server is binding to the correct network interface. The current configuration in `network.yaml` looks correct (binding to 0.0.0.0:8700), but let's verify:

```powershell
# Check which processes are listening on port 8700
netstat -an | findstr "8700"
```

You should see something like:
```
TCP    0.0.0.0:8700           0.0.0.0:0              LISTENING
```

## Step 3: Verify Peanut Shell Port Forwarding
1. Open the Peanut Shell application
2. Check the port forwarding configuration:
   - Ensure the internal IP address matches your computer's local IP (e.g., 192.168.x.x)
   - Ensure the internal port is set to 8700
   - Ensure the external port is also set to 8700 (or verify what external port is configured)
   - Ensure the protocol is set to TCP

## Step 4: Check Windows Firewall Settings
1. Open Windows Defender Firewall
2. Click on "Advanced settings"
3. Check both inbound and outbound rules:
   - Ensure there's an inbound rule allowing TCP traffic on port 8700
   - Ensure there's an outbound rule allowing TCP traffic on port 8700
   - If no rules exist, create new ones for port 8700

## Step 5: Test External Port Accessibility
Use a port checking tool to verify if port 8700 is accessible from the outside:

1. Visit https://www.canyouseeme.org/
2. Enter port 8700
3. Click "Check Port"

## Step 6: Verify Peanut Shell Domain Status
Check if the peanut shell domain is properly resolving and the service is running:

```powershell
# Check DNS resolution
nslookup 1nz171374pe64.vicp.fun

# Check if the domain is reachable (even if port is closed)
ping 1nz171374pe64.vicp.fun
```

## Step 7: Restart Services
1. Restart the peanut shell application
2. Restart the OpenAgents network server:

```powershell
# First, stop any running instances
Stop-Process -Name "python" -ErrorAction SilentlyContinue

# Then restart the server
cd c:\Users\biren\Documents\trae_projects\ai
python -m openagents network start ./my_first_network
```

## Step 8: Test with Alternative Port
If port 8700 is blocked by your ISP, try using a different port:

1. Update `network.yaml` to use a different port (e.g., 8080):
   ```yaml
   transports:
     - type: "http"
       config:
         host: "0.0.0.0"
         port: 8080
         cors_enabled: true
   ```

2. Update peanut shell port forwarding to use the new port
3. Restart the server
4. Test the new port

## Step 9: Check Router Configuration
If you're behind a router, ensure:
1. UPnP is enabled on your router (for automatic port forwarding)
2. If UPnP is disabled, manually configure port forwarding on your router:
   - Forward external port 8700 to internal IP:8700
   - Use TCP protocol

## Expected Results
After resolving the connectivity issues, you should be able to access the health check endpoint from outside:

```powershell
curl.exe -s http://1nz171374pe64.vicp.fun:8700/api/health
```

This should return a JSON response similar to the local health check.

## Notes
- If you're on a public network (school, office), there might be network restrictions blocking port forwarding
- Some ISPs block common ports for security reasons
- Ensure your computer has a static local IP address to avoid port forwarding configuration issues after reboots