%global	php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl:		%{expand:	%%global __pecl	%{_bindir}/pecl}}
%{!?php_extdir:	%{expand:	%%global php_extdir	%(php-config --extension-dir)}}

%global basepkg   php55w
%define	pecl_name	imagick

Summary:		Provides a wrapper to the ImageMagick library
Name:		%{basepkg}-pecl-%{pecl_name}
Version:		2.2.2
Release:		4%{?dist}
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

%prep
%setup -qc

%build
cd %{pecl_name}-%{version}
phpize
%{configure} --with-%{pecl_name}
%{__make}

%install
rm -rf %{buildroot}

cd %{pecl_name}-%{version}

%{__make} install \
	INSTALL_ROOT=%{buildroot}

# Install XML package description
install -m 0755 -d %{buildroot}%{pecl_xmldir}
install -m 0664 ../package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml
install -d %{buildroot}%{_sysconfdir}/php.d/
install -m 0664 %{SOURCE1} %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini

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
%{_libdir}/php/modules/%{pecl_name}.so
%{pecl_xmldir}/%{pecl_name}.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php.d/%{pecl_name}.ini

%changelog
* Sun Jul 27 2014 Andy Thompson <andy@webtatic.com> - 2.2.2-1
- Import spec from EPEL 6 php-pecl-imagick-2.2.2-4
- Update to have php55w prefix