#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	COIN-OR Utilities library
Summary(pl.UTF-8):	Biblioteka narzędziowa COIN-OR Utilities
Name:		CoinUtils
Version:	2.9.17
Release:	1
License:	Eclipse Public License v1.0
Group:		Libraries
Source0:	http://www.coin-or.org/download/source/CoinUtils/%{name}-%{version}.tgz
# Source0-md5:	e91ff822dc535055968094d88bcaabce
Patch0:		%{name}-format.patch
Patch1:		%{name}-destdir.patch
URL:		https://projects.coin-or.org/CoinUtils
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	blas-devel
BuildRequires:	bzip2-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	lapack-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CoinUtils (Coin-or Utilities) is an open-source collection of classes
and functions that are generally useful to more than one COIN-OR
project. These utilities include:
 - Vector classes
 - Matrix classes
 - MPS file reading
 - Comparing floating point numbers with a tolerance

%description -l pl.UTF-8
CoinUtils (Coin-or Utilities) to mający otwarte źródła zbiór klas i
funkcji ogólnie przydatnych dla więcej niż jednego projektu COIN-OR.
Narzędzia Coin-or zawirają:
 - klasy wektorów
 - klasy macierzy
 - odczyt plików MPS
 - porównywanie liczb zmiennoprzecinkowych z określoną dokładnością

%package devel
Summary:	Header files for CoinUtils library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CoinUtils
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	blas-devel
Requires:	bzip2-devel
Requires:	lapack-devel
Requires:	libstdc++-devel
Requires:	zlib-devel

%description devel
Header files for CoinUtils library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CoinUtils.

%package static
Summary:	Static CoinUtils library
Summary(pl.UTF-8):	Statyczna biblioteka CoinUtils
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CoinUtils library.

%description static -l pl.UTF-8
Statyczna biblioteka CoinUtils.

%package apidocs
Summary:	CoinUtils API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki CoinUtils
Group:		Documentation

%description apidocs
API documentation for CoinUtils library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki CoinUtils.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

ln -s ../BuildTools CoinUtils/BuildTools

%build
cd CoinUtils
%{__libtoolize}
%{__aclocal} -I BuildTools
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..
%configure \
	--enable-dependency-linking \
	%{?with_static_libs:--enable-static}
%{__make}

%if %{with apidocs}
%{__make} doxydoc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libCoinUtils.la
# packages as %doc
%{__rm} $RPM_BUILD_ROOT%{_datadir}/coin/doc/CoinUtils/{AUTHORS,LICENSE,README}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CoinUtils/{AUTHORS,LICENSE,README}
%attr(755,root,root) %{_libdir}/libCoinUtils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCoinUtils.so.3
%dir %{_datadir}/coin
%{_datadir}/coin/Data

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libCoinUtils.so
%dir %{_includedir}/coin
%{_includedir}/coin/CoinUtilsConfig.h
%{_includedir}/coin/Coin_C_defines.h
%{_includedir}/coin/Coin*.hpp
%{_pkgconfigdir}/coindatasample.pc
%{_pkgconfigdir}/coinutils.pc
%dir %{_datadir}/coin/doc
%dir %{_datadir}/coin/doc/CoinUtils
%{_datadir}/coin/doc/CoinUtils/coinutils_addlibs.txt

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libCoinUtils.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doxydoc/html/*
%endif
