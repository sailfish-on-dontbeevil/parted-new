Summary: The GNU disk partition manipulation program
Name:    parted-new
Version: 3.6
Release: 0
License: GPL-3.0-or-later
URL:     http://www.gnu.org/software/parted

Source0: %{name}-%{version}.tar.bz2

Patch0: 0001-fix-sed-tests.patch
Patch1: 0002-disable-unicode-test.patch

BuildRequires: gcc
BuildRequires: e2fsprogs-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: gettext-devel
BuildRequires: texinfo
BuildRequires: device-mapper-devel
BuildRequires: libuuid-devel
BuildRequires: libblkid-devel >= 2.17
BuildRequires: gnupg2
BuildRequires: git
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: e2fsprogs
BuildRequires: dosfstools
BuildRequires: bc
BuildRequires: python3-base
BuildRequires: gperf
BuildRequires: make
BuildRequires: check-devel
BuildRequires: rsync

Provides:  parted
Obsoletes: parted <= 3.1

# bundled gnulib library exception, as per packaging guidelines
# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries
Provides: bundled(gnulib)

%description
The GNU Parted program allows you to create, destroy, resize, move,
and copy hard disk partitions. Parted can be used for creating space
for new operating systems, reorganizing disk usage, and copying data
to new hard disks.


%package devel
Summary:  Files for developing apps which will manipulate disk partitions
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The GNU Parted library is a set of routines for hard disk partition
manipulation. If you want to develop programs that manipulate disk
partitions and filesystems using the routines provided by the GNU
Parted library, you need to install this package.


%prep
%autosetup -p1 -n %{name}-%{version}/upstream
# Build fix - 'gets' is removed in C11
# Chose this over committing this change to Git because gnulib/ is a Git submodule
sed -i '/^_GL_WARN_ON_USE (gets,/s;^;//;' gnulib/lib/stdio.in.h

# This is normally generated from Git history. Cannot be done on OBS.
touch ChangeLog

./bootstrap --skip-po --no-git --gnulib-srcdir=gnulib

%build
%configure --disable-static --disable-device-mapper --with-readline --libdir=%{_libdir} --exec-prefix=/usr --disable-tests
%{__make} %{?_smp_mflags}

%make_build


%install
%{__rm} -rf %{buildroot}
%make_install

# Remove components we do not ship
%{__rm} -rf %{buildroot}%{_infodir}/dir
#%{__rm} -rf %{buildroot}%{_bindir}/label
#%{__rm} -rf %{buildroot}%{_bindir}/disk


%check
export LD_LIBRARY_PATH=$(pwd)/libparted/.libs:$(pwd)/libparted/fs/.libs
make check

%files
%doc AUTHORS NEWS README THANKS
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_sbindir}/parted
%{_sbindir}/partprobe
%{_mandir}/man8/parted.8*
%{_mandir}/man8/partprobe.8*
%{_libdir}/libparted.so.2
%{_libdir}/libparted.so.2.0.5
%{_libdir}/libparted-fs-resize.so.0
%{_libdir}/libparted-fs-resize.so.0.0.5
%{_infodir}/parted.info*

%files devel
%doc TODO doc/API doc/FAT
%{_includedir}/parted
%{_libdir}/libparted.so
%{_libdir}/libparted-fs-resize.so
%{_libdir}/pkgconfig/libparted.pc
%{_libdir}/pkgconfig/libparted-fs-resize.pc

