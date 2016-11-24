
pushd ${1}

hadd -f redBkg_${2}.root data*_${2}.root

popd
