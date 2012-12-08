%define name netcdf-devel%{?fortran:-%{fortran}}
%define version 3.6.3
%define realversion %{version}
%define release %mkrel 5

%define fortrancomp gfortran
%define isstdfortran %{?fortran:1}%{?!fortran:0}
%define foptflags %optflags

%if %{?_with_pgf:1}%{?!_with_pgf:0}
%define fortrancomp pgf90
%define fortran pgf
%define foptflags
%endif

%if %{?_with_g95:1}%{?!_with_g95:0}
%define fortrancomp g95
%define fortran g95
%endif

%if %{?_with_nag:1}%{?!_with_nag:0}
%define fortrancomp f95
%define fortran nag
%endif

Name: %{name}
Version: %{version}
Release: %{release}
Summary: Libraries to use the Unidata network Common Data Form (netCDF)
License: distributable (see COPYRIGHT)
Source0: ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-%{realversion}.tar.gz
Source1: ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.pdf.bz2
Source2: ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.html.tar.bz2
Patch0:  netcdf-3.6.3-wformat.patch
URL: http://www.unidata.ucar.edu/packages/netcdf/index.html
Group: Development/C
BuildRequires: gcc-gfortran
%if %{?fortran:1}%{?!fortran:0}
Requires: netcdf-devel >= %{version}
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
NetCDF (network Common Data Form) is an interface for array-oriented data
access and a freely-distributed collection of software libraries for C, 
Fortran, C++, and perl that provides an implementation of the interface.
The netCDF library also defines a machine-independent format for representing
scientific data. Together, the interface, library, and format support the 
creation, access, and sharing of scientific data. The netCDF software was 
developed at the Unidata Program Center in Boulder, Colorado.

NetCDF data is: 

   o Self-Describing. A netCDF file includes information about the data it
     contains. 

   o Network-transparent. A netCDF file is represented in a form that can be 
     accessed by computers with different ways of storing integers, characters,
     and floating-point numbers. 

   o Direct-access. A small subset of a large dataset may be accessed 
     efficiently, without first reading through all the preceding data. 

   o Appendable. Data can be appended to a netCDF dataset along one dimension 
     without copying the dataset or redefining its structure. The structure of 
     a netCDF dataset can be changed, though this sometimes causes the dataset 
     to be copied. 

   o Sharable. One writer and multiple readers may simultaneously access the 
     same netCDF file. 

This package can be build with another fortran compiler than gfortran.
You can use rpm --rebuild with one of:
  --with pgf
  --with g95
  --with nag (warning: gfortran is also installed as f95 so it's conflict
	      with nag fortran )

%if %{isstdfortran}
This netcdf has been built with %{fortran}
%endif


%prep
%setup -q -n netcdf-%{realversion}
perl -pi -e "/^LIBDIR/ and s/\/lib/\/%_lib/g" src/macros.make.*
%patch0 -p0 -b .wformat

%build
export F77=%{fortrancomp}
export FC=%{fortrancomp}
export F90=%{fortrancomp}
export FFLAGS=-fPIC
export FCFLAGS=-fPIC
export F90FLAGS=-fPIC
export CFLAGS="%optflags -DpgiFortran -fPIC"
export CPPFLAGS="%optflags -DpgiFortran -fPIC"
export CXXFLAGS="%optflags -DpgiFortran -fPIC"
%if %{?_with_g95:1}%{?!_with_g95:0}
export CPPFLAGS="-DNDEBUG -Df2cFortran"
export CFLAGS="$RPM_OPT_FLAGS -fno-fast-math -Df2cFortran -fPIC"
export CXXFLAGS="$RPM_OPT_FLAGS -fno-fast-math -Df2cFortran -fPIC"
%endif
%if %{?_with_nag:1}%{?!_with_nag:0}
export CPPFLAGS="-DNDEBUG -DNAGf90Fortran"
export CFLAGS="$RPM_OPT_FLAGS -fno-fast-math -DNAGf90Fortran -fPIC"
export CXXFLAGS="$RPM_OPT_FLAGS -fno-fast-math -DNAGf90Fortran -fPIC"
%endif

%configure2_5x
make

%check
%if %{?_with_nag:0}%{?!_with_nag:1}
make test
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_prefix} $RPM_BUILD_ROOT%{_mandir}
%makeinstall

