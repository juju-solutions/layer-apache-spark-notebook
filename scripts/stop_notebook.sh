#!/bin/bash

PID=`pgrep -f 'ipython.*notebook'`
if [ -n "${PID}" ]; then
  kill ${PID}
fi
