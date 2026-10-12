#!/bin/zsh
set -euo pipefail

MYSQL_BIN=/opt/homebrew/opt/mysql@8.4/bin
CNF=/Users/sam/mysql.cnf
DATADIR=/Users/sam/mysql-data
SOCK=/tmp/mysql-sam.sock

if [[ -S "$SOCK" ]] && "$MYSQL_BIN/mysqladmin" --defaults-file="$CNF" ping >/dev/null 2>&1; then
  echo "Sam MySQL is already running on port 3307"
  exit 0
fi

"$MYSQL_BIN/mysqld" --defaults-file="$CNF" --daemonize
echo "Started Sam MySQL on port 3307 (data: $DATADIR)"
