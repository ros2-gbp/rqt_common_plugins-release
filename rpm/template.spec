%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/iron/.*$
%global __requires_exclude_from ^/opt/ros/iron/.*$

Name:           ros-iron-rqt-common-plugins
Version:        1.2.0
Release:        3%{?dist}%{?release_suffix}
Summary:        ROS rqt_common_plugins package

License:        BSD
URL:            http://ros.org/wiki/rqt_common_plugins
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-iron-rqt-action
Requires:       ros-iron-rqt-bag
Requires:       ros-iron-rqt-bag-plugins
Requires:       ros-iron-rqt-console
Requires:       ros-iron-rqt-graph
Requires:       ros-iron-rqt-image-view
Requires:       ros-iron-rqt-msg
Requires:       ros-iron-rqt-publisher
Requires:       ros-iron-rqt-py-common
Requires:       ros-iron-rqt-py-console
Requires:       ros-iron-rqt-reconfigure
Requires:       ros-iron-rqt-service-caller
Requires:       ros-iron-rqt-shell
Requires:       ros-iron-rqt-srv
Requires:       ros-iron-rqt-topic
Requires:       ros-iron-ros-workspace
BuildRequires:  ros-iron-ament-cmake
BuildRequires:  ros-iron-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
rqt_common_plugins metapackage provides ROS backend graphical tools suite that
can be used on/off of robot runtime. To run any rqt plugins, just type in a
single command &quot;rqt&quot;, then select any plugins you want from the GUI
that launches afterwards. rqt consists of three following metapackages: rqt -
core modules of rqt (ROS GUI) framework. rqt plugin developers barely needs to
pay attention to this metapackage. rqt_common_plugins (you're here!)
rqt_robot_plugins - rqt plugins that are particularly used with robots during
their runtime.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/iron" \
    -DAMENT_PREFIX_PATH="/opt/ros/iron" \
    -DCMAKE_PREFIX_PATH="/opt/ros/iron" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/iron

%changelog
* Thu Apr 20 2023 Ivan Paunovic <ivanpauno@ekumenlabs.com> - 1.2.0-3
- Autogenerated by Bloom

* Tue Mar 21 2023 Ivan Paunovic <ivanpauno@ekumenlabs.com> - 1.2.0-2
- Autogenerated by Bloom

