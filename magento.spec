# TODO
# - writable dirs: Ensure that the directories app/etc, var, and media are writable by the web server
%include	/usr/lib/rpm/macros.php
%define		php_min_version 5.2.0
Summary:	An open-source eCommerce platform focused on flexibility and control
Name:		magento
Version:	1.4.1.1
Release:	0.8
License:	Open Software License (OSL 3.0)
Group:		Applications/WWW
URL:		http://www.magentocommerce.com/
Source0:	http://www.magentocommerce.com/downloads/assets/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	319882ad9eaef8b7312071ba48a8045a
Source1:	apache.conf
Source2:	%{name}-crontab
Source3:	%{name}-cron_disabled.php
Source4:	%{name}-cron_import.php
Source5:	%{name}-cron_export.php
Patch0:		%{name}-1.3.2.3-php43.patch
Patch1:		%{name}-1.3.2.1-categories_id.patch
Patch2:		%{name}-1.3.2.1-cron_export_fix_lang.patch
Patch3:		%{name}-1.3.2.4-homelist_random.patch
Patch4:		pld-mysql-root.patch
Patch5:		amcustomerattr-optional.patch
Patch6:		local.xml-empty.patch
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-ctype
Requires:	php-curl
Requires:	php-dom
Requires:	php-gd
Requires:	php-hash
Requires:	php-iconv
Requires:	php-mcrypt
Requires:	php-mhash
Requires:	php-mhash
Requires:	php-pdo-mysql
Requires:	php-simplexml
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(indexfile)
Requires:	webserver(php)
Requires:	webserver(rewrite)
Suggests:	php-pecl-APC
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

# lib/3Dsecure
%define		libs_3dsecure	pear(XMLParser.php)
%define		libs_mage		pear(3Dsecure/CentinelClient.php) pear(CentinelErrors.php) pear(CreateController.php) pear(ProfileController.php) pear(Rijndael.php) pear(Varien.*.php) pear(abstract.php) pear(Mage.*.php) pear(Maged/.*.php) pear(app/Mage.php) pear(google.*.php) pear(lib/Varien/.*.php) pear(phpseclib/Crypt/.*) pear(phpseclib/Math/.*) pear(phpseclib/Net/.*) pear(processor.php) pear(xml-processing/.*.php)
%define		libs_pear		pear(Crypt/DES.php) pear(Crypt/Hash.php) pear(Crypt/Random.php) pear(Crypt/TripleDES.php) pear(Math/BigInteger.php) pear(Crypt/RSA.php)
%define		_noautopear		%{libs_mage} %{libs_pear} %{libs_3dsecure}

# exclude optional php dependencies
%define		_noautophp	%{nil}

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
An open-source eCommerce platform focused on flexibility and control.

%package setup
Summary:	Magento setup package
Summary(pl.UTF-8):	Pakiet do wstępnej konfiguracji Magento
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
Install this package to configure initial Magento installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować w celu wstępnej konfiguracji Magento po
pierwszej instalacji. Potem należy go odinstalować, jako że
pozostawienie plików instalacyjnych mogłoby być niebezpieczne.

%prep
%setup -qc
mv %{name}/{.??*,*} . && rmdir %{name}

# use system Zend, magento has bundled ZF somewhere between versions 1.9.6 and 1.9.7
rm -r lib/Zend

# php-pear-PEAR 1.7.2
rm lib/PEAR/PEAR.php
rm -r lib/PEAR/PEAR

# php-pear-HTTP 1.4.1
rm lib/PEAR/HTTP/HTTP.php

# php-pear-HTTP_Request 1.4.4
rm lib/PEAR/HTTP/Request.php
rm -r lib/PEAR/HTTP/Request

# php-pear-Mail_Mime 1.5.2
rm lib/PEAR/Mail/mime.php
rm lib/PEAR/Mail/mimePart.php
rm lib/PEAR/Mail/xmail.{dtd,xsl}

# php-pear-Mail_mimeDecode 1.5.0
rm lib/PEAR/Mail/mimeDecode.php

# php-pear-Net_URL 1.0.15
rm lib/PEAR/Net/URL.php

# php-pear-Net_Socket 1.0.9
rm lib/PEAR/Net/Socket.php

# php-pear-SOAP-0.12.0-1.noarch
rm -r lib/PEAR/SOAP

# php-pear-XML_Parser 1.3.2
rm lib/PEAR/XML/Parser.php
rm lib/PEAR/XML/Parser/Simple.php
rmdir lib/PEAR/XML/Parser

# php-pear-XML_Serializer 0.19.2
rm lib/PEAR/XML/Serializer.php
rm lib/PEAR/XML/Unserializer.php

rmdir lib/PEAR/{HTTP,Mail,Net}

%undos -f php,phtml
#%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

# include default config in package files (empty so it can be treated as missing)
> app/etc/local.xml

# make docs to pack
install -d doc
mv RELEASE_NOTES.txt doc
mv LICENSE*.txt doc
mv *sample doc
mv .htaccess.sample doc/htaccess.sample

# contents included in apache.conf
find -name .htaccess | xargs rm

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -a . $RPM_BUILD_ROOT%{_appdir}
rm -rf $RPM_BUILD_ROOT%{_appdir}/doc
rm -f $RPM_BUILD_ROOT%{_appdir}/debug*.list

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
%doc doc/*
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
%dir %attr(775,root,http) %{_appdir}/app/etc
%dir %attr(775,root,http) %{_appdir}/app/etc/modules
%attr(664,root,http) %config(noreplace) %verify(not md5 mtime size) %{_appdir}/app/etc/config.xml
%attr(664,root,http) %config(noreplace) %verify(not md5 mtime size) %{_appdir}/app/etc/local.xml*
%attr(664,root,http) %config(noreplace) %verify(not md5 mtime size) %{_appdir}/app/etc/modules/*.xml
%dir %{_appdir}/app/locale
%{_appdir}/app/locale/*
%{_appdir}/app/Mage.php
%dir %{_appdir}/includes
%{_appdir}/includes/config.php
#%dir %{_appdir}/report
#%{_appdir}/report/*
%dir %{_appdir}/shell
%{_appdir}/shell/*.php
%dir %{_appdir}/skin
%{_appdir}/skin/*
%dir %{_appdir}/js
%{_appdir}/js/*
%dir %{_appdir}/lib
%{_appdir}/lib/3Dsecure
%{_appdir}/lib/flex
%{_appdir}/lib/googlecheckout
%{_appdir}/lib/LinLibertineFont
%{_appdir}/lib/PEAR
%{_appdir}/lib/phpseclib
%{_appdir}/lib/Varien
#%{_appdir}/lib/Zend
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
#%{_appdir}/STATUS.txt

%files setup
%defattr(644,root,root,755)
%{_appdir}/LICENSE.html
%attr(755,root,root) %{_appdir}/pear
%dir %{_appdir}/install.php
%dir %{_appdir}/downloader
%{_appdir}/downloader/*
%dir %{_appdir}/pkginfo
%{_appdir}/pkginfo/*
