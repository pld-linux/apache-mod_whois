%define		mod_name	whois
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: WHOIS->WEB gateway
Summary(pl):	Modu� Apache'a: bramka WHOIS->WWW
Name:		apache-mod_%{mod_name}
Version:	0.1
Release:	3
License:	distributable
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modwhois/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	8b4f29868c221b2d54f59b7a0c090698
Source1:	%{name}.conf
URL:		http://modwhois.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apache >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
Apache module: WHOIS->WEB gateway.

%description -l pl
Modu� Apache'a: bramka WHOIS->WWW.

%prep
%setup -q -n mod_%{mod_name}

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/httpd.conf,%{_pkglibdir}}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/83_mod-whois.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_pkglibdir}/*.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*.conf
