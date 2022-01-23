#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJ_DIR=$( dirname "$SCRIPT_DIR")

cd $PROJ_DIR
docker build -f Dockerfile.unittest -t todotestproject .

docker run -d --name todotest \
  --mount type=bind,source=$PROJ_DIR,target=$PROJ_DIR \
  -w $PROJ_DIR \
  todotestproject /bin/bash \
  -c "nosetests --tests=tests -v --nologcapture --exe --with-xunit --xunit-file=test_reports/xunit-results.xml --with-coverage --cover-package=. --cover-html --cover-html-dir=test_reports/cov --cover-erase"

docker logs -f todotest
docker rm todotest
rm -rf .coverage