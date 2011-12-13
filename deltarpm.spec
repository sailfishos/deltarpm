%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Create deltas between rpms
Name: deltarpm
Version: 3.5
Release: 1
License: BSD
Group: System/Base
URL: http://gitorious.org/deltarpm/deltarpm
# Generate source by doing:
# git clone git://gitorious.org/deltarpm/deltarpm
# cd deltarpm
# git archive --format=tar --prefix="deltarpm-git-20090913" f716bb7 | \
# bzip2 > deltarpm-git-20090831.1.tar.bz2
Source: %{name}-git-20090913.tar.bz2
# Build with system zlib
Patch0: deltarpm-system-zlib.patch
Patch1: deltarpm-git-20090913-rpmio.patch

BuildRequires: bzip2-devel, xz-devel, rpm-devel, popt-devel
BuildRequires: zlib-devel
BuildRequires: python-devel

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

%package -n python-deltarpm
Summary: Python bindings for deltarpm
Requires: deltarpm = %{version}-%{release}

%description -n python-deltarpm
This package contains python bindings for deltarpm.

%prep
%setup -q -n %{name}-git-20090913
# Build with system zlib
%patch0 -p1 -b .zlib
%patch1 -p1

%build
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
    bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
    zlibbundled='' zlibldflags='-lz' zlibcppflags=''
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
    bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
    zlibbundled='' zlibldflags='-lz' zlibcppflags='' \
    python

%install
%{__rm} -rf %{buildroot}
%makeinstall

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/applydeltarpm*
%doc %{_mandir}/man8/makedeltarpm*
%doc %{_mandir}/man8/combinedeltarpm*
%{_bindir}/applydeltarpm
%{_bindir}/combinedeltarpm
%{_bindir}/makedeltarpm
%{_bindir}/rpmdumpheader

%files -n deltaiso
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/applydeltaiso*
%doc %{_mandir}/man8/makedeltaiso*
%{_bindir}/applydeltaiso
%{_bindir}/fragiso
%{_bindir}/makedeltaiso

%files -n drpmsync
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/drpmsync*
%{_bindir}/drpmsync

%files -n python-deltarpm
%defattr(-, root, root, 0755)
%doc LICENSE.BSD
%{python_sitearch}/*

