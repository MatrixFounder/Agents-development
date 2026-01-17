"""
Unit tests for task_id_tool.py

Tests cover:
- Auto-generation of IDs (proposed_id=None)
- Proposed ID validation (free/occupied)
- Conflict handling (allow_correction=True/False)
- Slug normalization
- Edge cases
"""

import os
import tempfile
import pytest

from task_id_tool import (
    normalize_slug,
    get_existing_task_ids,
    find_next_available_id,
    generate_task_archive_filename
)


class TestNormalizeSlug:
    """Tests for slug normalization."""
    
    def test_lowercase_conversion(self):
        assert normalize_slug("NewFeature") == "newfeature"
    
    def test_spaces_to_dashes(self):
        assert normalize_slug("new feature") == "new-feature"
    
    def test_underscores_to_dashes(self):
        assert normalize_slug("new_feature") == "new-feature"
    
    def test_remove_special_chars(self):
        assert normalize_slug("new!@#$%feature") == "newfeature"
    
    def test_consecutive_dashes(self):
        assert normalize_slug("new---feature") == "new-feature"
    
    def test_leading_trailing_dashes(self):
        assert normalize_slug("-new-feature-") == "new-feature"
    
    def test_mixed_case_spaces_underscores(self):
        assert normalize_slug("My New_Feature Test") == "my-new-feature-test"
    
    def test_empty_slug(self):
        assert normalize_slug("") == "untitled"
    
    def test_only_special_chars(self):
        assert normalize_slug("!@#$%") == "untitled"


class TestGetExistingTaskIds:
    """Tests for extracting task IDs from directory."""
    
    def test_empty_directory(self, tmp_path):
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        assert get_existing_task_ids(str(tasks_dir)) == []
    
    def test_nonexistent_directory(self, tmp_path):
        tasks_dir = tmp_path / "nonexistent"
        assert get_existing_task_ids(str(tasks_dir)) == []
    
    def test_single_task(self, tmp_path):
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        (tasks_dir / "task-001-test.md").touch()
        assert get_existing_task_ids(str(tasks_dir)) == [1]
    
    def test_multiple_tasks(self, tmp_path):
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        (tasks_dir / "task-001-first.md").touch()
        (tasks_dir / "task-005-second.md").touch()
        (tasks_dir / "task-010-third.md").touch()
        result = sorted(get_existing_task_ids(str(tasks_dir)))
        assert result == [1, 5, 10]
    
    def test_ignores_non_matching_files(self, tmp_path):
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        (tasks_dir / "task-001-valid.md").touch()
        (tasks_dir / "README.md").touch()
        (tasks_dir / "task-abc-invalid.md").touch()
        (tasks_dir / "not-a-task.md").touch()
        assert get_existing_task_ids(str(tasks_dir)) == [1]
    
    def test_supports_four_digit_ids(self, tmp_path):
        """Test that IDs beyond 999 are properly handled."""
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        (tasks_dir / "task-999-old.md").touch()
        (tasks_dir / "task-1000-newer.md").touch()
        (tasks_dir / "task-1001-newest.md").touch()
        result = sorted(get_existing_task_ids(str(tasks_dir)))
        assert result == [999, 1000, 1001]


class TestFindNextAvailableId:
    """Tests for finding next available ID."""
    
    def test_empty_list(self):
        assert find_next_available_id([]) == 1
    
    def test_single_id(self):
        assert find_next_available_id([1]) == 2
    
    def test_gap_in_ids(self):
        # Should return max + 1, NOT fill gaps
        assert find_next_available_id([1, 5, 10]) == 11
    
    def test_start_from_higher(self):
        assert find_next_available_id([1, 2, 3], start_from=10) == 10
    
    def test_start_from_lower_than_max(self):
        assert find_next_available_id([1, 5, 10], start_from=3) == 11


class TestGenerateTaskArchiveFilename:
    """Integration tests for the main function."""
    
    def test_auto_generate_empty_dir(self, tmp_path):
        tasks_dir = tmp_path / "tasks"
        # Don't create dir - function should create it
        
        result = generate_task_archive_filename(
            slug="new-feature",
            tasks_dir=str(tasks_dir)
        )
        
        assert result["status"] == "generated"
        assert result["filename"] == "task-001-new-feature.md"
        assert result["used_id"] == "001"
        assert result["message"] is None
        assert tasks_dir.exists()
    
    def test_auto_generate_with_existing_tasks(self, tmp_path):
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        (tasks_dir / "task-005-old.md").touch()
        
        result = generate_task_archive_filename(
            slug="new-feature",
            tasks_dir=str(tasks_dir)
        )
        
        assert result["status"] == "generated"
        assert result["filename"] == "task-006-new-feature.md"
        assert result["used_id"] == "006"
    
    def test_proposed_id_available(self, tmp_path):
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        (tasks_dir / "task-001-old.md").touch()
        
        result = generate_task_archive_filename(
            slug="new-feature",
            proposed_id="050",
            tasks_dir=str(tasks_dir)
        )
        
        assert result["status"] == "generated"
        assert result["filename"] == "task-050-new-feature.md"
        assert result["used_id"] == "050"
    
    def test_proposed_id_occupied_with_correction(self, tmp_path):
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        (tasks_dir / "task-031-old.md").touch()
        
        result = generate_task_archive_filename(
            slug="new-feature",
            proposed_id="31",
            allow_correction=True,
            tasks_dir=str(tasks_dir)
        )
        
        assert result["status"] == "corrected"
        assert result["filename"] == "task-032-new-feature.md"
        assert result["used_id"] == "032"
        assert "031" in result["message"]
        assert "032" in result["message"]
    
    def test_proposed_id_occupied_without_correction(self, tmp_path):
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        (tasks_dir / "task-031-old.md").touch()
        
        result = generate_task_archive_filename(
            slug="new-feature",
            proposed_id="31",
            allow_correction=False,
            tasks_dir=str(tasks_dir)
        )
        
        assert result["status"] == "conflict"
        assert result["filename"] is None
        assert result["used_id"] is None
        assert "031" in result["message"]
        assert "032" in result["message"]
    
    def test_invalid_proposed_id(self, tmp_path):
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        
        result = generate_task_archive_filename(
            slug="new-feature",
            proposed_id="abc",
            tasks_dir=str(tasks_dir)
        )
        
        assert result["status"] == "error"
        assert result["filename"] is None
        assert "Invalid ID format" in result["message"]
    
    def test_negative_proposed_id(self, tmp_path):
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        
        result = generate_task_archive_filename(
            slug="new-feature",
            proposed_id="-5",
            tasks_dir=str(tasks_dir)
        )
        
        assert result["status"] == "error"
        assert "Invalid ID format" in result["message"]
    
    def test_slug_normalization_in_output(self, tmp_path):
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        
        result = generate_task_archive_filename(
            slug="My New Feature!!!",
            tasks_dir=str(tasks_dir)
        )
        
        assert result["filename"] == "task-001-my-new-feature.md"
    
    def test_proposed_id_short_format(self, tmp_path):
        """Test that '31' is correctly formatted as '031'."""
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        
        result = generate_task_archive_filename(
            slug="feature",
            proposed_id="31",
            tasks_dir=str(tasks_dir)
        )
        
        assert result["used_id"] == "031"
        assert result["filename"] == "task-031-feature.md"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
