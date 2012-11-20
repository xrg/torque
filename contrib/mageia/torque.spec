%define git_repo torque
%define git_head HEAD

%define         major              2
%define         libname            %mklibname %{name} %{major}
%define         devname            %mklibname -d %{name}

%define         clientname         %{name}-client
%define         servername         %{name}-server
%define         schedname          %{name}-sched
%define         momname            %{name}-mom
%define         guiname            %{name}-gui


#default is /var/spool/torque: if you change this, you'll break some
#scripts coming along with the source files
%define         torquedir          /var/spool/torque


Name:           torque
Summary:        The Torque resource and queue manager
Group:          System/Cluster
Version:        %git_get_ver
Release:        %mkrel %git_get_rel2
License:        TORQUEv1.1
URL:            http://www.clusterresources.com/products/torque-resource-manager.php

Source0:        %git_bs_source %{name}-%{version}.tar.gz

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  groff
BuildRequires:  groff-for-man
BuildRequires:  sed
BuildRequires:  xauth
BuildRequires:  gperf
BuildRequires:  graphviz
BuildRequires:  latex
BuildRequires:  doxygen
BuildRequires:  glibc-devel
BuildRequires:  binutils-devel
BuildRequires:  libncurses-devel
BuildRequires:  libreadline-devel
BuildRequires:  tk-devel
BuildRequires:  tcl-devel
#BuildRequires:  tclx-devel
BuildRequires:  openssh-clients
BuildRequires:  readline-devel
BuildRequires:  gcc-gfortran
BuildRequires:  gcc-c++
# BuildRequires:  quadmath-devel
BuildRequires:  pam-devel
BuildRequires:  openssl-devel
BuildRequires:  libxml2-devel
#BuildRequires:  hwloc
#BuildRequires:  hwloc-devel

Requires:       openssh-clients 
Suggests:       torque-mom

%description
The Tera-scale Open-source Resource and QUEue manager provides control
over batch jobs and distributed computing resources. It is an advanced
open-source product based on the original PBS project* and
incorporates the best of both community and professional
development. It incorporates significant advances in the areas of
scalability, reliability, and functionality and is currently in use at
tens of thousands of leading government, academic, and commercial
sites throughout the world.

"TORQUE is a modification of OpenPBS which was developed by NASA Ames
Research Center, Lawrence Livermore National Laboratory, and Veridian
Information Solutions, Inc. Visit www.clusterresources.com/products/
for more information about TORQUE and to download TORQUE".



%package -n     %{libname}
Summary:        Shared libraries for Torque
Group:          System/Libraries
Provides:       lib%{name} = %{version}-%{release}

%description -n %{libname}
%{summary}.



%package -n     %{devname}
Summary:        Development files for Torque
Group:          Development/Other
Requires:       %{libname} = %{version}-%{release}
Provides:       lib%{name}-devel  = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{devname}
%{summary}.



%package -n    %{clientname}
Summary:        Command line utilities for Torque
Group:          System/Cluster
Requires:       %{libname} = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}

%description -n %{clientname}
%{summary}.



%package -n     %{servername}
Summary:        The Torque server
Group:          System/Cluster
Requires:       %{libname} = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
Suggests:       %{schedname} = %{version}-%{release}
Requires(post): rpm-helper
Requires(preun):rpm-helper

%description -n %{servername}
%{summary}.



%package -n     %{schedname}
Summary:        The scheduler for Torque server
Group:          System/Cluster
Requires:       %{libname} = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
Requires:       %{servername} = %{version}-%{release}
Requires(post): rpm-helper
Requires(preun):rpm-helper

%description -n %{schedname}
%{summary}.



%package -n     %{momname}
Summary:        Node manager programs for Torque
Group:          System/Cluster
Requires:       %{libname} = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
Requires:       openssh-server
Requires(post): rpm-helper
Requires(preun):rpm-helper

%description -n %{momname}
%{summary}.  



%package -n     %{guiname}
Summary:        Graphical clients for Torque
Group:          Monitoring
Requires:       tk
Requires:       tcl
Requires:       %{libname} = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-client = %{version}-%{release}
Obsoletes:      torque-xpbs <= 2.5.3

%description -n %{guiname}
%{summary}.


%prep
%git_get_source
%setup -q


%build
%configure2_5x \
                --srcdir=%{_builddir}/%{name}-%{version} \
                --includedir=%{_includedir}/%{name} \
                --with-default-server=localhost \
                --with-pam=%{_libdir}/security \
                --with-rcp=scp \
                --with-hwloc-path=%{_prefix} \
                --enable-docs \
                --enable-server \
                --enable-mom \
                --enable-client \
                --enable-drmaa \
                --enable-high-availability \
                --enable-syslog \
                --enable-gui \
                --disable-static
#                --enable-numa-support \
#                --enable-cpuset \

