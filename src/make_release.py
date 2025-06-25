#!/usr/bin/env python3
"""
Release Management Script - Automated version bumping and changelog generation

This script handles semantic version bumping and automatic changelog generation
based on git commit history. It follows the Keep a Changelog format and 
integrates with the project's version management system.

Usage:
    python make_release.py major    # 1.0.0 -> 2.0.0
    python make_release.py minor    # 1.0.0 -> 1.1.0  
    python make_release.py patch    # 1.0.0 -> 1.0.1
"""

import os
import re
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional


class ReleaseError(Exception):
    """Custom exception for release-related errors"""
    pass


class ReleaseManager:
    """Manages version releases, changelog generation, and git operations"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.version_file = self.project_root / "src" / "__init__.py"
        self.changelog_file = self.project_root / "CHANGELOG.md"
        
        # Commit categorization patterns
        self.commit_patterns = {
            "added": [r"^feat:", r"^add:", r"^new:", r"add "],
            "changed": [r"^change:", r"^update:", r"^modify:", r"update ", r"modify "],
            "deprecated": [r"^deprecate:", r"deprecate "],
            "removed": [r"^remove:", r"^delete:", r"remove ", r"delete "],
            "fixed": [r"^fix:", r"^bug:", r"fix ", r"bug "],
            "security": [r"^security:", r"^sec:", r"security "],
            "docs": [r"^docs?:", r"^documentation:", r"docs? "],
            "tests": [r"^test:", r"^tests:", r"test "],
            "refactor": [r"^refactor:", r"refactor "],
            "style": [r"^style:", r"^format:", r"style "],
            "chore": [r"^chore:", r"chore "]
        }
    
    def validate_prerequisites(self) -> None:
        """Validate that all prerequisites for a release are met"""
        # Check if we're in a git repository
        if not self._run_git_command(["rev-parse", "--git-dir"], check=False):
            raise ReleaseError("Not in a git repository")
        
        # Check if working directory is clean
        status = self._run_git_command(["status", "--porcelain"])
        if status.strip():
            raise ReleaseError("Working directory is not clean. Commit or stash changes first.")
        
        # Check if version file exists
        if not self.version_file.exists():
            raise ReleaseError(f"Version file not found: {self.version_file}")
        
        # Check if we can write to the project root
        if not os.access(self.project_root, os.W_OK):
            raise ReleaseError(f"Cannot write to project root: {self.project_root}")
    
    def parse_current_version(self) -> Tuple[int, int, int]:
        """Parse the current version from the version file"""
        try:
            with open(self.version_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find version line
            version_match = re.search(r'__version__\s*=\s*["\'](\d+)\.(\d+)\.(\d+)["\']', content)
            if not version_match:
                raise ReleaseError("Could not find version in version file")
            
            major, minor, patch = map(int, version_match.groups())
            return major, minor, patch
            
        except FileNotFoundError:
            raise ReleaseError(f"Version file not found: {self.version_file}")
        except Exception as e:
            raise ReleaseError(f"Error parsing version file: {e}")
    
    def bump_version(self, bump_type: str) -> Tuple[int, int, int]:
        """Bump version according to type (major/minor/patch)"""
        major, minor, patch = self.parse_current_version()
        
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "patch":
            patch += 1
        else:
            raise ReleaseError(f"Invalid bump type: {bump_type}. Use major, minor, or patch.")
        
        return major, minor, patch
    
    def update_version_file(self, new_version: Tuple[int, int, int]) -> None:
        """Update the version in the version file"""
        major, minor, patch = new_version
        new_version_str = f"{major}.{minor}.{patch}"
        
        try:
            with open(self.version_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace version
            new_content = re.sub(
                r'(__version__\s*=\s*["\'])\d+\.\d+\.\d+(["\'])',
                rf'\g<1>{new_version_str}\g<2>',
                content
            )
            
            if new_content == content:
                raise ReleaseError("Version replacement failed - pattern not found")
            
            with open(self.version_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
        except Exception as e:
            raise ReleaseError(f"Error updating version file: {e}")
    
    def get_last_version_tag(self) -> Optional[str]:
        """Get the last version tag from git"""
        try:
            # Get all tags that look like version numbers
            tags = self._run_git_command(["tag", "-l", "v*.*.*", "--sort=-version:refname"])
            if tags.strip():
                return tags.strip().split('\n')[0]
            return None
        except:
            return None
    
    def get_commits_since_tag(self, tag: Optional[str] = None) -> List[str]:
        """Get commit messages since the specified tag (or all if no tag)"""
        try:
            if tag:
                # Get commits since tag
                commits = self._run_git_command(["log", f"{tag}..HEAD", "--pretty=format:%s"])
            else:
                # Get all commits if no previous tag
                commits = self._run_git_command(["log", "--pretty=format:%s"])
            
            if commits.strip():
                return [commit.strip() for commit in commits.strip().split('\n') if commit.strip()]
            return []
            
        except Exception:
            return []
    
    def categorize_commits(self, commits: List[str]) -> Dict[str, List[str]]:
        """Categorize commits based on patterns"""
        categorized = {
            "added": [],
            "changed": [],
            "deprecated": [],
            "removed": [],
            "fixed": [],
            "security": [],
            "docs": [],
            "tests": [],
            "refactor": [],
            "style": [],
            "chore": [],
            "other": []
        }
        
        for commit in commits:
            commit_lower = commit.lower()
            categorized_commit = False
            
            for category, patterns in self.commit_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, commit_lower):
                        categorized[category].append(commit)
                        categorized_commit = True
                        break
                if categorized_commit:
                    break
            
            if not categorized_commit:
                categorized["other"].append(commit)
        
        return categorized
    
    def generate_changelog_entry(self, version: Tuple[int, int, int], 
                                categorized_commits: Dict[str, List[str]]) -> str:
        """Generate a changelog entry for the new version"""
        major, minor, patch = version
        version_str = f"{major}.{minor}.{patch}"
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        entry_lines = [
            f"## [{version_str}] - {date_str}",
            ""
        ]
        
        # Define section order and titles
        sections = [
            ("added", "### Added"),
            ("changed", "### Changed"),
            ("deprecated", "### Deprecated"),
            ("removed", "### Removed"), 
            ("fixed", "### Fixed"),
            ("security", "### Security")
        ]
        
        # Add main sections
        for section_key, section_title in sections:
            commits = categorized_commits.get(section_key, [])
            if commits:
                entry_lines.append(section_title)
                for commit in commits:
                    entry_lines.append(f"- {commit}")
                entry_lines.append("")
        
        # Add development sections if they have commits
        dev_sections = [
            ("docs", "### Documentation"),
            ("tests", "### Tests"),
            ("refactor", "### Refactoring"),
            ("style", "### Style"),
            ("chore", "### Chore")
        ]
        
        for section_key, section_title in dev_sections:
            commits = categorized_commits.get(section_key, [])
            if commits:
                entry_lines.append(section_title)
                for commit in commits:
                    entry_lines.append(f"- {commit}")
                entry_lines.append("")
        
        # Add other commits
        other_commits = categorized_commits.get("other", [])
        if other_commits:
            entry_lines.append("### Other")
            for commit in other_commits:
                entry_lines.append(f"- {commit}")
            entry_lines.append("")
        
        return "\n".join(entry_lines)
    
    def update_changelog(self, new_entry: str) -> None:
        """Update or create the changelog file"""
        try:
            if self.changelog_file.exists():
                with open(self.changelog_file, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
                
                # Find the position after the header to insert new entry
                lines = existing_content.split('\n')
                header_end_index = 0
                
                # Look for the end of the header (usually after "## [Unreleased]" or first "##")
                for i, line in enumerate(lines):
                    if line.startswith("## ") and i > 0:
                        header_end_index = i
                        break
                
                # Insert new entry
                if header_end_index > 0:
                    new_lines = lines[:header_end_index] + new_entry.split('\n') + lines[header_end_index:]
                else:
                    # If no existing entries, add after any header
                    new_lines = lines + new_entry.split('\n')
                
                new_content = '\n'.join(new_lines)
            else:
                # Create new changelog
                header = [
                    "# Changelog",
                    "",
                    "All notable changes to this project will be documented in this file.",
                    "",
                    "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),",
                    "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).",
                    "",
                    "## [Unreleased]",
                    "",
                ]
                
                new_content = '\n'.join(header) + new_entry
            
            with open(self.changelog_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
        except Exception as e:
            raise ReleaseError(f"Error updating changelog: {e}")
    
    def create_git_tag(self, version: Tuple[int, int, int]) -> None:
        """Create a git tag for the new version"""
        major, minor, patch = version
        tag_name = f"v{major}.{minor}.{patch}"
        
        try:
            # Add and commit changes
            self._run_git_command(["add", str(self.version_file)])
            if self.changelog_file.exists():
                self._run_git_command(["add", str(self.changelog_file)])
            
            commit_message = f"Release {major}.{minor}.{patch}"
            self._run_git_command(["commit", "-m", commit_message])
            
            # Create tag
            tag_message = f"Version {major}.{minor}.{patch}"
            self._run_git_command(["tag", "-a", tag_name, "-m", tag_message])
            
            print(f"✅ Created git tag: {tag_name}")
            
        except Exception as e:
            raise ReleaseError(f"Error creating git tag: {e}")
    
    def _run_git_command(self, args: List[str], check: bool = True) -> str:
        """Run a git command and return the output"""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=check
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            if check:
                raise ReleaseError(f"Git command failed: {' '.join(args)}\n{e.stderr}")
            return ""
    
    def perform_release(self, bump_type: str, dry_run: bool = False) -> None:
        """Perform a complete release"""
        print(f"🚀 Starting {bump_type} release...")
        
        if not dry_run:
            # Validate prerequisites
            print("🔍 Validating prerequisites...")
            self.validate_prerequisites()
        
        # Get current version
        current_version = self.parse_current_version()
        current_version_str = f"{current_version[0]}.{current_version[1]}.{current_version[2]}"
        print(f"📋 Current version: {current_version_str}")
        
        # Calculate new version
        new_version = self.bump_version(bump_type)
        new_version_str = f"{new_version[0]}.{new_version[1]}.{new_version[2]}"
        print(f"📈 New version: {new_version_str}")
        
        if dry_run:
            print("🔍 Dry run mode - no changes will be made")
            return
        
        # Get commits for changelog
        last_tag = self.get_last_version_tag()
        commits = self.get_commits_since_tag(last_tag)
        print(f"📝 Found {len(commits)} commits since last release")
        
        if commits:
            # Generate changelog
            categorized_commits = self.categorize_commits(commits)
            changelog_entry = self.generate_changelog_entry(new_version, categorized_commits)
            
            # Update files
            print("📝 Updating version file...")
            self.update_version_file(new_version)
            
            print("📝 Updating changelog...")
            self.update_changelog(changelog_entry)
        else:
            print("⚠️  No commits found - updating version only")
            self.update_version_file(new_version)
        
        # Create git tag
        print("🏷️  Creating git tag...")
        self.create_git_tag(new_version)
        
        print(f"✅ Release {new_version_str} completed successfully!")
        print(f"📁 Updated files: {self.version_file.name}, {self.changelog_file.name}")
        print(f"🏷️  Created tag: v{new_version_str}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Release management script")
    parser.add_argument(
        "bump_type", 
        choices=["major", "minor", "patch"],
        help="Type of version bump to perform"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without making changes"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Path to project root directory"
    )
    
    args = parser.parse_args()
    
    try:
        # Adjust project root if running from src directory
        project_root = Path(args.project_root)
        if project_root.name == "src":
            project_root = project_root.parent
        
        release_manager = ReleaseManager(str(project_root))
        release_manager.perform_release(args.bump_type, args.dry_run)
        
    except ReleaseError as e:
        print(f"❌ Release failed: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Release cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()