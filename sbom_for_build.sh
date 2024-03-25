#!/bin/bash
usage() {
    echo "Unknown options: $1
    Valid Script option are:
    --buildname - [Mandatory] Build Name
    --buildnumber - [Mandatory] Build Number
    --projectkey - [optinal] the project key
    ex1: bash <script> --buildname npm-build --buildnumber 37
    ex1: bash <script> --buildname npm-build-proj --buildnumber 40 --projectkey nagag"
}
while [[ $# -gt 0 ]]; do
    case "$1" in
        --buildname)
            buildname="$2"
            shift 2
            ;;
        --buildnumber)
            buildnumber="$2"
            shift 2
            ;;
        --projectkey)
            projectkey="$2"
            shift 2
            ;;
        *)
            usage $1
            exit 1
            ;;
    esac
done

if [ -z "${buildname}" ]; then
    echo "--buildname is unset or set to the empty string"
    usage
    exit 1
fi
if [ -z "${buildnumber}" ]; then
    echo "--buildnumber is unset or set to the empty string"
    usage
    exit 1
fi

if [ -z "${projectkey}" ]; then
    buildsha256=$(jf xr curl  -H "Content-Type: application/json" -XPOST "api/v1/dependencyGraph/build" -d '{
    "build_name":"'$buildname'",
    "build_number":"'$buildnumber'"
}'  | jq -r '.build.sha256')
else
    buildsha256=$(jf xr curl  -H "Content-Type: application/json" -XPOST "api/v1/dependencyGraph/build" -d '{
    "build_name":"'$buildname'",
    "build_number":"'$buildnumber'", "project":"'$projectkey'"
}'  | jq -r '.build.sha256')
fi
echo "Generating SBOM for build $buildname $buildnumber"
jf xr curl -XPOST api/v1/component/exportDetails \
    -H "Content-type: application/json" \
    -d '{"violations":true, "include_ignored_violations": true,
    "license": true, "security": true, "exclude_unknown": true,
    "spdx": true, "spdx_format": "json",
    "component_name": "'$buildname':'$buildnumber'",
    "package_type":"build", "sha_256":"'$buildsha256'", "output_format":"json"}'   --output build-report-$buildname-$buildnumber.zip
