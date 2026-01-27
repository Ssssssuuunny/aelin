#!/usr/bin/env bats

setup() {
    TEST_DIR=$(mktemp -d)
    OUTPUT_DIR=$(mktemp -d)
    SCRIPT="$BATS_TEST_DIRNAME/../convert/create-image-cache.sh"
    FIXTURES_DIR="$BATS_TEST_DIRNAME/fixtures"
    
    mkdir -p "$TEST_DIR/subdir"
    cp "$FIXTURES_DIR/sampleToConvert.jp2" "$TEST_DIR/sample.jp2"
    cp "$FIXTURES_DIR/sampleToConvert.jp2" "$TEST_DIR/subdir/sample2.jp2"
}

teardown() {
    rm -rf "$TEST_DIR" "$OUTPUT_DIR"
}

@test "creates valid JPEG thumbnails" {
    bash "$SCRIPT" "$TEST_DIR" "$OUTPUT_DIR"
    
    run identify "$OUTPUT_DIR/$TEST_DIR/sample.jp2.thumbnail.jpg"
    [ "$status" -eq 0 ]
}

@test "preserves subdirectory structure" {
    bash "$SCRIPT" "$TEST_DIR" "$OUTPUT_DIR"
    
    [ -f "$OUTPUT_DIR/$TEST_DIR/subdir/sample2.jp2.thumbnail.jpg" ]
}