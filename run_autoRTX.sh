#!/bin/sh

CONTAINER_NAME="AutoRTX-python2.7"
#コンテナ名定義

OLD="$(docker ps --all --quiet --filter=name="$CONTAINER_NAME")"
if [ -n "$OLD" ]; then
    docker exec -it \
    ${CONTAINER_NAME} "$@"
else
  echo 'No such container!' 1>&2
  exit 1
fi
#コンテナ一覧で、該当名前のコンテナあるかをチェック
#あった場合、コマンドを実行
#ない場合、エラーメッセージ出力