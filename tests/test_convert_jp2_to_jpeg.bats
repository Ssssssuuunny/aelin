#!/usr/bin/env bats

setup() {
    # Create temporary test directory
    TEST_DIR=$(mktemp -d)
    SCRIPT="$BATS_TEST_DIRNAME/../convert/convert-jp2-to-jpeg.sh"
}

teardown() {
    # Clean up test directory
    rm -rf "$TEST_DIR"
}

@test "script converts jp2 files and skips already converted ones" {
    # Copy fixture files to test directory
    cp "$BATS_TEST_DIRNAME/fixtures/sampleToConvert.jp2" "$TEST_DIR/"
    cp "$BATS_TEST_DIRNAME/fixtures/sampleToSkip.jp2" "$TEST_DIR/"
    cp "$BATS_TEST_DIRNAME/fixtures/sampleToSkip.jpg" "$TEST_DIR/"
    
    # Run script
    bash "$SCRIPT" "$TEST_DIR" 1
    
    # Check that sampleForConversion.jp2 was converted
    [ -f "$TEST_DIR/sampleToConvert.jpg" ]
    
    # Check that sampleToSkip.jp2 was NOT listed for conversion
    run grep "sampleToSkip.jp2" /tmp/toconvert2jp2.txt
    [ "$status" -eq 1 ]
}