%make all \
                XPBS_DIR=%{tcl_sitelib}/xpbs \
                XPBSMON_DIR=%{tcl_sitelib}/xpbsmon






%install
%makeinstall_std \
                PBS_SERVER_HOME=%{torquedir} \
                mandir=%_mandir \
                XPBS_DIR=%{tcl_sitelib}/xpbs \
                XPBSMON_DIR=%{tcl_sitelib}/xpbsmon


find %{buildroot}%{_libdir} -name *.la -delete

#yields various service to fail if relative symlinks
export DONT_RELINK=1

#install starting scripts
%__mkdir_p %{buildroot}%{_initrddir}
install -p -m 755 contrib/init.d/mageia.pbs_mom    %{buildroot}%{_initrddir}/pbs_mom
install -p -m 755 contrib/init.d/mageia.pbs_sched  %{buildroot}%{_initrddir}/pbs_sched
install -p -m 755 contrib/init.d/mageia.pbs_server %{buildroot}%{_initrddir}/pbs_server
#end starting scripts


#install config files: move them to /etc/torque
%__mkdir_p %{buildroot}%{_sysconfdir}/%{name}
pushd %{buildroot}%{torquedir}
%__mv server_name     %{buildroot}%{_sysconfdir}/%{name}
%__ln_s               %{_sysconfdir}/%{name}/server_name .
popd

pushd %{buildroot}%{torquedir}/server_priv
%__mv nodes %{buildroot}%{_sysconfdir}/%{name}
%__ln_s     %{_sysconfdir}/%{name}/nodes .
popd

pushd %{buildroot}%{torquedir}/sched_priv
%__mv sched_config   %{buildroot}%{_sysconfdir}/%{name}
%__mv dedicated_time %{buildroot}%{_sysconfdir}/%{name}
%__mv holidays       %{buildroot}%{_sysconfdir}/%{name}
%__mv resource_group %{buildroot}%{_sysconfdir}/%{name}
%__ln_s               %{_sysconfdir}/%{name}/sched_config .
%__ln_s               %{_sysconfdir}/%{name}/dedicated_time .
%__ln_s               %{_sysconfdir}/%{name}/holidays .
%__ln_s               %{_sysconfdir}/%{name}/resource_group .
popd

install -p -m 644 contrib/mageia/mom_config %{buildroot}%{_sysconfdir}/%{name}
pushd %{buildroot}%{torquedir}/mom_priv
%__ln_s -f %{_sysconfdir}/%{name}/mom_config config
popd
#end config files


