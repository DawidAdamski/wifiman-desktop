Name:           wifiman-desktop
Version:        %{_version}
Release:        1%{?dist}
Summary:        Ubiquiti WiFiman Desktop (Fedora Repack)
License:        Proprietary
BuildArch:      x86_64
AutoReqProv:    no
BuildRequires: systemd-rpm-macros

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

cp ${_ws}/wifiman_policy.pp ${buildroot}/usr/lib/wifiman-desktop/wifiman_policy.pp

# Przeniesienie serwisu
mv %{buildroot}/usr/lib/wifiman-desktop/wifiman-desktop.service %{buildroot}%{_unitdir}/

%post
# 1. SELinux: Rejestracja etykiet
semanage fcontext -a -t unconfined_exec_t "/usr/lib/wifiman-desktop/wifiman-desktopd" 2>/dev/null || :
semanage fcontext -a -t unconfined_exec_t "/usr/lib/wifiman-desktop/wireguard-go" 2>/dev/null || :
restorecon -Rv /usr/lib/wifiman-desktop/ >/dev/null 2>&1 || :
semodule -i /usr/lib/wifiman-desktop/wifiman_policy.pp 2>/dev/null || :

# 2. Capabilities dla Teleportu
setcap 'cap_net_admin,cap_net_raw+ep' /usr/lib/wifiman-desktop/wifiman-desktopd 2>/dev/null || :
setcap 'cap_net_admin,cap_net_raw+ep' /usr/lib/wifiman-desktop/wireguard-go 2>/dev/null || :

# 3. Systemd: Rejestracja i automatyczny start
%systemd_post wifiman-desktop.service
# Wymuszamy start, żeby GUI od razu działało
/usr/bin/systemctl enable --now wifiman-desktop.service >/dev/null 2>&1 || :


%preun
# Zatrzymanie serwisu przed odinstalowaniem
%systemd_preun wifiman-desktop.service

%postun
# Przeładowanie systemd po odinstalowaniu
%systemd_postun_with_restart wifiman-desktop.service

%files
%attr(0755, root, root) /usr/bin/wifiman-desktop
/usr/lib/wifiman-desktop/
%{_unitdir}/wifiman-desktop.service
/usr/share/applications/wifiman-desktop.desktop
/usr/share/icons/hicolor/*/apps/wifiman-desktop.png
/usr/lib/wifiman-desktop/wifiman_policy.pp

%changelog
* Sun Feb 15 2026 Dawid <dawid@example.com> - 1.2.8-1
- Fix build paths and add SELinux contexts

