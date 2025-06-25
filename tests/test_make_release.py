#!/usr/bin/env python3
"""
Tests for Release Management Script

Tests the make_release.py script including version bumping, changelog generation,
git operations, and error handling.
"""

import os
import sys
import tempfile
import shutil
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from make_release import ReleaseManager, ReleaseError


class TestReleaseManager:
    """Test ReleaseManager class initialization and basic functionality"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp(prefix=f"release_test_{method.__name__}_"))
        self.src_dir = self.test_dir / "src"
        self.src_dir.mkdir(parents=True)
        
        # Create mock version file
        self.version_file = self.src_dir / "__init__.py"
        self.version_content = '''#!/usr/bin/env python3
"""Package initialization"""

__version__ = "1.0.0"
__author__ = "Test Author"
'''
        self.version_file.write_text(self.version_content, encoding='utf-8')
        
        self.release_manager = ReleaseManager(str(self.test_dir))
    
    def teardown_method(self, method):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_init_default_project_root(self):
        """Test ReleaseManager initialization with default project root"""
        manager = ReleaseManager()
        assert manager.project_root == Path(".")
        assert manager.version_file == Path(".") / "src" / "__init__.py"
        assert manager.changelog_file == Path(".") / "CHANGELOG.md"
    
    def test_init_custom_project_root(self):
        """Test ReleaseManager initialization with custom project root"""
        assert self.release_manager.project_root == self.test_dir
        assert self.release_manager.version_file == self.test_dir / "src" / "__init__.py"
        assert self.release_manager.changelog_file == self.test_dir / "CHANGELOG.md"
    
    def test_commit_patterns_exist(self):
        """Test that commit categorization patterns are defined"""
        patterns = self.release_manager.commit_patterns
        
        expected_categories = [
            "added", "changed", "deprecated", "removed", "fixed", 
            "security", "docs", "tests", "refactor", "style", "chore"
        ]
        
        for category in expected_categories:
            assert category in patterns
            assert isinstance(patterns[category], list)
            assert len(patterns[category]) > 0


class TestVersionParsing:
    """Test version parsing and bumping functionality"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp(prefix=f"version_test_{method.__name__}_"))
        self.src_dir = self.test_dir / "src"
        self.src_dir.mkdir(parents=True)
        self.release_manager = ReleaseManager(str(self.test_dir))
    
    def teardown_method(self, method):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def create_version_file(self, version: str):
        """Helper to create version file with specific version"""
        version_file = self.src_dir / "__init__.py"
        content = f'''#!/usr/bin/env python3
"""Package initialization"""

__version__ = "{version}"
__author__ = "Test Author"
'''
        version_file.write_text(content, encoding='utf-8')
    
    def test_parse_current_version_valid(self):
        """Test parsing valid version numbers"""
        test_versions = ["1.0.0", "2.5.10", "0.1.0", "10.20.30"]
        
        for version in test_versions:
            self.create_version_file(version)
            major, minor, patch = self.release_manager.parse_current_version()
            expected_parts = [int(x) for x in version.split('.')]
            assert (major, minor, patch) == tuple(expected_parts)
    
    def test_parse_current_version_file_not_found(self):
        """Test parsing when version file doesn't exist"""
        with pytest.raises(ReleaseError, match="Version file not found"):
            self.release_manager.parse_current_version()
    
    def test_parse_current_version_invalid_format(self):
        """Test parsing with invalid version format"""
        invalid_versions = [
            '__version__ = "1.0"',  # Missing patch
            '__version__ = "v1.0.0"',  # Has 'v' prefix
            '__version__ = "1.0.0-beta"',  # Has suffix
            'version = "1.0.0"',  # Wrong variable name
        ]
        
        for invalid_version in invalid_versions:
            version_file = self.src_dir / "__init__.py"
            version_file.write_text(invalid_version, encoding='utf-8')
            
            with pytest.raises(ReleaseError, match="Could not find version"):
                self.release_manager.parse_current_version()
    
    def test_bump_version_major(self):
        """Test major version bumping"""
        self.create_version_file("1.5.3")
        new_version = self.release_manager.bump_version("major")
        assert new_version == (2, 0, 0)
    
    def test_bump_version_minor(self):
        """Test minor version bumping"""
        self.create_version_file("1.5.3")
        new_version = self.release_manager.bump_version("minor")
        assert new_version == (1, 6, 0)
    
    def test_bump_version_patch(self):
        """Test patch version bumping"""
        self.create_version_file("1.5.3")
        new_version = self.release_manager.bump_version("patch")
        assert new_version == (1, 5, 4)
    
    def test_bump_version_invalid_type(self):
        """Test bumping with invalid type"""
        self.create_version_file("1.0.0")
        
        with pytest.raises(ReleaseError, match="Invalid bump type"):
            self.release_manager.bump_version("invalid")
    
    def test_update_version_file(self):
        """Test updating version file with new version"""
        self.create_version_file("1.0.0")
        
        self.release_manager.update_version_file((2, 1, 5))
        
        # Verify file was updated
        content = (self.src_dir / "__init__.py").read_text(encoding='utf-8')
        assert '__version__ = "2.1.5"' in content
        assert '__author__ = "Test Author"' in content  # Other content preserved
    
    def test_update_version_file_no_match(self):
        """Test updating version file when pattern doesn't match"""
        version_file = self.src_dir / "__init__.py"
        version_file.write_text("# No version here", encoding='utf-8')
        
        with pytest.raises(ReleaseError, match="Version replacement failed"):
            self.release_manager.update_version_file((1, 0, 0))


