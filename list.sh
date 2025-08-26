#!/bin/bash

if [[ "$1" == "-u" || "$1" == "--update" ]]; then
  shift
  node update-item.js "$@"
else
  node show-active-items.js
fi