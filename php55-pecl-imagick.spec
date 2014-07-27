%global	php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl:		%{expand:	%%global __pecl	%{_bindir}/pecl}}
%{!?php_extdir:	%{expand:	%%global php_extdir	%(php-config --extension-dir)}}

# Build ZTS extension or only NTS
%global with_zts      1

%global basepkg   php55w
%define	pecl_name	imagick

Summary:		Provides a wrapper to the ImageMagick library
Name:		%{basepkg}-pecl-%{pecl_name}
Version:		3.1.2
Release:		1%{?dist}
License:		PHP
Group:		Development/Libraries
Source0:		http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:		%{pecl_name}.ini
BuildRoot:	%{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
URL:			http://pecl.php.net/package/%{pecl_name}
BuildRequires:	%{basepkg}-pear >= 1.4.7
BuildRequires: %{basepkg}-devel >= 5.1.3, ImageMagick-devel >= 6.2.4
Requires(post):	%{__pecl}
Requires(postun):	%{__pecl}
%if %{?php_zend_api}0
Requires:		php(zend-abi) = %{php_zend_api}
Requires:		php(api) = %{php_core_api}
%else
Requires:		php-api = %{php_apiver}
%endif
Provides:		php-pecl(%{pecl_name}) = %{version}
Provides:               php-pecl-%{pecl_name} = %{version}

%description
%{pecl_name} is a native php extension to create and modify images using the
ImageMagick API.
This extension requires ImageMagick version 6.2.4+ and PHP 5.1.3+.

IMPORTANT: Version 2.x API is not compatible with earlier versions.

%package devel
Summary:       Imagick developer files (header)
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Requires:      %{basepkg}-devel
Provides:      php-pecl-imagick-devel = %{version}-%{release}

%description devel
These are the files needed to compile programs using Imagick.

%prep
%setup -qc

%if %{with_zts}
cp -r %{pecl_name}-%{version} %{pecl_name}-%{version}-zts
%endif

%build
pushd %{pecl_name}-%{version}
phpize
%configure --with-%{pecl_name} --with-php-config=%{_bindir}/php-config
%{__make} %{?_smp_mflags}
popd

%if %{with_zts}
pushd %{pecl_name}-%{version}-zts
zts-phpize
%configure --with-%{pecl_name} --with-php-config=%{_bindir}/zts-php-config
%{__make} %{?_smp_mflags}
popd
%endif

%install
rm -rf %{buildroot}

pushd %{pecl_name}-%{version}
%{__make} install \
	INSTALL_ROOT=%{buildroot}
popd

%if %{with_zts}
pushd %{pecl_name}-%{version}-zts
%{__make} install \
	INSTALL_ROOT=%{buildroot}
popd
%endif

# Install XML package description
install -m 0755 -d %{buildroot}%{pecl_xmldir}
install -m 0664 package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml
install -d %{buildroot}%{php_inidir}
install -m 0664 %{SOURCE1} %{buildroot}%{php_inidir}/%{pecl_name}.ini
%if %{with_zts}
install -d %{buildroot}%{php_ztsinidir}
install -m 0664 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini
%endif

%clean
rm -rf %{buildroot}

%post
%if 0%{?pecl_install:1}
%{pecl_install} %{pecl_xmldir}/%{pecl_name}.xml
%endif

%postun
%if 0%{?pecl_uninstall:1}
if [ "$1" -eq "0" ]; then
	%{pecl_uninstall} %{pecl_name}
fi
%endif

%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/examples %{pecl_name}-%{version}/{CREDITS,TODO,INSTALL}
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{pecl_name}.xml
%config(noreplace) %{php_inidir}/%{pecl_name}.ini

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%endif

%files devel
%{php_incldir}/ext/%{pecl_name}
%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif

%changelog
* Sun Jul 27 2014 Andy Thompson <andy@webtatic.com> - 3.1.2-1
- Import spec from EPEL 6 php-pecl-imagick-2.2.2-4
- Update to have php55w prefix
- Add ZTS compilation support
- Update to 3.1.2
- Add devel package to contain the header files