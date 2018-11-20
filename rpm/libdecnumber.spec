Name:		libdecnumber
Version:	999.999
Release:	99999%{?dist}
Summary:	IEEE 754-2008 decimal library

Group:		Development/Libraries
License:	GPL3
URL:		https://github.com/raitechnology/%{name}
Source0:	%{name}-%{version}-99999.tar.gz
BuildRoot:	${_tmppath}
BuildArch:      x86_64
Prefix:	        /usr

%description
A IEEE 754-2008 decimal library pulled from gcc

%prep
%setup -q


%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0
%define _missing_build_ids_terminate_build 0
%define _include_gdb_index 1

%build
make build_dir=./usr %{?_smp_mflags} dist_bins
cp -a ./include ./usr/include

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}

# in builddir
cp -a * %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/usr/lib64/*
/usr/include/*

%post
echo "${RPM_INSTALL_PREFIX}/lib64" > /etc/ld.so.conf.d/libdecnumber.conf
ldconfig

%postun
rm -f /etc/ld.so.conf.d/libdecnumber.conf
ldconfig

%changelog
* __DATE__ <gchrisanderson@gmail.com>
- Hello world