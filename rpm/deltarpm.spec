# fixme: should be defined in base system side
%define python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

Summary: Create deltas between rpms
Name: deltarpm
Version: 3.6.3
Release: 1
License: BSD
URL: https://github.com/rpm-software-management/deltarpm
Source: %{name}-%{version}.tar.bz2
BuildRequires: bzip2-devel, xz-devel
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(rpm)
BuildRequires: pkgconfig(popt)
BuildRequires: pkgconfig(python3)
BuildRequires: pkgconfig(libzstd)

%description
A deltarpm contains the difference between an old
and a new version of a rpm, which makes it possible
to recreate the new rpm from the deltarpm and the old
one. You don't have to have a copy of the old rpm,
deltarpms can also work with installed rpms.

%package -n drpmsync
Summary: Sync a file tree with deltarpms
Requires: deltarpm = %{version}-%{release}

%description -n drpmsync
This package contains a tool to sync a file tree with
deltarpms.

%package -n deltaiso
Summary: Create deltas between isos containing rpms
Requires: deltarpm = %{version}-%{release}

%description -n deltaiso
This package contains tools for creating and using deltasisos,
a difference between an old and a new iso containing rpms.

%package -n python3-%{name}
Summary: Python bindings for deltarpm
Requires: deltarpm = %{version}-%{release}

%description -n python3-%{name}
This package contains python bindings for deltarpm.

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}

%description doc
Man and info pages for %{name}.

%prep
%autosetup -n %{name}-%{version}/deltarpm -p1

%build
export PYTHONS=python3
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -DWITH_ZSTD=1" \
    bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
    zlibbundled='' zlibldflags='-lz' zlibcppflags='' \
    all python

%install
%{__rm} -rf %{buildroot}
export PYTHONS=python3
%{__make} DESTDIR=%{buildroot} INSTALL_ROOT=%{buildroot} \
    prefix="%{_prefix}" libdir="%{_libdir}" mandir=%{_mandir} \
    install

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} README

%files
%defattr(-, root, root, 0755)
%license LICENSE.BSD
%{_bindir}/applydeltarpm
%{_bindir}/combinedeltarpm
%{_bindir}/makedeltarpm
%{_bindir}/rpmdumpheader

%files -n deltaiso
%defattr(-, root, root, 0755)
%license LICENSE.BSD
%{_bindir}/applydeltaiso
%{_bindir}/fragiso
%{_bindir}/makedeltaiso

%files -n drpmsync
%defattr(-, root, root, 0755)
%license LICENSE.BSD
%{_bindir}/drpmsync

%files -n python3-%{name}
%defattr(-, root, root, 0755)
%license LICENSE.BSD
%{python3_sitearch}/%{name}.py
%{python3_sitearch}/_%{name}module.so
%{python3_sitearch}/__pycache__/*

%files doc
%defattr(-,root,root,-)
%{_mandir}/man8/*.*
%{_docdir}/%{name}-%{version}
