#!/bin/awk -f

function red(s) {
    return "\033[1;31m" s "\033[0m "
}

/idle_age=.,/ { $0 = red($0) }
{ print }

