import os
import platform
import re
from conan import ConanFile
from conan.tools.files import save, load
from conan.tools.gnu import AutotoolsToolchain, AutotoolsDeps
from conan.tools.microsoft import unix_path, VCVars, is_msvc
from conan.errors import ConanInvalidConfiguration
from conan.errors import ConanException
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps

class FalconConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    name = 'foo'
    version = '1.0'
    default_options = {
        "boost/*:shared": False,
        "librdkafka/*:ssl": True,
        "poco/*:enable_data_odbc": True,
        "tbb/*:tbbmalloc": True
    }
    def generate(self):
        tc = CMakeToolchain(self)
        tc.user_presets_path = 'ConanPresets.json'
        tc.generate()
        

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder, os.pardir))
        cmake.build()
        
    #below requirements are for both linux and windows
    requires = (
        "boost/1.75.0",             # TODO: run posttrade generators when we upgrade to boost/1.75.0+
                                    #   See https://github.com/boostorg/property_tree/issues/51
                                    #   and https://gitlab.tradeweb.com/idb/falcon/falcon/-/merge_requests/447
        "bzip2/1.0.8",
        "fmt/7.1.3",
        "jsoncpp/1.9.2",
        "ms-gsl/3.0.1",
        "libsodium/1.0.18",
        "libzip/1.7.3",       
        "quickfix/1.15.1",
        "spdlog/1.8.5",
        "zlib/1.2.11"
    )

    @staticmethod
    def _llmPlatform():
        if platform.system() == "Linux":
            if os.path.exists("/etc/system-release"):
                with open("/etc/system-release", "r") as file:
                    release = file.readline()
                    major = re.search(r"release (\d+)\.\d+", release).group(1)
                    if major == "6":
                        return "rhel6"
                    else:
                        return "rhel7"
            elif os.path.exists("/etc/debian_version"):
                return "debian"
            else:
                raise ConanException(f'Unsupported Linux Distribution')
        elif platform.system() == "Windows":
            return "windows"
        else:
            raise ConanException(f'Unsupported platform: {platform.system()}')

    def init(self):
        self.generators = "cmake" if platform.system() == "Linux" else ("cmake", "cmake_find_package_multi")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options["llm"].cxx = False
            self.options["llm"].python2 = False
            self.options["llm"].python3 = False
            self.options["llm"].shared = True
            self.options["odbc"].shared = True
        else:
            self.options["llm"].shared = False
            self.options["llm"].lz4 = False
            self.options["tbb"].shared = False

    def imports(self):
        if self.settings.os == "Windows":
            self.copy("*.dll", dst="bin", src="bin")

    def requirements(self):
        if self.settings.os == "Linux":
            if Version(self.settings.compiler.version.value) >= 8:
                self.requires("libpqxx/7.2.1")
            self.requires("bison/3.5.3")
            self.requires("catch2/2.13.1")
            self.requires("cppzmq/4.6.0")
            self.requires("cryptopp/8.2.0")
            self.requires("date/2.4.1")
            self.requires("flex/2.6.4")
            self.requires("librdkafka/1.4.0")
            self.requires("libiconv/1.16")
            self.requires("libxml2/2.9.8@idbdevbuild/stable")               # TODO: switch to Conan Center version
            self.requires("mq/7.5@idbdevbuild/stable")                      # Use FIXED_PKG::mq, not CONAN_PKG::mq
            self.requires("odbc/2.3.9")                 
            self.requires("onetick/20201128120000@idbdevbuild/stable")
            self.requires("poco/1.10.1")
            self.requires("quickfix-falcon/1.13.3.27@idbdevbuild/stable")
            self.requires("range-v3/0.3.0@ericniebler/stable")
            self.requires("swapi/18.1.428847@idbdevbuild/stable")           # Use FIXED_PKG::swapi, not CONAN_PKG::swapi
            self.requires("tz/2016j@idbdevbuild/stable")
            self.requires("zstd/1.4.9")
           
        else:
            self.requires("winflexbison/2.5.22")

