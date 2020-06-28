#!/bin/bash

echo
echo "************** START: test_client.sh **********************"

# Create temporary testing directory
echo "Creating temporary directory to work in."
here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

. $here/helpers.sh

unset GITHUB_REPOSITORY || true

# Create temporary testing directory
tmpdir=$(mktemp -d)
output=$(mktemp ${tmpdir:-/tmp}/rse_test.XXXXXX)
printf "Created temporary directory to work in. ${tmpdir}\n"

# Copy executable to testing space (should work outside of repo)
a2z="${tmpdir}/a2z.py"
cp a2z.py "${a2z}"

runTest 0 $output ls $a2z

echo
echo "#### Testing a2z init without GitHub repository defined"
runTest 1 $output python $a2z init --filename $tmpdir/.all-contributorsrc

echo
echo "#### Testing a2z init with GitHub repository defined"
runTest 0 $output python $a2z init --filename $tmpdir/.all-contributorsrc singularityhub/sregistry
runTest 0 $output ls $tmpdir/.all-contributorsrc

echo
echo "#### Testing a2z init existing outfile without force"
runTest 1 $output python $a2z init --filename $tmpdir/.all-contributorsrc singularityhub/sregistry

echo
echo "#### Testing a2z init existing outfile with force"
runTest 0 $output python $a2z init --filename $tmpdir/.all-contributorsrc --force singularityhub/sregistry
runTest 0 $output ls $tmpdir/.all-contributorsrc
rm $tmpdir/.all-contributorsrc

echo
echo "#### Testing a2z init with GitHub repository defined in environment"
export GITHUB_REPOSITORY=singularityhub/sregistry
runTest 0 $output python $a2z init --filename $tmpdir/.all-contributorsrc
runTest 0 $output ls $tmpdir/.all-contributorsrc
rm $tmpdir/.all-contributorsrc

echo
echo "#### Testing a2z init with malformed name"
runTest 1 $output python $a2z init --filename $tmpdir/.all-contributorsrc pancakes-hub

echo
echo "#### Testing a2z init with zenodo DOI"
runTest 0 $output python $a2z init --zenodo 10.5281/zenodo.1012531 --zenodo-file $tmpdir/.zenodo.json singularityhub/sregistry

echo
echo "#### Testing a2z init with zenodo DOI without force"
runTest 1 $output python $a2z init --zenodo 10.5281/zenodo.1012531 --zenodo-file $tmpdir/.zenodo.json singularityhub/sregistry

echo "#### Testing a2z init with zenodo DOI with force"
runTest 0 $output python $a2z init --zenodo 10.5281/zenodo.1012531 --zenodo-file $tmpdir/.zenodo.json  --force singularityhub/sregistry

echo "#### Testing a2z update zenodo"
runTest 0 $output python $a2z update zenodo singularityhub/sregistry --zenodo-file $tmpdir/.zenodo.json

echo "#### Testing a2z update allcontrib"
runTest 0 $output python $a2z init --filename $tmpdir/.all-contributorsrc
runTest 0 $output python $a2z update allcontrib --filename $tmpdir/.all-contributorsrc

echo "#### Testing a2z update all"
runTest 0 $output python $a2z update all --filename $tmpdir/.all-contributorsrc --zenodo-file $tmpdir/.zenodo.json

rm -rf ${tmpdir}
