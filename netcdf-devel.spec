%define name netcdf-devel%{?fortran:-%{fortran}}
%define version 3.6.1
%define realversion %{version}
%define release %mkrel 3

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
Source0: ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-%{realversion}.tar.bz2
Source1: ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.pdf.bz2
Source2: ftp://ftp.unidata.ucar.edu/pub/netcdf/guidec.html.tar.bz2
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

%build
cd src

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
cd src
%if %{?_with_nag:0}%{?!_with_nag:1}
make test
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_prefix} $RPM_BUILD_ROOT%{_mandir}
(cd src
%makeinstall

mv $RPM_BUILD_ROOT%{_prefix}/man/* $RPM_BUILD_ROOT%{_mandir}

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

)
bzcat %{SOURCE1} > guidec.pdf
bzcat %{SOURCE2} | tar xvf -

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*.a
%if %{?fortran:0}%{?!fortran:1}
%doc src/COPYRIGHT src/README src/RELEASE_NOTES guidec.pdf guidec
%{_bindir}/ncgen
%{_bindir}/ncdump
%{_mandir}/man1/ncgen.1*
%{_mandir}/man1/ncdump.1*
%{_mandir}/man3/netcdf.3*
%endif
%if %{isstdfortran}
%dir %{_includedir}/%{fortran}
%{_includedir}/%{fortran}/*
%else
%{_includedir}/*
%endif