class TestGitOperations:
    """Test git-related functionality with mocking"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp(prefix=f"git_test_{method.__name__}_"))
        self.release_manager = ReleaseManager(str(self.test_dir))
    
    def teardown_method(self, method):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    @patch('make_release.subprocess.run')
    def test_run_git_command_success(self, mock_run):
        """Test successful git command execution"""
        mock_run.return_value = MagicMock(stdout="output", stderr="", returncode=0)
        
        result = self.release_manager._run_git_command(["status"])
        
        assert result == "output"
        mock_run.assert_called_once()
    
    @patch('make_release.subprocess.run')
    def test_run_git_command_failure(self, mock_run):
        """Test git command failure handling"""
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(1, ["git", "invalid-command"], stderr="Command failed")
        
        with pytest.raises(ReleaseError, match="Git command failed"):
            self.release_manager._run_git_command(["invalid-command"])
    
    @patch('make_release.subprocess.run')
    def test_get_last_version_tag(self, mock_run):
        """Test getting last version tag"""
        mock_run.return_value = MagicMock(stdout="v2.1.0\nv2.0.0\nv1.0.0\n", stderr="", returncode=0)
        
        last_tag = self.release_manager.get_last_version_tag()
        assert last_tag == "v2.1.0"
    
    @patch('make_release.subprocess.run')
    def test_get_last_version_tag_no_tags(self, mock_run):
        """Test getting last version tag when no tags exist"""
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        
        last_tag = self.release_manager.get_last_version_tag()
        assert last_tag is None
    
    @patch('make_release.subprocess.run')
    def test_get_commits_since_tag(self, mock_run):
        """Test getting commits since a specific tag"""
        mock_run.return_value = MagicMock(
            stdout="fix: bug in template\nfeat: add new feature\ndocs: update README\n",
            stderr="", returncode=0
        )
        
        commits = self.release_manager.get_commits_since_tag("v1.0.0")
        
        expected_commits = [
            "fix: bug in template",
            "feat: add new feature", 
            "docs: update README"
        ]
        assert commits == expected_commits
    
    @patch('make_release.subprocess.run')
    def test_get_commits_since_tag_no_commits(self, mock_run):
        """Test getting commits when no commits exist"""
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        
        commits = self.release_manager.get_commits_since_tag("v1.0.0")
        assert commits == []


class TestCommitCategorization:
    """Test commit message categorization"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.release_manager = ReleaseManager()
    
    def test_categorize_commits_added(self):
        """Test categorization of 'added' commits"""
        commits = [
            "feat: add new feature",
            "add new component",
            "new: user authentication",
            "Add support for multiple formats"
        ]
        
        categorized = self.release_manager.categorize_commits(commits)
        
        assert len(categorized["added"]) == 4
        for commit in commits:
            assert commit in categorized["added"]
    
    def test_categorize_commits_fixed(self):
        """Test categorization of 'fixed' commits"""
        commits = [
            "fix: resolve template bug", 
            "bug: fix memory leak",
            "Fix issue with PDF generation",
            "fix template rendering"
        ]
        
        categorized = self.release_manager.categorize_commits(commits)
        
        assert len(categorized["fixed"]) == 4
        for commit in commits:
            assert commit in categorized["fixed"]
    
    def test_categorize_commits_docs(self):
        """Test categorization of documentation commits"""
        commits = [
            "documentation: improve README"
        ]
        
        categorized = self.release_manager.categorize_commits(commits)
        
        assert len(categorized["docs"]) == 1
        assert commits[0] in categorized["docs"]
    
    def test_categorize_commits_multiple_categories(self):
        """Test categorization with commits from multiple categories"""
        commits = [
            "feat: add new feature",
            "fix: resolve bug",
            "documentation: improve README",
            "refactor: improve code structure"
        ]
        
        categorized = self.release_manager.categorize_commits(commits)
        
        assert len(categorized["added"]) == 1
        assert len(categorized["fixed"]) == 1
        assert len(categorized["docs"]) == 1
        assert len(categorized["refactor"]) == 1
    
    def test_categorize_commits_other(self):
        """Test categorization of uncategorized commits"""
        commits = [
            "random commit message",
            "misc changes"
        ]
        
        categorized = self.release_manager.categorize_commits(commits)
        
        assert len(categorized["other"]) == 2
        for commit in commits:
            assert commit in categorized["other"]


