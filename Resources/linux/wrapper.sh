#!/bin/bash
echo 'export VISTAR=/Some/Path:$VISTAR' >> /etc/profile.d/vistar.sh
exec "$@"
