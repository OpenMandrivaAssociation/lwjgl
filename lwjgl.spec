Summary:	The Lightweight Java Game Library
Name:		lwjgl
Version:	2.7.1
Release:	2
Source0:	http://downloads.sourceforge.net/project/java-game-lib/Official%20Releases/LWJGL%20%{version}/%{name}-source-%{version}.zip
Source1:	http://developer.apple.com/mac/library/samplecode/AppleJavaExtensions/AppleJavaExtensions.zip
Patch0:		lwjgl-source-2.5-link.patch
License:	BSD
Group:		Development/Java
Url:		http://lwjgl.org
BuildRequires:	ant
BuildRequires:	ant-nodeps
BuildRequires:	ant-pack200
BuildRequires:	java-rpmbuild
BuildRequires:	jinput
BuildRequires:	unzip
BuildRequires:	jlzma
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(x11)
Buildrequires:	libxt-devel

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
%setup -c
%remove_java_binaries
%__mkdir libs bin
pushd libs
ln -s %_javadir/jinput.jar .
# Deps needed for build only, macOS compat.
unzip -j %{SOURCE1} AppleJavaExtensions/AppleJavaExtensions.jar
popd
pushd platform_build
ln -s %_javadir/jlzma JLzma.jar
ln -s %_javadir/ant/Pack200Task.jar .
popd
%patch0 -p0
%__sed -i -e 's|<jar|<jar index="true" compress="true"|g' build.xml

%build
export CLASSPATH="."
%ant all javadoc

%install
install -m644 libs/%{name}.jar -D $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m644 libs/%{name}_util.jar -D $RPM_BUILD_ROOT%{_javadir}/%{name}-util-%{version}.jar
install -m644 libs/%{name}_util_applet.jar -D $RPM_BUILD_ROOT%{_javadir}/%{name}-util-applet-%{version}.jar
%create_jar_links
install -m644 libs/linux/lib%{name}*.so -D $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%{_javadir}/*.jar
%{_libdir}/*.so

%files javadoc
%{_javadocdir}/*


%changelog
* Tue Jun 07 2011 Zombie Ryushu <ryushu@mandriva.org> 2.7.1-1mdv2011.0
+ Revision: 683006
- Upgrade to 2.7.1

* Sat Feb 05 2011 Funda Wang <fwang@mandriva.org> 2.5-2
+ Revision: 636071
- tighten BR

* Wed Oct 13 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.5-1mdv2011.0
+ Revision: 585261
- fix install on 64 bit
- fix buildrequires
- apply some cosmetics

  + Jonathan Bayle <mrhide@mandriva.org>
    - fix %%setup
    - import lwjgl

