#!/bin/bash

source "${BASH_SOURCE%/*}/common.sh"

. "$(git --exec-path)/git-sh-setup"

if [ -z "$1" ] ; then
    c_echo $RED "Need to provide the version ie v0.0.0 as the first argument"
    exit 1
fi

# Confirmation message, take two arguments
confirmation()
{
    c_echo $YELLOW "
--------------------------------------------------------------------------------
--                                Confirmation                                --
--------------------------------------------------------------------------------
"
    c_echo $YELLOW "You are about to release the following..."
    echo
    c_echo $YELLOW "$1"
    c_echo $YELLOW "Are you sure you want to continue? (Default: y)"
    read -r CONFIRMATION
    if [[ -z $CONFIRMATION ]]; then
        CONFIRMATION="y"
    fi
    if [[ $CONFIRMATION != "y" ]]; then
        c_echo $RED "Exiting..."
        exit 1
    fi
}

VERSION=$1
VERSION_BUMP=${VERSION:1}
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Require valid format for version
rx='^v[0-9]+\.[0-9]+\.[0-9]+$'
if ! [[ $VERSION =~ $rx ]]; then
    c_echo $RED "The version must be in the format 'vX.X.X'"
    exit 1
fi

# Require main branch for release
if [ "$BRANCH" != "main" ]
then
    c_echo $RED "You must release on the main branch"
    exit 1
fi

# make sure you have the most recent from remote main
git fetch
git pull origin main

if [ x"$(git rev-parse $BRANCH)" != x"$(git rev-parse origin/$BRANCH)" ]
then
    c_echo $RED "Out of sync with remote"
    git status
    exit 1
fi

# Require no untracked files
if [[ -n $(git status -s) ]]
then
    c_echo $RED "Untracked files detected. Please stash or commit"
    git status -s
    exit 1
fi

# Require new tag/version
if [ $(git tag -l "$VERSION") ]; then
    c_echo $RED "The tag/version already exists..."
    echo
    echo Tags:
    git tag
    exit 1
fi

# Require clean working tree for release
require_clean_work_tree release "Please commit or stash them and sync with remote"

# Get most recent tag
PREVIOUS_TAG=$(git describe --tags --abbrev=0)

# Build commit message for version bump
MESSAGE="Release: $VERSION

Changes:

$(git log --pretty=oneline $PREVIOUS_TAG..)

Diff:

https://github.com/sarfrazahmad307/$APP_NAME/compare/$PREVIOUS_TAG...$VERSION
"

# Confirmation message
confirmation "$MESSAGE"

c_echo $GREEN "Releasing Version $VERSION"
echo

# Modify the VERSION file
printf "$VERSION" > ./VERSION

# Commit and tag the release
git add ./VERSION
git commit -m "🚀 $MESSAGE"
git tag $VERSION
git push origin $BRANCH
git push origin $VERSION

gh release create "$VERSION" --generate-notes
echo "Release $VERSION created."