from conan import ConanFile


class somelibraryRecipe(ConanFile):
    name = "somelibrary"
    version = "1.0"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    def requirements(self):
        self.requires("openssl/1.1.1c")
