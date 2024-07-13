#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.4
%define		qtver		5.15.2
%define		kfname		kcontacts
Summary:	kcontacts
Name:		kf6-%{kfname}
Version:	6.4.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	abea6bacf5722aeb26d6beca69f626b3
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kcodecs-devel >= %{version}
BuildRequires:	kf6-kconfig-devel >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	kf6-ki18n-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	ka5-kcontacts < 20.12.3
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Address book API based on KDE Frameworks.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-kcontacts-devel < 20.12.3
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.


%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%{_datadir}/qlogging-categories6/kcontacts.categories
%{_datadir}/qlogging-categories6/kcontacts.renamecategories
%ghost %{_libdir}/libKF6Contacts.so.6
%attr(755,root,root) %{_libdir}/libKF6Contacts.so.*.*
%dir %{_libdir}/qt6/qml/org/kde/contacts
%{_libdir}/qt6/qml/org/kde/contacts/kcontactsqml.qmltypes
%{_libdir}/qt6/qml/org/kde/contacts/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/contacts/libkcontactsqml.so
%{_libdir}/qt6/qml/org/kde/contacts/qmldir

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KContacts
%{_libdir}/cmake/KF6Contacts
%{_libdir}/libKF6Contacts.so
