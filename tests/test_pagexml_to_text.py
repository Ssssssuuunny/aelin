#!/usr/bin/env python3
"""
Tests for pagexml-to-text.py

Usage: pytest tests/test_pagexml_to_text.py
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "conversion"))
import importlib.util
spec = importlib.util.spec_from_file_location(
    "pagexml_to_text",
    Path(__file__).parent.parent / "conversion" / "pagexml-to-text.py"
)
pagexml_to_text = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pagexml_to_text)


@pytest.fixture
def sample_pagexml():
    """Create a comprehensive PageXML file for testing all parameters"""
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<PcGts xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15">
    <Page imageFilename="test.jpg">
        <TextRegion id="r1">
            <TextLine id="l1">
                <Coords points="100,200 200,200 200,220 100,220"/>
                <TextEquiv>
                    <PlainText>Hyphen-</PlainText>
                </TextEquiv>
            </TextLine>
            <TextLine id="l2">
                <Coords points="100,230 200,230 200,250 100,250"/>
                <TextEquiv>
                    <PlainText>ated word.</PlainText>
                </TextEquiv>
            </TextLine>
        </TextRegion>
        <TextRegion id="r2">
            <TextLine id="l3">
                <Coords points="100,300 200,300 200,320 100,320"/>
                <TextEquiv>
                    <PlainText>First sentence.</PlainText>
                </TextEquiv>
            </TextLine>
            <TextLine id="l4">
                <Coords points="100,330 200,330 200,350 100,350"/>
                <TextEquiv>
                    <PlainText>Second sentence.</PlainText>
                </TextEquiv>
            </TextLine>
        </TextRegion>
        <TextRegion id="r3">
            <TextLine id="l5">
                <Coords points="100,500 200,500 200,520 100,520"/>
                <TextEquiv>
                    <PlainText>List item:</PlainText>
                </TextEquiv>
            </TextLine>
            <TextLine id="l6">
                <Coords points="100,530 200,530 200,550 100,550"/>
                <TextEquiv>
                    <PlainText>Description here.</PlainText>
                </TextEquiv>
            </TextLine>
        </TextRegion>
    </Page>
</PcGts>'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False, encoding='utf-8') as f:
        f.write(xml_content)
        temp_path = f.name
    
    yield temp_path
    os.unlink(temp_path)


def test_separate_single_words(sample_pagexml):
    """Test that single-word lines remain separate when enabled"""
    lines = pagexml_to_text.read_pagexml_file(
        sample_pagexml,
        separate_single_words=True,
        merge_dashes=False,
        split_periods=False,
        merge_quotes=False,
        separate_colons=False
    )
    
    # "Hyphen-" should be separate, not merged with "ated word."
    assert "Hyphen-" in lines
    assert "Hyphen- ated word." not in lines


def test_merge_dashes(sample_pagexml):
    """Test hyphenated word merging at line breaks"""
    lines = pagexml_to_text.read_pagexml_file(
        sample_pagexml,
        separate_single_words=False,
        merge_dashes=True,
        split_periods=False,
        merge_quotes=False,
        separate_colons=False
    )
    
    # Should join "Hyphen-" and "ated" without hyphen
    assert any("Hyphenated word." in line for line in lines)


def test_split_periods(sample_pagexml):
    """Test splitting on periods before capital letters"""
    lines = pagexml_to_text.read_pagexml_file(
        sample_pagexml,
        separate_single_words=False,
        merge_dashes=False,
        split_periods=True,
        merge_quotes=False,
        separate_colons=False
    )
    
    # Should keep sentences separate
    assert "First sentence." in lines
    assert "Second sentence." in lines


def test_separate_colons(sample_pagexml):
    """Test keeping lines ending with colons separate"""
    lines = pagexml_to_text.read_pagexml_file(
        sample_pagexml,
        separate_single_words=False,
        merge_dashes=False,
        split_periods=False,
        merge_quotes=False,
        separate_colons=True
    )
    
    # Should keep lines with colons separate
    assert "List item:" in lines
    assert "Description here." in lines


def test_main_function_creates_output(sample_pagexml):
    """Test that main function creates output files"""
    with tempfile.TemporaryDirectory() as input_dir:
        with tempfile.TemporaryDirectory() as output_dir:
            # Copy sample XML to input directory
            import shutil
            xml_path = os.path.join(input_dir, "test.xml")
            shutil.copy(sample_pagexml, xml_path)
            
            # Run main function
            pagexml_to_text.main(
                input_dir=input_dir,
                output_dir=output_dir,
                separate_single_words=False,
                merge_dashes=False,
                split_periods=False,
                merge_quotes=False,
                separate_colons=False
            )
            
            # Check output file was created
            output_file = os.path.join(output_dir, "test.txt")
            assert os.path.exists(output_file)
            
            # Check content
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "Description here." in content
