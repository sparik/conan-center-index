
from conans import ConanFile, CMake, tools
import os


class LightPcapNgConan(ConanFile):
    name = "LightPcapNg"
    homepage = "https://github.com/woidpointer/LightPcapNg"
    description = "Library for general-purpose tracing based on PCAPNG file format"
    topics = ("conan", "pcapng", "pcap")
    url = "https://github.com/conan-io/conan-center-index"
    no_copy_source = True
    license = "MIT"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "with_zstd": [True, False],
    }
    default_options = {
        "shared": False,
        "with_zstd": True,
    }
    generators = "cmake", "cmake_paths", "cmake_find_package"
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def requirements(self):
        if self.options.with_zstd:
            self.requires("zstd/1.4.5")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["LIGHT_USE_ZSTD"] = self.options.with_zstd
        self._cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_subfolder)
        return self._cmake

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "light_pcapng"
        self.cpp_info.names["cmake_find_package_multi"] = "light_pcapng"
        if not self.settings.os == "Windows":
            self.cpp_info.libs = ["liblight_pcapng.a"] if not self.options.shared else ["liblight_pcapng.so"]
        else:
            self.cpp_info.libs = ["light_pcapng.lib"]



