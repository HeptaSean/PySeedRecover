#!/bin/sh
echo "pydocstyle"
echo "=========="
if pydocstyle $1
then echo "OK"
fi
echo
echo "pycodestyle"
echo "==========="
if pycodestyle $1
then echo "OK"
fi
echo
echo "mypy"
echo "===="
mypy $1
echo
echo "doctest"
echo "======="
if python -m doctest $1
then echo "OK"
fi
echo
echo "TODO"
echo "===="
if ! grep TODO $1
then echo "OK"
fi
