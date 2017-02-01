Summary:	Yubikey tool for generating OATH event-based HOTP and time-based TOTP codes
Name:		yubioath-desktop
Version:	3.1.0
Release:	1
License:	GPL v3+
Group:		X11/Applications
URL:		https://developers.yubico.com/yubioath-desktop/
Source0:	https://developers.yubico.com/yubioath-desktop/Releases/%{name}-%{version}.tar.gz
# Source0-md5:	2b36482fc4ecd5edf8cc4d72716bdef4
BuildRequires:	asciidoc
BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
Requires:	pcsc-driver-ccid
Requires:	python-PySide
Requires:	pythonegg(click)
Requires:	ykpers
Requires(post):	desktop-file-utils
Requires(postun):	desktop-file-utils
BuildArch:	noarch

%description
The Yubico Authenticator is a graphical desktop tool and CLI for
generating Open AuTHentication (OATH) event-based HOTP and time-based
TOTP one-time password codes, with the help of a YubiKey that protects
the shared secrets.

%prep
%setup -q

%build
%{py_build}

for m in man/*.adoc; do
	a2x -f manpage "$m"
done

%install
rm -rf $RPM_BUILD_ROOT
%{py_install}

# man pages
install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

# desktop file
desktop-file-install --dir=$RPM_BUILD_ROOT%{_desktopdir} %{_builddir}/%{buildsubdir}/resources/yubioath.desktop

# icons
install -d $RPM_BUILD_ROOT%{_pixmapsdir}
cp %{_builddir}/%{buildsubdir}/resources/yubioath.xpm $RPM_BUILD_ROOT%{_pixmapsdir}
install -d $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps
cp %{_builddir}/%{buildsubdir}/resources/yubioath-desktop.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database

%postun
if [ $1 -eq 0 ] ; then
	%update_icon_cache hicolor
fi
%update_desktop_database

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/yubioath
%attr(755,root,root) %{_bindir}/yubioath-gui
%{py_sitescriptdir}/yubioath
%{py_sitescriptdir}/yubioath_desktop*.egg-info
%{_desktopdir}/yubioath.desktop
%{_iconsdir}/hicolor/128x128/apps/yubioath-desktop.png
%{_pixmapsdir}/yubioath.xpm
%{_mandir}/man1/yubioath-gui.1*
%{_mandir}/man1/yubioath.1*
