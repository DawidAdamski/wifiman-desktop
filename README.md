# WiFiman Desktop for Fedora (RPM Repackager)
This repository provides an automated way to repackage the official Ubiquiti WiFiman Desktop .deb installer into a Fedora-compatible .rpm package. It specifically addresses common issues like directory conflicts and SELinux denials that prevent Teleport (VPN) from working on RHEL-based systems.

## Why this exists?
The official WiFiman Desktop is only provided as a Debian package. Converting it using tools like alien often results in:

1. Directory Conflicts: Errors during installation regarding /usr/bin, /usr/lib, etc.
2. SELinux Denials: Teleport (WireGuard) failing to initialize because the binaries lack the correct security context.
3. Broken Systemd Integration: Services being placed in non-standard locations.

## Features
Automated CI/CD: Triggered by simply dropping a .deb file into the deb/ folder.

- Clean RPM Structure: No system directory ownership conflicts.
- SELinux Ready: Automatically applies unconfined_exec_t to the daemon and WireGuard binaries via %post scripts.
- Systemd Support: Correctly installs and enables the wifiman-desktop.service.

## How to use
1. Build your own
  1. Clone this repository.
  2. Download the latest .deb from Ubiquiti Downloads.
  3. Place the .deb file in the deb/ directory.
  4. Push the changes to GitHub:
```
git add deb/*.deb
git commit -m "Upload WiFiman v1.2.8"
git push origin master
```
  5. GitHub Actions will trigger, build the RPM, and create a new Release with the .rpm file attached.
2. Installation

Download the .rpm from the Releases tab and install it:

```
sudo dnf install ./wifiman-desktop-1.2.8-1.fcXX.x86_64.rpm
```

# Technical Details

## SELinux & Teleport

To allow Teleport to create tunnels and manage network interfaces, the RPM applies the following labels during installation:

- ` /usr/lib/wifiman-desktop/wifiman-desktopd -> unconfined_exec_t`

- ` /usr/lib/wifiman-desktop/wireguard-go -> unconfined_exec_t `

This allows the daemon to transition to a domain with sufficient privileges to manage WireGuard interfaces without disabling SELinux.

## Build Process
The CI/CD workflow avoids alien to ensure a clean build:

1. Extracts the .deb using ar and tar.
2. Reconstructs the file tree in a Fedora-compliant way.
3. Uses rpmbuild with a custom .spec file to generate the final package.

# Disclaimer
This project is not affiliated with Ubiquiti. WiFiman is proprietary software owned by Ubiquiti Inc. This repository only contains the build logic to repackage the software for personal use on Fedora Linux.

# Legal Disclaimer

- **Software Ownership**: WiFiman and WiFiman Desktop are proprietary software owned by **Ubiquiti Inc.**. This repository is not affiliated with, sponsored by, or endorsed by Ubiquiti.
- **Purpose**: This project is intended for personal use and interoperability purposes only. It provides scripts to repackage an officially downloaded Debian package into an RPM format for use on Fedora Linux.
- **Distribution**: This repository **does not** host the WiFiman source code. Any binaries produced by these scripts contain proprietary code. Users are responsible for complying with Ubiquiti's End User License Agreement (EULA).
- **No Warranty**: The build scripts are provided "as is" under the MIT License. Use them at your own risk.
