#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	Read, write, repair, and transform PDFs in Python, powered by qpdf
Summary(pl.UTF-8):	Odczyt, zapis, naprawa i przekształcanie PDF-ów w Pythonie przy wsparciu qpdf
Name:		python3-pikepdf
Version:	10.7.3
Release:	1
License:	MPL v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pikepdf/
Source0:	https://files.pythonhosted.org/packages/source/p/pikepdf/pikepdf-%{version}.tar.gz
# Source0-md5:	5928f028116e5f3af7f84044d3dec545
URL:		https://pypi.org/project/pikepdf/
BuildRequires:	cmake >= 3.15
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	ninja
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-installer
BuildRequires:	python3-nanobind >= 2.0
BuildRequires:	python3-scikit-build-core >= 0.10
BuildRequires:	qpdf-devel >= 12.2.0
%if %{with tests}
BuildRequires:	python3-attrs >= 20.2.0
BuildRequires:	python3-dateutil >= 2.8.1
BuildRequires:	python3-hypothesis >= 6.36
BuildRequires:	python3-lxml >= 4.8
BuildRequires:	python3-numpy >= 1.21.0
BuildRequires:	python3-packaging
BuildRequires:	python3-psutil >= 5.9
BuildRequires:	python3-pillow >= 10.0.1
BuildRequires:	python3-pytest >= 6.2.5
BuildRequires:	python3-pytest-cov >= 3.0.0
BuildRequires:	python3-pytest-timeout >= 2.1.0
BuildRequires:	python3-pytest-xdist >= 2.5.0
%if "%{py3_ver}" == "3.10"
BuildRequires:	python3-tomli
%endif
BuildRequires:	python3-xmp-toolkit >= 2.0.1
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-myst_parser >= 3.0.1
BuildRequires:	python3-sphinx_autoapi
BuildRequires:	python3-sphinx_design
BuildRequires:	python3-sphinx_issues
BuildRequires:	python3-sphinx_rtd_theme
%if "%{py3_ver}" == "3.10"
BuildRequires:	python3-tomli
%endif
BuildRequires:	sphinx-pdg-3 >= 3
%endif
Requires:	python3-modules >= 1:3.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Read, write, repair, and transform PDFs in Python.

pikepdf is based on qpdf (<https://github.com/qpdf/qpdf>), a mature,
actively maintained C++ library for PDF manipulation and repair.

%description -l pl.UTF-8
Odczyt, zapis, naprawa i przekształcanie PDF-ów w Pythonie.

pikepdf jest oparty na qpdf (<https://github.com/qpdf/qpdf>) -
dojrzałej, aktywnie rozwijanej bibliotece C++ do operacji i naprawy
plików PDF.

%package apidocs
Summary:	API documentation for Python pikepdf module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pikepdf
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python pikepdf module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pikepdf.

%prep
%setup -q -n pikepdf-%{version}

# force system qpdf
%{__rm} -r qpdf

%build
export CMAKE_BUILD_PARALLEL_LEVEL=%{__jobs}
export SKBUILD_BUILD_VERBOSE=true
export SKBUILD_CMAKE_BUILD_TYPE=PLD
export SKBUILD_INSTALL_STRIP=false
%py3_build_pyproject

%if %{with doc} || %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
%endif

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=xdist.plugin \
PYTHONPATH=$(pwd)/build-3-test \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-3-test \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{py3_sitedir}/pikepdf
%{py3_sitedir}/pikepdf/_core.cpython-*.so
%{py3_sitedir}/pikepdf/_core.pyi
%{py3_sitedir}/pikepdf/py.typed
%{py3_sitedir}/pikepdf/*.py
%{py3_sitedir}/pikepdf/__pycache__
%{py3_sitedir}/pikepdf/models
%{py3_sitedir}/pikepdf-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_sphinx_design_static,_static,api,references,releasenotes,topics,*.html,*.js}
%endif
