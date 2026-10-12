#!/bin/zsh
set -euo pipefail

MYSQL_BIN=/opt/homebrew/opt/mysql@8.4/bin
CNF=/Users/sam/mysql.cnf

"$MYSQL_BIN/mysqladmin" --defaults-file="$CNF" -p shutdown  # prompts for the root password
echo "Stopped Sam MySQL"
