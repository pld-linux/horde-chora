Summary:	Web Based CVS Program
Summary(pl):	Program do obs³ugi CVS przez WWW
Name:		chora
Version:	1.0
Release:	1
License:	GPL v2
Group:		Networking/Utilities
Source0:	ftp://ftp.horde.org/pub/chora/tarballs/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
URL:		http://www.horde.org/chora
Requires:	cvs
Requires:	horde >= 2.0
Prereq:		perl
Prereq:		webserver
BuildArch:	noarch
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apachedir	/etc/httpd
%define		contentdir	/home/httpd

%description
Chora is the CVS viewing frontend, one of the Horde components. It
provides webmail access to CVS repositories.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with IMP) please visit http://www.horde.org/.

%description -l pl
Chra jest programem do obs³ugi CVS przez www, bazowanym na Horde.
Daje dostêp do zasobów CVS z wygodnym interfejsem www.

Projekt Horde tworzy aplikacje w PHP i dostarcza je na licencji GNU
Public License. Je¿eli chcesz siê dowiedzieæ czego¶ wiêcej (tak¿e help
do IMP'a) zajrzyj na stronê http://www.horde.org

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{apachedir}/
install -d $RPM_BUILD_ROOT%{contentdir}/html/horde/%{name}/{config,graphics,lib,locale,templates}

install %{SOURCE1} 		$RPM_BUILD_ROOT%{apachedir}
cp -pR	*.php			$RPM_BUILD_ROOT%{contentdir}/html/horde/%{name}
cp -pR	config/*.dist		$RPM_BUILD_ROOT%{contentdir}/html/horde/%{name}/config

for i in graphics lib locale templates; do
	cp -pR	$i/*		$RPM_BUILD_ROOT%{contentdir}/html/horde/%{name}/$i
done
for i in config lib locale templates; do
	cp -p	$i/.htaccess	$RPM_BUILD_ROOT%{contentdir}/html/horde/%{name}/$i
done

ln -sf	%{contentdir}/html/horde/%{name}/config $RPM_BUILD_ROOT%{apachedir}/%{name}

gzip -9nf README docs/* config/README

cd $RPM_BUILD_ROOT%{contentdir}/html/horde/%{name}/config/
for i in *.dist; do cp $i `basename $i .dist`; done

%clean
rm -rf $RPM_BUILD_ROOT

%post
grep -i 'Include.*%{name}.conf$' %{apachedir}/httpd.conf >/dev/null 2>&1
echo "Changing apache configuration"
if [ $? -eq 0 ]; then
	perl -pi -e 's/^#+// if (/Include.*%{name}.conf$/i);' %{apachedir}/httpd.conf
else
	echo "Include %{apachedir}/%{name}.conf" >>%{apachedir}/httpd.conf
fi

if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start http daemon."
fi


%postun
echo "Changing apache configuration"
perl -pi -e 's/^/#/ if (/^Include.*%{name}.conf$/i);' %{apachedir}/httpd.conf
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start http daemon."
fi

%files
%defattr(644,root,root,755)
%doc *.gz docs/*.gz config/*.gz

%dir %{contentdir}/html/horde/%{name}
%attr(640,root,http) %{contentdir}/html/horde/%{name}/*.php
%attr(750,root,http) %{contentdir}/html/horde/%{name}/graphics
%attr(750,root,http) %{contentdir}/html/horde/%{name}/lib
%attr(750,root,http) %{contentdir}/html/horde/%{name}/locale
%attr(750,root,http) %{contentdir}/html/horde/%{name}/templates

%attr(750,root,http) %dir %{contentdir}/html/horde/%{name}/config
%attr(640,root,http) %{contentdir}/html/horde/%{name}/config/*.dist
%attr(640,root,http) %{contentdir}/html/horde/%{name}/config/.htaccess
%attr(640,root,http) %config(noreplace) %{apachedir}/%{name}.conf
%attr(640,root,http) %config(noreplace) %{contentdir}/html/horde/%{name}/config/*.php
%attr(640,root,http) %config(noreplace) %{contentdir}/html/horde/%{name}/config/*.txt
%{apachedir}/%{name}
