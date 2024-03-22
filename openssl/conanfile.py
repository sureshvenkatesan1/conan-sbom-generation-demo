from conan import ConanFile


class opensslRecipe(ConanFile):
    name = "openssl"
    version = "1.1.1c"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