#mv $RPM_BUILD_ROOT%{_prefix}/man/* $RPM_BUILD_ROOT%{_mandir}

%if %{?fortran:1}%{?!fortran:0}
mv %{buildroot}%{_libdir}/libnetcdf.a %{buildroot}%{_libdir}/libnetcdf-%{fortran}.a
(cd %{buildroot}%{_includedir}
 mkdir  %{fortran}
 mv netcdf.mod %{fortran}/netcdf.mod
 mv typesizes.mod %{fortran}/typesizes.mod
 rm %{buildroot}/%{_bindir}/*
 rm %{buildroot}/%{_libdir}/libnetcdf_c++.a
 rm -rf %{buildroot}/%{_mandir}
 rm %{buildroot}%{_includedir}/*
)
%endif

bzcat %{SOURCE1} > guidec.pdf
bzcat %{SOURCE2} | tar xvf -

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*.a
%{_infodir}/netcdf-c.info.*
%{_infodir}/netcdf-cxx.info.*
%{_infodir}/netcdf-install.info.*
%{_infodir}/netcdf-tutorial.info.*
%{_infodir}/netcdf.info.*
%if %{?fortran:0}%{?!fortran:1}
%doc README RELEASE_NOTES guidec.pdf guidec
%{_bindir}/ncgen
%{_bindir}/ncdump
%{_infodir}/netcdf-f77.info.*
%{_infodir}/netcdf-f90.info.*
%{_mandir}/man1/ncgen.1*
%{_mandir}/man1/ncdump.1*
%{_mandir}/man3/netcdf.3*
%{_mandir}/man3/netcdf_f77.3.*
%{_mandir}/man3/netcdf_f90.3.*
%endif
%if %{isstdfortran}
%dir %{_includedir}/%{fortran}
%{_includedir}/%{fortran}/*
%else
%{_includedir}/*
%endif


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 3.6.3-3mdv2011.0
+ Revision: 666611
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 3.6.3-2mdv2011.0
+ Revision: 606820
- rebuild

* Tue Mar 30 2010 Funda Wang <fwang@mandriva.org> 3.6.3-1mdv2010.1
+ Revision: 529726
- new version 3.6.3

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 3.6.1-6mdv2010.1
+ Revision: 521152
- rebuilt for 2010.1

* Tue Sep 01 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.6.1-5mdv2010.0
+ Revision: 423654
- rebuild
- fix -Wformat warnings
- fix gcc 4.4 compilation

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 3.6.1-3mdv2008.1
+ Revision: 130573
- kill re-definition of %%buildroot on Pixel's request


* Mon Mar 19 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 3.6.1-3mdv2007.1
+ Revision: 146599
- Fixed Group (bug #28161).

* Sun Feb 18 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 3.6.1-2mdv2007.1
+ Revision: 122417
- rebuild.
- Import netcdf-devel

* Fri May 05 2006 Giuseppe Ghibò <ghibo@mandriva.com> 3.6.1-1mdk
- Release 3.6.1.

* Tue Dec 20 2005 Olivier Thauvin <nanardon@mandriva.org> 3.6.1-0.beta3.3mdk
- From Philippe Weill <Philippe.Weill@aero.jussieu.fr>
  - change false comments to change Fortran compiler
  - removing somes files when compiled with other than standard fortran
    to install more than one version without conflict
  - added dependancy to standard version when compiled with other fortran
  -removing test for nag fortran ( one test as syntax problem )

* Fri Oct 07 2005 Olivier Thauvin <nanardon@mandriva.org> 3.6.1-0.beta3.2mdk
* Thu Oct 06 2005 Olivier Thauvin <nanardon@mandriva.org> 3.6.1-0.beta3.1mdk
- From Philippe Weill <Philippe.Weill@aero.jussieu.fr>
  - allow build with pgf90, g95, fortran nag
  - 3.6.1beta3
  - -fPIC for x86_64
- re-add %%doc
- spec cleanup

* Mon May 23 2005 Laurent MONTEL <lmontel@mandriva.com> 3.6.1-0.beta3.1mdk
- 3.6.1-beta3

* Mon May 23 2005 Laurent MONTEL <lmontel@mandriva.com> 3.5.0-7mdk
- Fix

* Wed Mar 23 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 3.5.0-6mdk
- Rebuilt.

