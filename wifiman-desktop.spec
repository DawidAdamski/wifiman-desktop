Name:           wifiman-desktop
Version:        %{_version}
Release:        1%{?dist}
Summary:        Ubiquiti WiFiman Desktop (Fedora Repack)
License:        Proprietary
BuildArch:      x86_64
AutoReqProv:    no

%description
WiFiman Desktop for Fedora. Includes Teleport (WireGuard) fixes.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/lib/wifiman-desktop
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/icons/hicolor
mkdir -p %{buildroot}%{_unitdir}

# Kopiowanie plików rozpakowanych przez CI
cp usr/bin/wifiman-desktop %{buildroot}/usr/bin/
cp -r usr/lib/wifiman-desktop/* %{buildroot}/usr/lib/wifiman-desktop/
cp -r usr/share/applications/* %{buildroot}/usr/share/applications/
cp -r usr/share/icons/hicolor/* %{buildroot}/usr/share/icons/hicolor/

# Naprawa serwisu systemd
mv %{buildroot}/usr/lib/wifiman-desktop/wifiman-desktop.service %{buildroot}%{_unitdir}/

%post
# SELinux: Nadajemy kontekst unconfined_exec_t, żeby Teleport mógł działać
if [ $1 -eq 1 ] ; then
    semanage fcontext -a -t unconfined_exec_t "/usr/lib/wifiman-desktop/wifiman-desktopd" 2>/dev/null || :
    semanage fcontext -a -t unconfined_exec_t "/usr/lib/wifiman-desktop/wireguard-go" 2>/dev/null || :
    restorecon -Rv /usr/lib/wifiman-desktop/ 2>/dev/null || :
fi
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%files
%attr(0755, root, root) /usr/bin/wifiman-desktop
/usr/lib/wifiman-desktop/
%{_unitdir}/wifiman-desktop.service
/usr/share/applications/wifiman-desktop.desktop
/usr/share/icons/hicolor/*/apps/wifiman-desktop.png

