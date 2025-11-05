#!/bin/bash

if [[ "$1" == "-u" || "$1" == "--update" ]]; then
  shift
  node ./js/update-item.js "$@"
else
  node ./js/show-active-items.js
fi