#move drmaa man to the right place
%__mv %{buildroot}%{_defaultdocdir}/torque-drmaa/man/man3/* %{buildroot}%{_mandir}/man3/.
install -D -m 644 contrib/mageia/README.mga %{buildroot}%{_docdir}/%{name}/README.mga


#make symbolic links for tcl
pushd %{buildroot}%{_libdir}
%__ln_s -f %{tcl_sitelib}/xpbs    .
%__ln_s -f %{tcl_sitelib}/xpbsmon .
popd


#clean make install bugs the dirty way...
%__rm -f %{buildroot}%{_mandir}/man1/basl2c.1*
%__rm -f %{buildroot}%{_mandir}/man3/_*src_drmaa_src_.3*




%post
#update of /etc/services
CHECK_PORT=`grep 15003 /etc/services`
if [ -z "$CHECK_PORT" ]; then
          cat >> /etc/services << EOF
# Standard Torque/PBS services
pbs_server      15001/tcp   # pbs server
pbs_server      15001/udp   # pbs server
pbs_mom         15002/tcp   # mom to/from server
pbs_mom         15002/udp   # mom to/from server
pbs_resmon      15003/tcp   # mom resource management requests
pbs_resmon      15003/udp   # mom resource management requests
pbs_sched       15004/tcp   # scheduler 
pbs_sched       15004/udp   # scheduler
trqauthd        15005/tcp   #authd
trqauthd        15005/udp   #authd
EOF
fi
#end update


%post -n %{momname}
%_post_service pbs_mom

%preun -n %{momname}
%_preun_service pbs_mom

%post -n %{servername}
%_post_service pbs_server

%preun -n %{servername}
%_preun_service pbs_server

%post -n %{schedname}
%_post_service pbs_sched

%preun -n %{schedname}
%_preun_service pbs_sched

%post -n %{clientname}
%_post_service trqauthd

%preun -n %{clientname}
%_preun_service trqauthd



%files
%doc PBS_License_2.5.txt Release_Notes README.torque
%doc README.array_changes
%dir %{torquedir}
%dir %{torquedir}/checkpoint
%dir %{torquedir}/aux
%dir %{torquedir}/spool
%dir %{torquedir}/undelivered
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/server_name
%{torquedir}/server_name
%{torquedir}/pbs_environment
%{_libdir}/security/pam*
%{_mandir}/man1/pbs.1.*



%files -n %{libname}
%doc CHANGELOG
%{_libdir}/*.so.*


%files -n %{devname}
%doc 
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_bindir}/pbs-config
%{_libdir}/*.so
%{_defaultdocdir}/torque-drmaa
%{_mandir}/man3/*.h.3*
%{_mandir}/man3/pbs_*.3*
%{_mandir}/man3/rpp.3*
%{_mandir}/man3/tm.3*
%{_mandir}/man3/drmaa.3*
%{_mandir}/man3/drmaa_*.3*


%files -n %{clientname}
%doc
%{_bindir}/qa*
%{_bindir}/qc*
%{_bindir}/qdel
%{_bindir}/qg*
%{_bindir}/qh*
%{_bindir}/qm*
%{_bindir}/qo*
%{_bindir}/qrerun
%{_bindir}/qrls
%{_bindir}/qsub
%{_bindir}/qstat
%{_bindir}/qsig
%{_bindir}/qselect
%{_bindir}/chk_tree
%{_bindir}/hostn
%{_bindir}/nqs2pbs
%{_bindir}/pbsnodes
%{_bindir}/qnodes
%{_bindir}/pbsdsh
%{_bindir}/qterm
%{_bindir}/qstop
%{_bindir}/qstart
%{_bindir}/qdisable
%{_bindir}/qenable
%{_bindir}/qrun
%{_mandir}/man1/q*.1*
%{_mandir}/man1/nqs2pbs.1*
%{_mandir}/man1/pbsdsh.1*
%{_mandir}/man3/jobs.3*
%{_mandir}/man7/pbs_*.7*
%{_mandir}/man8/pbsnodes.8*
%{_mandir}/man8/q*.8*
%{_sbindir}/pbs_iff


%files -n %{servername}
%dir %{torquedir}/server_priv
%dir %{torquedir}/server_priv/acl_svr
%dir %{torquedir}/server_priv/acl_groups
%dir %{torquedir}/server_priv/acl_hosts
%dir %{torquedir}/server_priv/acl_users
%dir %{torquedir}/server_priv/accounting
%dir %{torquedir}/server_priv/arrays
%dir %{torquedir}/server_priv/credentials
%dir %{torquedir}/server_priv/disallowed_types
%dir %{torquedir}/server_priv/hostlist
%dir %{torquedir}/server_priv/jobs
%dir %{torquedir}/server_priv/queues
%config(noreplace) %{_sysconfdir}/%{name}/nodes
%{torquedir}/server_priv/nodes
%{_initrddir}/pbs_server
%{_sbindir}/pbs_server
%{_sbindir}/qserverd
%{_bindir}/pbs_track
%{_bindir}/tracejob
%{_bindir}/printjob
%{_bindir}/printserverdb
%{_bindir}/printtracking
%{_mandir}/man8/pbs_server.8*


%files -n %{schedname}
%dir %{torquedir}/sched_priv
%dir %{torquedir}/sched_priv/accounting
%dir %{torquedir}/sched_logs
%config(noreplace) %{_sysconfdir}/%{name}/sched_config 
%config(noreplace) %{_sysconfdir}/%{name}/dedicated_time 
%config(noreplace) %{_sysconfdir}/%{name}/holidays 
%config(noreplace) %{_sysconfdir}/%{name}/resource_group
%{torquedir}/sched_priv/sched_config
%{torquedir}/sched_priv/dedicated_time
%{torquedir}/sched_priv/holidays
%{torquedir}/sched_priv/resource_group
%{_initrddir}/pbs_sched
%{_sbindir}/pbs_sched
%{_sbindir}/qschedd
%{_mandir}/man8/pbs_sched*.8*


%files -n %{momname}
%doc
%dir %{torquedir}/mom_priv
%dir %{torquedir}/mom_priv/jobs
%dir %{torquedir}/mom_logs
%config(noreplace) %{_sysconfdir}/%{name}/mom_config
%{torquedir}/mom_priv/config
%{_initrddir}/pbs_mom
%{_sbindir}/pbs_mom
%{_sbindir}/qnoded
%{_sbindir}/momctl
%{_sbindir}/pbs_demux
#attr(4755, root, root) {_sbindir}/pbs_iff
%{_mandir}/man8/pbs_mom.8*


%files -n %{guiname}
%{_bindir}/xpbs*
%{_bindir}/pbs_wish
%{_bindir}/pbs_tclsh
%{tcl_sitelib}/xpbs
%{tcl_sitelib}/xpbsmon
%{_libdir}/xpbs
%{_libdir}/xpbsmon
%{_mandir}/man1/xpbs*.1*

%changelog -f %{_sourcedir}/%{name}-changelog.gitrpm.txt