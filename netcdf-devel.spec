#This package should be upgraded for Lx5

%define name netcdf-devel%{?fortran:-%{fortran}}

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

%define _disable_lto 1
%define _disable_rebuild_configure 1

Summary:	Libraries to use the Unidata network Common Data Form (netCDF)
Name:		%{name}
Version:	3.6.3
Release:	1
Group:		Development/C
License:	distributable (see COPYRIGHT)
Url:		https://www.unidata.ucar.edu/packages/netcdf/index.html
Source0:	ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-%{version}.tar.gz
Source1:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.pdf.bz2
Source2:	ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.html.tar.bz2
Patch0:		netcdf-3.6.3-wformat.patch
BuildRequires:	gcc-gfortran
%if %{?fortran:1}%{?!fortran:0}
Requires:	netcdf-devel >= %{version}
%endif

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
  --with nag (warning:	gfortran is also installed as f95 so it's conflict
	      with nag fortran )

%if %{isstdfortran}
This netcdf has been built with %{fortran}
%endif


%prep
%setup -q -n netcdf-%{version}
perl -pi -e "/^LIBDIR/ and s/\/lib/\/%_lib/g" src/macros.make.*
%patch0 -p0 -b .wformat

%build
export F77=%{fortrancomp}
export FC=%{fortrancomp}
export F90=%{fortrancomp}
export FFLAGS="-fPIC -fallow-argument-mismatch"
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
mkdir -p %{buildroot}/%{_prefix} %{buildroot}%{_mandir}
%makeinstall

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

%files
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
