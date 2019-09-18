rm -r swarmrobw
rm -r swarmrob
cp -R ../../../../swarmrobw .
cp -R ../../../../swarmrob .
docker build -t swarmrob_test:ubuntu_18_04 .
