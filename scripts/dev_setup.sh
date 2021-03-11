#!/bin/bash

# Prior to running this script:
# git clone git@github.com:brucewroberts/form_990.git
# cd form_990

set -x
set -e
set -o pipefail

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

for system in python mariadb
do
    brew list ${system} &>/dev/null || brew install ${system}
done

pushd ..

virtualenv venv
. venv/bin/activate

pip3 install -r requirements.txt

mkdir -p instance

PASSWORD=`make_secret`
SECRET=`make_secret`

cat > instance/app.cnf <<EOF
[database-dev]
host = localhost
database = form990
user = form990-dev
password = ${PASSWORD}
connection_timeout = 30
use_ssl = false

[app-secret-dev]
secret = ${SECRET}

EOF

mysql.server start

cat <<EOF
************************************************************************
Running the server:

cd form_990
./devrun

Testing:

TODO
************************************************************************
EOF


