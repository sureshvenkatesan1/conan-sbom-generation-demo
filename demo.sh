## CONFIGURATION

# the demo uses a fake openssl empty library with known issues and an empty somelibrary

# Follow the steps and substitute the <> placeholders with your own information

# <conan_remote_name> --> use the name of the remote in Conan (it may not be the same with the name in Artifactory, this is the name you get with 'conan remote list')
# <artifactory_repo_name> --> this is the name of the repository in Artifactory that is configured in Conan
# <artifactory_url> --> url for Artifactory, something like 'https://whatever/artifactory'
# <user> and <password> for the Artifactory repo

conan remove "somelibrary*" -r=<conan_remote_name> -c
conan remove "openssl/1.1.1c*" -r=<conan_remote_name> -c
conan remove "openssl*" -c
conan remove "somelibrary*" -c

# a fake openssl

conan create openssl --build="openssl*"

conan upload "openssl*" -r=<conan_remote_name> -c

conan create somelibrary --format=json --build="somelibrary*" -r=<conan_remote_name> > create_output.json

conan upload "somelibrary*" -r=<conan_remote_name> -c

conan art:build-info create create_output.json somelib_build 1 <artifactory_repo_name> --url=<artifactory_url> --user=<user> --password=<password> --with-dependencies > somelib_build.json

conan art:build-info upload somelib_build.json --url=<artifactory_url> --user=<user> --password=<password>
