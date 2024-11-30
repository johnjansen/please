import pytest
from please.core.processor import CommandProcessor
from please.models.command import Command

def test_processor_initialization():
    """Test that CommandProcessor initializes correctly"""
    processor = CommandProcessor()
    assert isinstance(processor, CommandProcessor)
    assert hasattr(processor, 'commands')

def test_empty_command():
    """Test that empty commands raise ValueError"""
    processor = CommandProcessor()
    with pytest.raises(ValueError, match="Please provide a command"):
        processor.process("")
    with pytest.raises(ValueError, match="Please provide a command"):
        processor.process("   ")

def test_unknown_command():
    """Test that unknown commands raise ValueError"""
    processor = CommandProcessor()
    with pytest.raises(ValueError, match="I don't know how to do_something_unknown"):
        processor.process("do_something_unknown")
