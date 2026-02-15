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

# Kopiowanie binarki GUI
cp %{_ws}/usr/bin/wifiman-desktop %{buildroot}/usr/bin/

# KLUCZOWA ZMIANA: Kropka po slashu kopiuje wszystko, w tym ukryte pliki .env
cp -a %{_ws}/usr/lib/wifiman-desktop/. %{buildroot}/usr/lib/wifiman-desktop/

# Reszta bez zmian
cp -r %{_ws}/usr/share/applications/* %{buildroot}/usr/share/applications/
cp -r %{_ws}/usr/share/icons/hicolor/* %{buildroot}/usr/share/icons/hicolor/

# Przeniesienie serwisu
mv %{buildroot}/usr/lib/wifiman-desktop/wifiman-desktop.service %{buildroot}%{_unitdir}/

%post
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

%changelog
* Sun Feb 15 2026 Dawid <dawid@example.com> - 1.2.8-1
- Fix build paths and add SELinux contexts

