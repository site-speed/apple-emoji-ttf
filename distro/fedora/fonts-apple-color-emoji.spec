# Fedora/RHEL RPM spec for Apple Color Emoji TTF
# See https://github.com/samuelngs/apple-emoji-ttf

Name:           fonts-apple-color-emoji
Version:        1.0.0
Release:        1%{?dist}
Summary:        Apple Color Emoji as CBDT/CBLC TTF for Linux

License:        custom
URL:            https://github.com/samuelngs/apple-emoji-ttf
Source0:        AppleColorEmoji.ttf
Source1:        50-apple-color-emoji.conf

BuildArch:      noarch
Requires:       fontconfig

%description
Brings Apple's vibrant color emojis to Linux. Installs the font and a
fontconfig snippet (50-apple-color-emoji.conf) so Apple Color Emoji is
preferred for emoji, serif, sans-serif, and monospace.

%prep
# Sources are copied into build dir by CI; no unpack needed

%build
# No compilation

%install
install -d %{buildroot}%{_datadir}/fonts/truetype/apple-color-emoji
install -m644 %{SOURCE0} %{buildroot}%{_datadir}/fonts/truetype/apple-color-emoji/
install -d %{buildroot}%{_sysconfdir}/fonts/conf.d
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/fonts/conf.d/

%files
%{_datadir}/fonts/truetype/apple-color-emoji/AppleColorEmoji.ttf
%{_sysconfdir}/fonts/conf.d/50-apple-color-emoji.conf

%post
/usr/bin/fc-cache -f

%postun
if [ $1 -eq 0 ]; then
  /usr/bin/fc-cache -f
fi

%changelog
* Mon Jan 01 2024 samuelngs <samuelngs@users.noreply.github.com> - 1.0.0-1
- Initial release.
