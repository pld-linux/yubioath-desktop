Summary:	Yubikey tool for generating OATH event-based HOTP and time-based TOTP codes
Summary(pl.UTF-8):	Narzędzie Yubikey do generowania kodów OATH opartych na zdarzeniach (HOTP) i czasie (TOTP)
Name:		yubioath-desktop
Version:	4.3.4
Release:	1
License:	BSD
Group:		X11/Applications
Source0:	https://developers.yubico.com/yubioath-desktop/Releases/%{name}-%{version}.tar.gz
# Source0-md5:	a4a18ba12d8ce63e94f0c0af80194a8a
URL:		https://developers.yubico.com/yubioath-desktop/
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Qml-devel >= 5
BuildRequires:	Qt5Quick-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	desktop-file-utils
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5
Requires(post,postun):	desktop-file-utils
Requires:	pcsc-driver-ccid
Requires:	python-PySide
Requires:	yubikey-manager
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Yubico Authenticator is a graphical desktop tool and CLI for
generating Open AuTHentication (OATH) event-based HOTP and time-based
TOTP one-time password codes, with the help of a YubiKey that protects
the shared secrets.

%description -l pl.UTF-8
Yubico Authenticator to narzędzie graficzne oraz linii poleceń do
generowania kodów jednorazowych haseł OATH (Open AuTHentication)
opartych na zdarzeniach (HOTP) i czasie (TOTP) z pomocą urządzenia
YubiKey, które zabezpiecza współdzielone dane prywatne.

%prep
%if 0
%setup -q
%else
# 4.3.4 tarball is broken (pure tar saved as .tar.gz)
%setup -q -c -T -n %{name}
%{__tar} xf %{SOURCE0} -C ..
%endif

%build
qmake-qt5 \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	STRIP=:

# desktop file
desktop-file-install --dir=$RPM_BUILD_ROOT%{_desktopdir} resources/yubioath-desktop.desktop
# icons
install -d $RPM_BUILD_ROOT%{_pixmapsdir}
cp -p resources/icons/yubioath.png $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%postun
%update_desktop_database

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README
%attr(755,root,root) %{_bindir}/yubioath-desktop
%{_desktopdir}/yubioath-desktop.desktop
%{_pixmapsdir}/yubioath.png
