from conans import ConanFile, CMake, tools
import os


class OpenscenegraphConan(ConanFile):
    name = "openscenegraph"
    version = "3.6.3"
    description = "OpenSceneGraph is an open source high performance 3D graphics toolkit"
    topics = ("conan", "openscenegraph", "graphics")
    url = "https://github.com/bincrafters/conan-openscenegraph"
    homepage = "https://github.com/openscenegraph/OpenSceneGraph"
    license = "MIT"
    exports_sources = ["CMakeLists.txt"]
    short_paths = True
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_osg_applications": [True, False],
        "build_osg_plugins_by_default": [True, False],
        "build_osg_examples": [True, False],
        "dynamic_openthreads": [True, False],
        "with_curl_plugin": [True, False],
        "with_resthttpdevice_plugin": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "build_osg_applications": False,
        "build_osg_plugins_by_default": False,
        "build_osg_examples": False,
        "dynamic_openthreads": True,
        "with_curl_plugin": False,
        "with_resthttpdevice_plugin": False,
    }
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def requirements(self):
        self.requires("zlib/1.2.11"),
        self.requires("freetype/2.10.1"),
        self.requires("libxml2/2.9.10"),
        self.requires("cairo/1.17.2"),
        # OSG uses ImageIO on MacOs, which will conflict with libjpeg apparently
        if self.settings.os != 'Macos':
            self.requires("libjpeg/9d"),
            self.requires("libpng/1.6.37"),
            self.requires("libtiff/4.1.0"),
            self.requires("jasper/2.0.14"),

    def build_requirements(self):
        if self.settings.os != 'Windows':
            self.build_requires("ninja/1.10.0")

    def system_requirements(self):
        if tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                if self.settings.arch == "x86" and tools.detected_architecture() == "x86_64":
                    installer.install("gcc-multilib")
                    installer.install("libx11-dev:i386")
                    installer.install("libgl1-mesa-dev:i386")
                    installer.install("libglu1-mesa-dev:i386")
                    installer.install("libegl1-mesa-dev:i386")
                    installer.install("libgtk2.0-dev:i386")
                    installer.install("libpoppler-glib-dev:i386")
                else:
                    installer.install("libx11-dev")
                    installer.install("libgl1-mesa-dev")
                    installer.install("libglu1-mesa-dev")
                    installer.install("libegl1-mesa-dev")
                    installer.install("libgtk2.0-dev")
                    installer.install("libpoppler-glib-dev")
            elif tools.os_info.with_yum:
                installer = tools.SystemPackageTool()
                if self.settings.arch == "x86" and tools.detected_architecture() == "x86_64":
                    installer.install("glibmm24.i686")
                    installer.install("glibc-devel.i686")
                    installer.install("libGLU-devel.i686")
                else:
                    installer.install("libGLU-devel")
            else:
                self.output.warn("Could not determine Linux package manager, skipping system requirements installation.")

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        prefix='OpenSceneGraph'
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "{}-{}-".format(prefix, prefix) + self.version
        os.rename(extracted_dir, self._source_subfolder)
        tools.replace_in_file(os.path.join(self._source_subfolder, 'src', 'osgPlugins', 'freetype', 'CMakeLists.txt'),
        "SET(TARGET_EXTERNAL_LIBRARIES ${FREETYPE_LIBRARIES} )",
        "SET(TARGET_EXTERNAL_LIBRARIES ${CONAN_LIBS_FREETYPE} ${CONAN_LIBS_LIBPNG} ${CONAN_LIBS_ZLIB} ${CONAN_LIBS_BZIP2} )"
        )

    def _configure_cmake(self):
        cmake = CMake(self, set_cmake_flags=True)
        cmake.definitions["BUILD_OSG_APPLICATIONS"] = self.options.build_osg_applications
        cmake.definitions["DYNAMIC_OPENSCENEGRAPH"] = self.options.shared
        cmake.definitions["BUILD_OSG_PLUGINS_BY_DEFAULT"] = self.options.build_osg_plugins_by_default
        cmake.definitions['BUILD_OSG_EXAMPLES'] = self.options.build_osg_examples
        cmake.definitions["DYNAMIC_OPENTHREADS"] = self.options.dynamic_openthreads
        cmake.definitions["BUILD_OSG_PLUGIN_CURL"] = self.options.with_curl_plugin
        cmake.definitions["BUILD_OSG_PLUGIN_RESTHTTPDEVICE"] = self.options.with_resthttpdevice_plugin
        cmake.definitions["BUILD_OSG_PLUGIN_FREETYPE"] = True

        if self.settings.os == 'Macos':
            cmake.definitions["OSG_DEFAULT_IMAGE_PLUGIN_FOR_OSX"] = 'imageio'
            cmake.definitions["BUILD_OSG_PLUGIN_IMAGEIO"] = True
            cmake.definitions["BUILD_OSG_PLUGIN_JPEG"] = False
            cmake.definitions["BUILD_OSG_PLUGIN_PNG"] = False
            cmake.definitions["BUILD_OSG_PLUGIN_TIFF"] = False
            cmake.definitions["BUILD_OSG_PLUGIN_JP2"] = False

        if self.settings.compiler == "Visual Studio":
            cmake.definitions['BUILD_WITH_STATIC_CRT'] = "MT" in str(self.settings.compiler.runtime)

        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*", dst="freetype-plugin-source", src=os.path.join(self._source_subfolder, 'src', 'osgPlugins', 'freetype'))
        cmake = self._configure_cmake()
        cmake.install()
        if os.path.exists(os.path.join(self.package_folder, 'lib64')):
            # rhel installs libraries into lib64
            os.rename(os.path.join(self.package_folder, 'lib64'),
                      os.path.join(self.package_folder, 'lib'))


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("rt")
        if not self.options.shared:
            self.cpp_info.defines.append("OSG_LIBRARY_STATIC=1")
        freetype_plugin_path = os.path.join(self.package_folder, 'freetype-plugin-source')
        self.user_info.openscenegraph_freetype_plugin_source = freetype_plugin_path.replace('\\', '/')
