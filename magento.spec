# TODO
# - writable dirs: Ensure that the directories app/etc, var, and media are writable by the web server
#include	/usr/lib/rpm/macros.php
%define		php_min_version 5.2.0
Summary:	An open-source eCommerce platform focused on flexibility and control
Name:		magento
Version:	1.4.0.0
Release:	0.3
License:	Open Software License (OSL 3.0)
Group:		Applications/WWW
URL:		http://www.magentocommerce.com/
Source0:	http://www.magentocommerce.com/downloads/assets/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	74bba43bf8f5429fb26797be3fefbf0f
Source1:	apache.conf
Source2:	%{name}-crontab
Source3:	%{name}-cron_disabled.php
Source4:	%{name}-cron_import.php
Source5:	%{name}-cron_export.php
Patch0:		%{name}-1.3.2.3-php43.patch
Patch1:		%{name}-1.3.2.1-categories_id.patch
Patch2:		%{name}-1.3.2.1-cron_export_fix_lang.patch
Patch3:		%{name}-1.3.2.4-homelist_random.patch
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-dom
Requires:	php-mcrypt
Requires:	php-mhash
Requires:	php-pdo-mysql
Requires:	php-simplexml
Suggests:	php-pecl-APC
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
An open-source eCommerce platform focused on flexibility and control.

%prep
%setup -q -n %{name}
%undos -f php
#%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
rm -rf app/.svn

# contents included in apache.conf
find -name .htaccess | xargs rm

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -a . $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_appdir}/crontab
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_appdir}/cron_disabled.php
cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_appdir}/cron_import.php
cp -a %{SOURCE5} $RPM_BUILD_ROOT%{_appdir}/cron_export.php

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%dir %{_appdir}
%{_appdir}/errors
%dir %{_appdir}/app
%dir %{_appdir}/app/code
%{_appdir}/app/code/*
%dir %{_appdir}/app/design
%{_appdir}/app/design/*
%dir %{_appdir}/app/etc
%attr(775,root,http) %config(noreplace) %{_appdir}/app/etc/*
%dir %{_appdir}/app/locale
%{_appdir}/app/locale/*
%{_appdir}/app/Mage.php
%dir %{_appdir}/downloader
%{_appdir}/downloader/*
%dir %{_appdir}/includes
%{_appdir}/includes/config.php
%{_appdir}/index.php.sample
%dir %{_appdir}/pkginfo
%{_appdir}/pkginfo/*
#%dir %{_appdir}/report
#%{_appdir}/report/*
%dir %{_appdir}/shell
%{_appdir}/shell/*.php
%dir %{_appdir}/skin
%{_appdir}/skin/*
%dir %{_appdir}/js
%{_appdir}/js/*
%dir %{_appdir}/install.php
%dir %{_appdir}/lib
%{_appdir}/lib/*
%attr(775,root,http) %dir %{_appdir}/media
%attr(775,root,http) %dir %{_appdir}/var
%{_appdir}/favicon.ico
%{_appdir}/cron.php
%{_appdir}/cron.sh
%{_appdir}/crontab
%{_appdir}/cron_disabled.php
%{_appdir}/cron_import.php
%{_appdir}/cron_export.php
%{_appdir}/index.php
%{_appdir}/LICENSE.txt
%{_appdir}/LICENSE.html
%{_appdir}/LICENSE_AFL.txt
#%{_appdir}/STATUS.txt
%{_appdir}/pear
%{_appdir}/php.ini.sample
