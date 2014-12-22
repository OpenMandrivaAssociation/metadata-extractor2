%{?_javapackages_macros:%_javapackages_macros}
%global majorversion 2
Name:          metadata-extractor2
Version:       2.6.4
Release:       4.1
Summary:       Extracts EXIF, IPTC and XMP metadata from image files
Group:         Development/Java
License:       ASL 2.0
URL:           http://drewnoakes.com/code/exif/
Source0:       http://metadata-extractor.googlecode.com/files/metadata-extractor-%{version}-src.jar
# originally taken from http://code.google.com/p/metadata-extractor/source/browse/pom.xml
# fix javadoc task, jar maifest entries
Source1:       metadata-extractor-%{version}.pom

BuildRequires: java-devel
BuildRequires: mvn(com.adobe.xmp:xmpcore)
BuildRequires: mvn(xerces:xercesImpl)
# Test deps
BuildRequires: mvn(junit:junit)
BuildRequires: maven-local
Provides:      mvn(com.drewnoakes:metadata-extractor) = %{version}-%{release}
BuildArch:     noarch

%description
Metadata Extractor is a straightforward Java library
for reading metadata from image files.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -c %{name}-%{version}
rm -r META-INF
find -name '*.jar' -delete
find -name '*.class' -delete

cp -p %{SOURCE1} pom.xml

# Fix non ASCII chars
for s in Source/com/drew/lang/GeoLocation.java \
 Source/com/drew/metadata/icc/IccDescriptor.java;do
  native2ascii -encoding UTF8 ${s} ${s}
done

# This test fail for unavailable resource
# java.io.FileNotFoundException: Tests/com/drew/metadata/icc/iccDataInvalid1.app2bytes (No such file or directory)
rm -r Tests/com/drew/metadata/icc/IccReaderTest.java

sed -i 's/\r//' LICENSE-2.0.txt README.txt

# NoClassDefFound org/w3c/dom/ElementTraversal
%pom_add_dep xml-apis:xml-apis::test

%build

%mvn_file :metadata-extractor %{name}
%mvn_alias :metadata-extractor "drew:metadata-extractor"
%mvn_compat_version ":metadata-extractor" %{majorversion}
%mvn_build

%install
%mvn_install

%jpackage_script com.drew.imaging.ImageMetadataReader "" "" %{name}-%{majorversion}:xmpcore %{name} true

%files -f .mfiles
%{_bindir}/*
%doc LICENSE-2.0.txt README.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE-2.0.txt

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 02 2014 gil cattaneo <puntogil@libero.it> 2.6.4-3
- fix rhbz#1068933

* Mon Oct 21 2013 gil cattaneo <puntogil@libero.it> 2.6.4-2
- fix script

* Mon Jan 21 2013 gil cattaneo <puntogil@libero.it> 2.6.4-1
- initial rpm
