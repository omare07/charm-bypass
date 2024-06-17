#!/bin/sh
#
# html-tidy5 does not yet support the minlength attributes
# that we use on our daily security code inputs,
#
#  https://github.com/htacg/tidy-html5/issues/1101
#
# so we use sed to preprocess them out before calling tidy.
#
sed -e 's/minlength="[0-9]*"//g' index.html | tidy > /dev/null
