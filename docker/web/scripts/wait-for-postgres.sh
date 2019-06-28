#!/bin/sh
# wait-for-postgres.sh

set -e

host="$1"
shift
port="$1"
shift
cmd="$@"

while ! pg_isready -h $host -p $port > /dev/null 2> /dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
