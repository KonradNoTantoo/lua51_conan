from conans import ConanFile, CMake, tools
import os


class LuaConan(ConanFile):
    name = "lua"
    version = "5.1.5"
    folder_name = "{}-{}".format(name, version)
    license = "MIT"
    author = "konrad.no.tantoo"
    url = "https://github.com/KonradNoTantoo/lua51_conan"
    description = "Lua is a powerful, efficient, lightweight, embeddable scripting language."
    topics = ("language", "scripting", "embedded")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "build_interpreter": [True, False], "build_compiler": [True, False]}
    default_options = {"shared": True, "fPIC": True, "build_interpreter": False, "build_compiler": False}
    exports = "CMakeLists.txt"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"


    def copy_file_to_source(self, name):
        file_content = tools.load(name)
        path_to_source = os.path.join(self.source_folder, self.folder_name, name)
        tools.save(path_to_source, file_content)


    def requirements(self):
        if self.settings.os != "Windows" and self.options.build_interpreter:
            self.requires("readline/8.0", private=True)


    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        # fPIC isn't needed either when using VS or on x86 platforms with other compilers
        if self.settings.compiler == 'Visual Studio' or self.settings.arch == "x86":
            del self.options.fPIC


    def source(self):
        zip_name = "lua-%s.tar.gz" % self.version
        tarball_path = "https://www.lua.org/ftp/{}.tar.gz".format(self.folder_name)
        tools.get(tarball_path)
        self.copy_file_to_source("CMakeLists.txt")


    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_INTERPRETER"] = "ON" if self.options.build_interpreter else "OFF"
        cmake.definitions["BUILD_COMPILER"] = "ON" if self.options.build_compiler else "OFF"
        cmake.definitions["SHARED"] = "ON" if self.options.shared else "OFF"
        cmake.configure(source_folder=self.folder_name)
        cmake.build()


    def package(self):
        src_path = os.path.join(self.folder_name, "src")

        exported_headers = [
            "lua.h",
            "lualib.h",
            "lauxlib.h",
            "luaconf.h",
        ]

        for header in exported_headers:
            self.copy(header, dst="include", src=src_path, keep_path=False)
        self.copy("*/lua.exe", dst="bin", keep_path=False)
        self.copy("*/luac.exe", dst="bin", keep_path=False)
        self.copy("*/lua", dst="bin", keep_path=False)
        self.copy("*/luac", dst="bin", keep_path=False)
        self.copy("*/lua.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)


    def package_info(self):
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ["lua"]
        else:
            self.cpp_info.libs = ["lua" if self.options.shared else "liblua.a"]
            self.cpp_info.system_libs = ["dl", "m"]
