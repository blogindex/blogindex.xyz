#!/usr/bin/env bash
if [ -f "${RESULT_LOCATION}.txt" ]; then
    cat ${RESULT_LOCATION}.txt
else
    echo "Log unsuccessfully captured."
fi

if [ -d "${RESULT_LOCATION}" ]; then
    echo "results are available at https://results.blogindex.dev/${RESULT_LOCATION}"
else
    echo "An unknown error has occurred.\nResults are not available for this test."
fi