Summary:	An open-source eCommerce platform focused on flexibility and control
Name:		magento
Version:	1.4.0.0
Release:	0.1
License:	Open Software License
Group:		Applications/WWW
URL:		http://www.magentocommerce.com/
Source0:	http://www.magentocommerce.com/downloads/assets/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	74bba43bf8f5429fb26797be3fefbf0f
Source2:	%{name}-crontab
Source3:	%{name}-cron_disabled.php
Source4:	%{name}-cron_import.php
Source5:	%{name}-cron_export.php
Patch0:		%{name}-1.3.2.3-php43.patch
Patch1:		%{name}-1.3.2.1-categories_id.patch
Patch2:		%{name}-1.3.2.1-cron_export_fix_lang.patch
Patch3:		%{name}-1.3.2.4-homelist_random.patch
Requires:	php-mysql
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
#%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
rm -rf app/.svn

cat <<'EOF' > apache.conf
Alias /magento %{_appdir}/magento
<Directory %{_appdir}/magento>
    AllowOverride All
    RewriteEngine On
    Order allow,deny
    Allow from All
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -a . $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

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
%{_appdir}/app/.htaccess
%{_appdir}/app/code/*
%{_appdir}/app/design/*
%attr(775,root,http) %config(noreplace) %{_appdir}/app/etc/*
%{_appdir}/app/locale/*
%{_appdir}/app/Mage.php
%dir %{_appdir}/downloader
%{_appdir}/downloader/*
%{_appdir}/downloader/.htaccess
%{_appdir}/includes/config.php
%{_appdir}/includes/.htaccess
%{_appdir}/index.php.sample
%{_appdir}/media/downloadable/.htaccess
%{_appdir}/media/.htaccess
%dir %{_appdir}/pkginfo
%{_appdir}/pkginfo/*
%{_appdir}/pkginfo/.htaccess
#%dir %{_appdir}/report
#%{_appdir}/report/*
#%{_appdir}/report/.htaccess
%{_appdir}/shell/*.php
%dir %{_appdir}/skin
%{_appdir}/skin/*
%dir %{_appdir}/js
%{_appdir}/js/*
%dir %{_appdir}/install.php
%dir %{_appdir}/lib
%dir %{_appdir}/lib/.htaccess
%{_appdir}/lib/*
%attr(775,root,http) %dir %{_appdir}/media
%attr(775,root,http) %dir %{_appdir}/var
%attr(664,root,http) %{_appdir}/var/.htaccess
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
%{_appdir}/.htaccess
