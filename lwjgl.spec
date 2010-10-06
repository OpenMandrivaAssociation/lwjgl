Summary:	The Lightweight Java Game Library
Name:		lwjgl
Version:	2.5
Release:	%mkrel 1
Source0:	http://downloads.sourceforge.net/project/java-game-lib/Official%20Releases/LWJGL%20%{version}/%{name}-source-%{version}.zip
Source1:	http://developer.apple.com/mac/library/samplecode/AppleJavaExtensions/AppleJavaExtensions.zip
License:	BSD
Group:		Development/Java
Url:		http://lwjgl.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	ant
BuildRequires:	ant-nodeps
BuildRequires:	ant-pack200
BuildRequires:	java-rpmbuild
BuildRequires:	jinput
BuildRequires:	unzip
BuildRequires:	libxxf86vm-static-devel
BuildRequires:	libxrandr2-devel
BuildRequires:	libxcursor-devel
BuildRequires:	x11-proto-devel
BuildRequires:	libx11_6-devel

Requires:	java >= 1.5

%description
The Lightweight Java Game Library (LWJGL) is a solution aimed directly at 
professional and amateur Java programmers alike to enable commercial quality 
games to be written in Java. LWJGL provides developers access to high 
performance cross-platform libraries such as OpenGL and OpenAL allowing for 
state of the art 3D games and sound.
Additionally LWJGL provides access to controllers such as Gamepads, Steering 
wheel and Joysticks. All in a simple and straight forward API.

%package	javadoc
Summary:	Javadoc for lwjgl
Group:		Development/Java

%description	javadoc
Javadoc for lwjgl.

%prep
%setup -q -c -T -b1 -a0
%remove_java_binaries
%__mkdir libs bin
pushd libs
ln -s %_javadir/jinput.jar .
# Deps needed for build only, macOS compat.
mv ../../AppleJavaExtensions/AppleJavaExtensions.jar .
popd
pushd platform_build
ln -s %_javadir/jlzma JLzma.jar
ln -s %_javadir/ant/Pack200Task.jar .
popd
# adjust linking option for Xxf86vm
%__sed -i -e 's|-Wl,-static,-lXxf86vm,-call_shared|-lXxf86vm|g' platform_build/linux_ant/build.xml
# fix jar build
%__sed -i -e 's|<jar|<jar index="true" compress="true"|g' build.xml

%build
export CLASSPATH="."
%ant all javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -m644 libs/%{name}.jar -D $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m44 libs/%{name}_util.jar -D $RPM_BUILD_ROOT%{_javadir}/%{name}-util-%{version}.jar
install -m644 libs/%{name}_util_applet.jar -D $RPM_BUILD_ROOT%{_javadir}/%{name}-util-applet-%{version}.jar
%create_jar_links
install -m644 libs/linux/lib%{name}.so -D $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_javadir}/*.jar
%{_libdir}/*.so

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/*