class TestChangelogGeneration:
    """Test changelog generation functionality"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp(prefix=f"changelog_test_{method.__name__}_"))
        self.release_manager = ReleaseManager(str(self.test_dir))
    
    def teardown_method(self, method):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_generate_changelog_entry(self):
        """Test generating changelog entry"""
        categorized_commits = {
            "added": ["feat: add new feature", "add user authentication"],
            "fixed": ["fix: resolve template bug"],
            "changed": ["update API endpoints"],
            "docs": ["docs: update README"],
            "other": ["misc cleanup"]
        }
        
        entry = self.release_manager.generate_changelog_entry((2, 1, 0), categorized_commits)
        
        # Verify entry structure
        assert "## [2.1.0]" in entry
        assert "### Added" in entry
        assert "### Fixed" in entry
        assert "### Changed" in entry
        assert "### Documentation" in entry
        assert "### Other" in entry
        
        # Verify commits are included
        assert "feat: add new feature" in entry
        assert "fix: resolve template bug" in entry
        assert "update API endpoints" in entry
        assert "docs: update README" in entry
        assert "misc cleanup" in entry
    
    def test_generate_changelog_entry_empty_sections(self):
        """Test generating changelog entry with empty sections"""
        categorized_commits = {
            "added": ["feat: add feature"],
            "fixed": [],
            "changed": [],
            "docs": [],
            "other": []
        }
        
        entry = self.release_manager.generate_changelog_entry((1, 0, 1), categorized_commits)
        
        # Should only include sections with commits
        assert "### Added" in entry
        assert "### Fixed" not in entry
        assert "### Changed" not in entry
        assert "feat: add feature" in entry
    
    def test_update_changelog_new_file(self):
        """Test creating new changelog file"""
        entry = """## [1.0.1] - 2025-01-01

### Fixed
- fix: resolve bug

