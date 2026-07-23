#!/bin/sh
# Non-destructive current-source proof gate for the Smithian Fold corpus.
#
# This command copies only the ErnosPlain derivation/test sources and required
# committed data into an isolated temporary directory. It compiles and executes
# every current test there. It never rewrites tests/, verify/, or committed C.

set -u

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
project_root=$(CDPATH= cd -- "$script_dir/.." && pwd)

if command -v ernos >/dev/null 2>&1; then
    ernos_command=ernos
elif [ -x "$project_root/compiler/target/release/ernos" ]; then
    ernos_command="$project_root/compiler/target/release/ernos"
else
    echo "ERROR: ErnosPlain compiler 'ernos' was not found."
    exit 1
fi

isolated_root=$(mktemp -d /private/tmp/sft-current-source.XXXXXX)
mkdir "$isolated_root/tests"
cp -R "$project_root/foundation" "$isolated_root/foundation"
cp -R "$project_root/constants" "$isolated_root/constants"
cp -R "$project_root/data" "$isolated_root/data"

for source_path in "$project_root"/tests/test_*.ep; do
    cp "$source_path" "$isolated_root/tests/"
done

cd "$isolated_root/tests" || exit 1

suite_total=0
check_total=0

for source_file in test_*.ep; do
    test_name=${source_file%.ep}
    compile_output=$($ernos_command "$source_file" 2>&1)
    compile_status=$?
    if [ "$compile_status" -ne 0 ]; then
        echo "COMPILE_FAIL $test_name"
        printf '%s\n' "$compile_output"
        exit 1
    fi

    run_output=$("./$test_name" 2>&1)
    run_status=$?
    if [ "$run_status" -ne 0 ]; then
        echo "RUN_FAIL $test_name exit=$run_status"
        printf '%s\n' "$run_output"
        exit 1
    fi

    if printf '%s\n' "$run_output" | rg -q "FAIL"; then
        echo "ASSERT_FAIL $test_name"
        printf '%s\n' "$run_output" | rg "FAIL"
        exit 1
    fi

    current_checks=$(printf '%s\n' "$run_output" | rg -c "^[[:space:]]+(ok|PASS)[[:space:]]" || true)
    suite_total=$((suite_total + 1))
    check_total=$((check_total + current_checks))

    if [ $((suite_total % 25)) -eq 0 ]; then
        echo "PROGRESS suites=$suite_total checks=$check_total last=$test_name"
    fi
done

if [ "$suite_total" -ne 409 ]; then
    echo "MANIFEST_FAIL expected_suites=409 got=$suite_total"
    exit 1
fi

if [ "$check_total" -ne 2693 ]; then
    echo "MANIFEST_FAIL expected_checks=2693 got=$check_total"
    exit 1
fi

identical_certificates=0
drifted_certificates=0
absent_certificates=0

for generated_c in "$isolated_root"/tests/test_*_compiled.c; do
    generated_name=${generated_c##*/}
    certificate_name=${generated_name%_compiled.c}.c
    committed_certificate="$project_root/verify/$certificate_name"

    if [ ! -f "$committed_certificate" ]; then
        echo "CERTIFICATE_ABSENT $certificate_name"
        absent_certificates=$((absent_certificates + 1))
    elif diff -q "$generated_c" "$committed_certificate" >/dev/null; then
        identical_certificates=$((identical_certificates + 1))
    else
        echo "CERTIFICATE_DRIFTED $certificate_name"
        drifted_certificates=$((drifted_certificates + 1))
    fi
done

certificate_total=$((identical_certificates + drifted_certificates + absent_certificates))
if [ "$certificate_total" -ne "$suite_total" ]; then
    echo "CERTIFICATE_MANIFEST_FAIL suites=$suite_total certificates=$certificate_total"
    exit 1
fi

echo "CURRENT_SOURCE_COMPLETE suites=$suite_total checks=$check_total failures=0"
echo "CERTIFICATE_COMPARE identical=$identical_certificates drifted=$drifted_certificates absent=$absent_certificates total=$certificate_total"
echo "ISOLATED_BUILD=$isolated_root"
