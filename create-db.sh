CREATEDB_VERSION=`createdb --version`

if [[ $? -ne 0 ]]; then
  echo 'createdb health check returned non-zero code. please check that postgres is correctly installed'
  exit 1
fi

# case insensitive regex
shopt -s nocasematch

if [[ ! $CREATEDB_VERSION =~ .*PostgreSQL*. ]]; then
  echo 'createdb command may not belong to postgres. please check'
  exit 1
fi

echo "$PGHOST"

echo "Config: PG-Host: $PGHOST, PG-Port: $PGPORT, PG-User: $PGUSER\nCreating database $PGDATABASE"

createdb -e

if [[ $? -ne 0 ]]; then
  echo 'createdb exited with non-zero exit code'
  exit 1
fi
