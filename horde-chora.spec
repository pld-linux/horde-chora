%include	/usr/lib/rpm/macros.php
Summary:	Web Based CVS Program
Summary(pl):	Program do obs³ugi CVS przez WWW
Name:		chora
Version:	2.0
Release:	0.16
License:	GPL v2
Group:		Networking/Utilities
Source0:	ftp://ftp.horde.org/pub/chora/%{name}-h3-%{version}.tar.gz
# Source0-md5:	11f4b8ad6e0706026aefd0ee29eff7a5
Source1:	%{name}.conf
URL:		http://www.horde.org/chora/
Requires:	apache >= 1.3.33-2
# well. depending on configuration, it needs cvs, rcs or svn, cvsps
Requires:	cvs
Requires:	rcs
Requires:	horde >= 3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{name}
%define		_sysconfdir	/etc/horde.org
%define		_apache1dir	/etc/apache
%define		_apache2dir	/etc/httpd

%description
Chora is the CVS viewing frontend, one of the Horde components. It
provides webmail access to CVS repositories.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with IMP) please visit <http://www.horde.org/>.

%description -l pl
Chora jest programem do obs³ugi CVS przez WWW, bazowanym na Horde.
Daje dostêp do zasobów CVS z wygodnym interfejsem WWW.

Projekt Horde tworzy aplikacje w PHP i dostarcza je na licencji GNU
Public License. Je¿eli chcesz siê dowiedzieæ czego¶ wiêcej (tak¿e help
do IMP-a) zajrzyj na stronê <http://www.horde.org/>.

%prep
%setup -q -n %{name}-h3-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	$RPM_BUILD_ROOT%{_appdir}/{lib,locale,templates,themes}

cp -pR	*.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -p $i $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$(basename $i .dist)
done
cp -pR	config/*.xml		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}

echo "<?php ?>" > 		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php
sed -e '
	s,/usr/local/bin/cvsps,/usr/bin/cvsps,
	s,dirname(__FILE__).*/cvsgraph.conf.,%{_sysconfdir}/%{name}/cvsgraph.conf,
' < config/conf.xml > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.xml
> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php.bak

cp -pR  lib/*                   $RPM_BUILD_ROOT%{_appdir}/lib
cp -pR  locale/*                $RPM_BUILD_ROOT%{_appdir}/locale
cp -pR  templates/*             $RPM_BUILD_ROOT%{_appdir}/templates
cp -pR  themes/*                $RPM_BUILD_ROOT%{_appdir}/themes

ln -s	%{_sysconfdir}/%{name} 	$RPM_BUILD_ROOT%{_appdir}/config
install %{SOURCE1} 		$RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
# apache1
if [ -d %{_apache1dir}/conf.d ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache1dir}/conf.d/99_%{name}.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi
# apache2
if [ -d %{_apache2dir}/httpd.conf ]; then
	ln -sf %{_sysconfdir}/apache-%{name}.conf %{_apache2dir}/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%postun
if [ "$1" = "0" ]; then
	# apache1
	if [ -d %{_apache1dir}/conf.d ]; then
		rm -f %{_apache1dir}/conf.d/99_%{name}.conf
		if [ -f /var/lock/subsys/apache ]; then
			/etc/rc.d/init.d/apache restart 1>&2
		fi
	fi
	# apache2
	if [ -d %{_apache2dir}/httpd.conf ]; then
		rm -f %{_apache2dir}/httpd.conf/99_%{name}.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/etc/rc.d/init.d/httpd restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc README docs/*
%attr(770,root,http) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{name}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{name}/conf.php
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/[^c]*.php
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/*.txt
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/*.conf
%ghost %{_sysconfdir}/%{name}/*.php.bak
%attr(640,root,http) %{_sysconfdir}/%{name}/*.xml

%dir %{_appdir}
%{_appdir}/config
%{_appdir}/*.php
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
