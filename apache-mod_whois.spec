%define		mod_name	whois
%define		ver		0.1
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: WHOIS->WEB gateway
Summary(pl):	Modu³ Apache'a: bramka WHOIS->WWW
Name:		apache-mod_%{mod_name}
Version:	%{ver}
Release:	0.1
License:	distributable
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modwhois/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	8b4f29868c221b2d54f59b7a0c090698
Source1:	%{name}.conf
URL:		http://modwhois.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.0
Requires(post,preun):	%{apxs}
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
Apache module: WHOIS->WEB gateway.

%description -l pl
Modu³ Apache'a: bramka WHOIS->WWW.

%prep
%setup -q -n mod_%{mod_name}

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/httpd/httpd.conf,%{_pkglibdir}}

libtool --mode=install install mod_%{mod_name}.la $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/83_mod-whois.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_pkglibdir}/*.so
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/httpd.conf/*.conf
