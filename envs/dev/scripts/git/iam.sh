#!/usr/bin/env bash


cat << EOM
---------------------------------------------------------

This script will help you setup your git name and email
associated with this repository. It is needed to attach
a correct information to your commits in this repo.

You're probably working with different repositories
under different name/email configurations, so this script
is a helper for you to configure these things.

Your global git configuration won't be touched.
This script will just append your name and email
configuration to the local .git/config file of this repo.

---------------------------------------------------------

EOM


echo "Enter the name you want to appear in your commits:"
read name

echo ""

echo "Enter the email you use to access this repository:"
read email

git config user.name "$name"
git config user.email "$email"

echo ""
echo "Your info has been successfully added to .git/config"