"""
        
        self.release_manager.update_changelog(entry)
        
        # Verify file was created
        assert self.release_manager.changelog_file.exists()
        
        content = self.release_manager.changelog_file.read_text(encoding='utf-8')
        assert "# Changelog" in content
        assert "Keep a Changelog" in content
        assert "## [1.0.1] - 2025-01-01" in content
        assert "fix: resolve bug" in content
    
    def test_update_changelog_existing_file(self):
        """Test updating existing changelog file"""
        # Create existing changelog
        existing_content = """# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.0.0] - 2024-01-01

### Added
- Initial release
"""
        
        self.release_manager.changelog_file.write_text(existing_content, encoding='utf-8')
        
        # Add new entry
        new_entry = """## [1.0.1] - 2025-01-01

### Fixed
- fix: resolve bug

"""
        
        self.release_manager.update_changelog(new_entry)
        
        # Verify file was updated
        content = self.release_manager.changelog_file.read_text(encoding='utf-8')
        assert "## [1.0.1] - 2025-01-01" in content
        assert "## [1.0.0] - 2024-01-01" in content
        assert "fix: resolve bug" in content
        assert "Initial release" in content


class TestPrerequisiteValidation:
    """Test prerequisite validation functionality"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp(prefix=f"prereq_test_{method.__name__}_"))
        self.release_manager = ReleaseManager(str(self.test_dir))
    
    def teardown_method(self, method):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    @patch('make_release.ReleaseManager._run_git_command')
    def test_validate_prerequisites_not_git_repo(self, mock_git):
        """Test validation when not in a git repository"""
        mock_git.return_value = ""
        
        with pytest.raises(ReleaseError, match="Not in a git repository"):
            self.release_manager.validate_prerequisites()
    
    @patch('make_release.ReleaseManager._run_git_command')
    def test_validate_prerequisites_dirty_working_dir(self, mock_git):
        """Test validation with dirty working directory"""
        mock_git.side_effect = [
            ".git",  # rev-parse --git-dir
            "M  modified_file.py\n?? untracked_file.py"  # status --porcelain
        ]
        
        with pytest.raises(ReleaseError, match="Working directory is not clean"):
            self.release_manager.validate_prerequisites()
    
    @patch('make_release.ReleaseManager._run_git_command')
    def test_validate_prerequisites_version_file_missing(self, mock_git):
        """Test validation when version file is missing"""
        mock_git.side_effect = [
            ".git",  # rev-parse --git-dir
            ""  # status --porcelain (clean)
        ]
        
        with pytest.raises(ReleaseError, match="Version file not found"):
            self.release_manager.validate_prerequisites()
    
    @patch('make_release.ReleaseManager._run_git_command')
    def test_validate_prerequisites_success(self, mock_git):
        """Test successful prerequisite validation"""
        mock_git.side_effect = [
            ".git",  # rev-parse --git-dir
            ""  # status --porcelain (clean)
        ]
        
        # Create version file
        src_dir = self.test_dir / "src"
        src_dir.mkdir(parents=True)
        version_file = src_dir / "__init__.py"
        version_file.write_text('__version__ = "1.0.0"', encoding='utf-8')
        
        # Should not raise any exception
        self.release_manager.validate_prerequisites()


class TestDryRunMode:
    """Test dry run functionality"""
    
    def setup_method(self, method):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp(prefix=f"dryrun_test_{method.__name__}_"))
        self.src_dir = self.test_dir / "src"
        self.src_dir.mkdir(parents=True)
        
        # Create version file
        version_file = self.src_dir / "__init__.py"
        version_file.write_text('__version__ = "1.0.0"', encoding='utf-8')
        
        self.release_manager = ReleaseManager(str(self.test_dir))
    
    def teardown_method(self, method):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_perform_release_dry_run(self):
        """Test performing release in dry run mode"""
        # Should not raise any exceptions and not modify files
        original_content = (self.src_dir / "__init__.py").read_text()
        
        self.release_manager.perform_release("patch", dry_run=True)
        
        # Verify no files were modified
        assert (self.src_dir / "__init__.py").read_text() == original_content
        assert not self.release_manager.changelog_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])