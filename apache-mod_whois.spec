%define		mod_name	whois
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: WHOIS->WEB gateway
Summary(pl.UTF-8):   Moduł Apache'a: bramka WHOIS->WWW
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
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
Apache module: WHOIS->WEB gateway.

%description -l pl.UTF-8
Moduł Apache'a: bramka WHOIS->WWW.

%prep
%setup -q -n mod_%{mod_name}

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/httpd.conf,%{_pkglibdir}}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/83_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
