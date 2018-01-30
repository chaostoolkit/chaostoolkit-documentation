#!/bin/bash
set -eo pipefail

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
    cd /tmp/site
    echo "chaostoolkit.org" > CNAME
    git add .
    git commit -a -m "Built from ${TRAVIS_COMMIT}"
    git push
}

function main () {
    build-docs || return 1

    if [[ "$TRAVIS_BRANCH" == "master" ]] && [[ "$TRAVIS_PULL_REQUEST" == false ]]; then
        # build docs on each commit but only from master
        publish-docs || return 1
    fi
}

main "$@" || exit 1
exit 0
