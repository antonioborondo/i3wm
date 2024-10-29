#! /bin/bash

find . -type d -exec chmod 700 {} \;
find . -type f -not -name fix_permissions.sh -exec chmod 600 {} \;
find . -type f -name fix_permissions.sh -or -path './.local/bin/*' -exec chmod 700 {} \;
