#!/bin/bash
set -eo pipefail

function fetch-and-install-chaostoolkit-packages() {
    cd extensions-doc-builder
    mkdir deps

    pip install --pre -U chaostoolkit-lib chaostoolkit
    pip install httplib2 uritemplate pytzdata
    
    # collect all the dependencies for our drivers
    pip install -U -r requirements-toolkit.txt

    # now let's get them as archives for building their docs
    pip download \
        --no-deps \
        --no-cache-dir \
        --dest deps \
        --no-binary=chaostoolkit-aws,chaostoolkit-azure,chaostoolkit-cloud-foundry,chaostoolkit-google-cloud,chaostoolkit-humio,chaostoolkit-kubernetes,chaostoolkit-prometheus,chaostoolkit-spring,chaostoolkit-toxiproxy,chaostoolkit-opentracing \
        -r requirements-toolkit.txt

    cd deps
    for archive in *.tar.gz;
    do
        tar zxvf "$archive"
        dirname=$(basename $archive .tar.gz)
        cd $dirname
        python setup.py develop
        cd ..
    done
    cd ../..
}

function build-drivers-doc () {
    cd extensions-doc-builder

    if python ext2md.py; then
        echo "Extension documentation built"
    fi

    cd ..
}

function build-docs () {
    echo "Building the documentation"
    mkdir /tmp/site
    cd /tmp/site
    git clone https://$GH_USER_NAME:$GH_USER_PWD@github.com/chaostoolkit/chaostoolkit-documentation.git .
    git checkout gh-pages
    cd -
    mkdocs build --strict -d /tmp/site
}

function publish-docs () {
    echo "Publishing the documentation"
    echo `pwd`
    cd /tmp/site
    echo "docs.chaostoolkit.org" > CNAME
    git add .
    git commit -a -m "Built from ${TRAVIS_COMMIT}"
    git push
}

function main () {
    fetch-and-install-chaostoolkit-packages || return 1
    build-drivers-doc || return 1
    #build-docs || return 1

    if [[ "$TRAVIS_BRANCH" == "master" ]] && [[ "$TRAVIS_PULL_REQUEST" == false ]]; then
        # build docs on each commit but only from master
        publish-docs || return 1
    fi
}

main "$@" || exit 1
exit 0
