#!/usr/bin/env python3
"""
Regeneration Tester - Validates that regeneration scripts produce equivalent results
"""

import os
import sys
import json
import shutil
import tempfile
import subprocess
import platform
from pathlib import Path
from typing import Dict, Any, List, Optional, NamedTuple
from datetime import datetime
import difflib
import argparse


class ComparisonResult(NamedTuple):
    """Result of comparing two output directories"""
    passed: bool
    mode: str
    files_compared: int
    files_identical: int
    files_different: int
    structure_match: bool
    content_issues: List[str]
    warnings: List[str]


class TestResult(NamedTuple):
    """Result of a regeneration test"""
    test_name: str
    passed: bool
    execution_time: float
    comparison: ComparisonResult
    error_message: Optional[str]
    script_output: str


class RegenerationTester:
    """Tests regeneration scripts and validates output consistency"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir).resolve()
        self.test_config = self._load_test_config()
        self.test_results: List[TestResult] = []
        
    def _load_test_config(self) -> Dict[str, Any]:
        """Load test configuration"""
        return {
            'timeout': int(os.getenv('TEST_TIMEOUT', '300')),  # 5 minutes
            'compare_mode': os.getenv('TEST_COMPARE_MODE', 'content'),  # strict, content, structure
            'clean_after': os.getenv('TEST_CLEAN_AFTER', 'true').lower() == 'true',
            'ai_variance_threshold': 0.2  # 20% variation allowed for AI content
        }
    
    def test_all_regeneration_scripts(self, target_dir: Optional[Path] = None) -> List[TestResult]:
        """Test all regeneration scripts in the Ausgabe directory"""
        
        ausgabe_dir = self.base_dir / "Ausgabe"
        if not ausgabe_dir.exists():
            print("❌ No Ausgabe directory found")
            return []
        
        # Find all directories with regeneration scripts
        test_targets = []
        
        if target_dir:
            # Test specific directory
            test_targets = [target_dir]
        else:
            # Find all application directories
            for app_dir in ausgabe_dir.iterdir():
                if app_dir.is_dir() and not app_dir.name.startswith('.'):
                    # Look for model-specific subdirectories
                    for model_dir in app_dir.iterdir():
                        if (model_dir.is_dir() and 
                            '_' in model_dir.name and 
                            (model_dir / "regenerate.sh").exists()):
                            test_targets.append(model_dir)
        
        print(f"🧪 Found {len(test_targets)} regeneration scripts to test")
        
        for target in test_targets:
            result = self.test_regeneration_script(target)
            self.test_results.append(result)
            self._print_test_result(result)
        
        return self.test_results
    
    def test_regeneration_script(self, output_dir: Path) -> TestResult:
        """Test a specific regeneration script"""
        
        test_name = f"{output_dir.parent.name}/{output_dir.name}"
        start_time = datetime.now()
        
        print(f"\\n🔄 Testing regeneration script: {test_name}")
        
        try:
            # Create temporary directory for regeneration test
            with tempfile.TemporaryDirectory(prefix="regen_test_") as temp_dir:
                temp_path = Path(temp_dir)
                
                # Copy original output for comparison
                original_backup = temp_path / "original"
                shutil.copytree(output_dir, original_backup)
                
                # Execute regeneration script
                script_output = self._execute_regeneration_script(output_dir)
                
                # Find the regenerated output
                regenerated_dir = self._find_regenerated_output(output_dir)
                
                if not regenerated_dir or not regenerated_dir.exists():
                    return TestResult(
                        test_name=test_name,
                        passed=False,
                        execution_time=(datetime.now() - start_time).total_seconds(),
                        comparison=ComparisonResult(False, "n/a", 0, 0, 0, False, ["Regenerated output not found"], []),
                        error_message="Regenerated output directory not found",
                        script_output=script_output
                    )
                
                # Compare original vs regenerated
                comparison = self.compare_outputs(original_backup, regenerated_dir)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return TestResult(
                    test_name=test_name,
                    passed=comparison.passed,
                    execution_time=execution_time,
                    comparison=comparison,
                    error_message=None,
                    script_output=script_output
                )
                
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return TestResult(
                test_name=test_name,
                passed=False,
                execution_time=execution_time,
                comparison=ComparisonResult(False, "error", 0, 0, 0, False, [str(e)], []),
                error_message=str(e),
                script_output=""
            )
    
    def _execute_regeneration_script(self, output_dir: Path) -> str:
        """Execute the regeneration script and return output"""
        
        # Determine which script to run
        script_path = None
        if platform.system() == "Windows":
            script_path = output_dir / "regenerate.bat"
        else:
            script_path = output_dir / "regenerate.sh"
        
        if not script_path.exists():
            raise FileNotFoundError(f"Regeneration script not found: {script_path}")
        
        print(f"🚀 Executing: {script_path}")
        
        # Change to project root directory
        old_cwd = os.getcwd()
        try:
            os.chdir(self.base_dir)
            
            # Execute script
            if platform.system() == "Windows":
                result = subprocess.run(
                    [str(script_path)],
                    capture_output=True,
                    text=True,
                    timeout=self.test_config['timeout'],
                    shell=True
                )
            else:
                result = subprocess.run(
                    ["/bin/bash", str(script_path)],
                    capture_output=True,
                    text=True,
                    timeout=self.test_config['timeout']
                )
            
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, str(script_path), result.stderr)
            
            return result.stdout
            
        finally:
            os.chdir(old_cwd)
    
    def _find_regenerated_output(self, original_dir: Path) -> Optional[Path]:
        """Find the regenerated output directory"""
        
        # The regenerated output should be in the same location as the original
        # Since we're testing the script, it should regenerate in the same path structure
        
        app_dir = original_dir.parent
        model_folder_name = original_dir.name
        
        # Look for the regenerated model folder
        regenerated_path = app_dir / model_folder_name
        
        return regenerated_path if regenerated_path.exists() else None
    
    def compare_outputs(self, original: Path, regenerated: Path) -> ComparisonResult:
        """Compare two output directories"""
        
        mode = self.test_config['compare_mode']
        files_compared = 0
        files_identical = 0
        files_different = 0
        content_issues = []
        warnings = []
        
        # Check structure first
        original_files = set(f.relative_to(original) for f in original.rglob('*') if f.is_file())
        regenerated_files = set(f.relative_to(regenerated) for f in regenerated.rglob('*') if f.is_file())
        
        structure_match = original_files == regenerated_files
        
        if not structure_match:
            missing_files = original_files - regenerated_files
            extra_files = regenerated_files - original_files
            
            if missing_files:
                content_issues.append(f"Missing files: {', '.join(str(f) for f in missing_files)}")
            if extra_files:
                warnings.append(f"Extra files: {', '.join(str(f) for f in extra_files)}")
        
        # Compare common files
        common_files = original_files & regenerated_files
        
        for file_path in common_files:
            files_compared += 1
            
            original_file = original / file_path
            regenerated_file = regenerated / file_path
            
            if self._compare_file(original_file, regenerated_file, mode):
                files_identical += 1
            else:
                files_different += 1
                
                if mode == "strict":
                    content_issues.append(f"File differs: {file_path}")
                elif mode == "content":
                    # For content mode, check if it's acceptable AI variation
                    if not self._is_acceptable_variation(original_file, regenerated_file):
                        content_issues.append(f"Significant content difference: {file_path}")
                    else:
                        warnings.append(f"Minor AI variation in: {file_path}")
                        files_identical += 1  # Count as identical for AI variance
                        files_different -= 1
        
        # Determine if test passed
        passed = True
        if mode == "strict":
            passed = structure_match and files_different == 0
        elif mode == "content":
            passed = structure_match and len(content_issues) == 0
        elif mode == "structure":
            passed = structure_match
        
        return ComparisonResult(
            passed=passed,
            mode=mode,
            files_compared=files_compared,
            files_identical=files_identical,
            files_different=files_different,
            structure_match=structure_match,
            content_issues=content_issues,
            warnings=warnings
        )
    
    def _compare_file(self, original: Path, regenerated: Path, mode: str) -> bool:
        """Compare two individual files"""
        
        # Skip certain files that are expected to differ
        if original.name in ['generation_info.json', 'generation.log']:
            return True  # These files will naturally differ due to timestamps
        
        try:
            original_content = original.read_text(encoding='utf-8')
            regenerated_content = regenerated.read_text(encoding='utf-8')
            
            if mode == "strict":
                return original_content == regenerated_content
            elif mode == "content":
                return self._compare_content_semantically(original_content, regenerated_content)
            elif mode == "structure":
                return True  # Structure mode only checks file existence
            
        except Exception as e:
            # For binary files or encoding issues, do binary comparison
            try:
                original_bytes = original.read_bytes()
                regenerated_bytes = regenerated.read_bytes()
                return original_bytes == regenerated_bytes
            except:
                return False
        
        return False
    
    def _compare_content_semantically(self, original: str, regenerated: str) -> bool:
        """Compare content semantically, allowing for AI variations"""
        
        # For markdown files, compare structure and key elements
        if self._is_markdown_content(original):
            return self._compare_markdown_content(original, regenerated)
        
        # For other text files, allow small variations
        return self._calculate_similarity(original, regenerated) > 0.8
    
    def _is_markdown_content(self, content: str) -> bool:
        """Check if content appears to be markdown"""
        return '# ' in content or '## ' in content or '**' in content
    
    def _compare_markdown_content(self, original: str, regenerated: str) -> bool:
        """Compare markdown content structure"""
        
        # Extract headers and structure
        original_headers = self._extract_markdown_headers(original)
        regenerated_headers = self._extract_markdown_headers(regenerated)
        
        # Headers should be identical
        if original_headers != regenerated_headers:
            return False
        
        # Check content length similarity (allow 20% variation for AI content)
        length_ratio = len(regenerated) / len(original) if len(original) > 0 else 1
        return 0.8 <= length_ratio <= 1.2
    
    def _extract_markdown_headers(self, content: str) -> List[str]:
        """Extract markdown headers from content"""
        headers = []
        for line in content.split('\\n'):
            line = line.strip()
            if line.startswith('#'):
                headers.append(line)
        return headers
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity ratio"""
        return difflib.SequenceMatcher(None, text1, text2).ratio()
    
    def _is_acceptable_variation(self, original_file: Path, regenerated_file: Path) -> bool:
        """Check if file differences are within acceptable AI variation"""
        
        try:
            original_content = original_file.read_text(encoding='utf-8')
            regenerated_content = regenerated_file.read_text(encoding='utf-8')
            
            # Calculate similarity
            similarity = self._calculate_similarity(original_content, regenerated_content)
            
            # For AI-generated content, allow more variation
            threshold = 1.0 - self.test_config['ai_variance_threshold']
            
            return similarity >= threshold
            
        except:
            return False
    
    def _print_test_result(self, result: TestResult):
        """Print formatted test result"""
        
        status = "✅ PASS" if result.passed else "❌ FAIL"
        print(f"{status} {result.test_name} ({result.execution_time:.1f}s)")
        
        comp = result.comparison
        print(f"   📊 Files: {comp.files_compared} compared, {comp.files_identical} identical, {comp.files_different} different")
        print(f"   🏗️  Structure: {'✅' if comp.structure_match else '❌'} Match")
        print(f"   📋 Mode: {comp.mode}")
        
        if comp.content_issues:
            for issue in comp.content_issues:
                print(f"   ❌ {issue}")
        
        if comp.warnings:
            for warning in comp.warnings:
                print(f"   ⚠️  {warning}")
        
        if result.error_message:
            print(f"   💥 Error: {result.error_message}")
    
    def generate_test_report(self) -> str:
        """Generate comprehensive test report"""
        
        if not self.test_results:
            return "No test results available"
        
        passed_tests = [r for r in self.test_results if r.passed]
        failed_tests = [r for r in self.test_results if not r.passed]
        
        total_time = sum(r.execution_time for r in self.test_results)
        
        report = f"""# Regeneration Test Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Tests:** {len(self.test_results)}
**Passed:** {len(passed_tests)} ✅
**Failed:** {len(failed_tests)} ❌
**Success Rate:** {len(passed_tests)/len(self.test_results)*100:.1f}%
**Total Time:** {total_time:.1f}s

## Test Configuration
- **Compare Mode:** {self.test_config['compare_mode']}
- **Timeout:** {self.test_config['timeout']}s
- **AI Variance Threshold:** {self.test_config['ai_variance_threshold']*100}%

## Detailed Results

"""
        
        for result in self.test_results:
            status_icon = "✅" if result.passed else "❌"
            report += f"### {status_icon} {result.test_name}\\n"
            report += f"- **Execution Time:** {result.execution_time:.1f}s\\n"
            report += f"- **Files Compared:** {result.comparison.files_compared}\\n"
            report += f"- **Structure Match:** {'✅' if result.comparison.structure_match else '❌'}\\n"
            
            if result.comparison.content_issues:
                report += f"- **Issues:** {', '.join(result.comparison.content_issues)}\\n"
            
            if result.comparison.warnings:
                report += f"- **Warnings:** {', '.join(result.comparison.warnings)}\\n"
            
            report += "\\n"
        
        return report


def main():
    """Main entry point for regeneration testing"""
    
    parser = argparse.ArgumentParser(description="Test regeneration scripts")
    parser.add_argument("--target", help="Specific target directory to test")
    parser.add_argument("--mode", choices=['strict', 'content', 'structure'], 
                       default='content', help="Comparison mode")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout in seconds")
    parser.add_argument("--report", help="Generate report file")
    
    args = parser.parse_args()
    
    # Set test configuration from args
    os.environ['TEST_COMPARE_MODE'] = args.mode
    os.environ['TEST_TIMEOUT'] = str(args.timeout)
    
    # Create tester
    tester = RegenerationTester()
    
    # Run tests
    target_path = Path(args.target) if args.target else None
    results = tester.test_all_regeneration_scripts(target_path)
    
    # Generate summary
    passed = len([r for r in results if r.passed])
    total = len(results)
    
    print(f"\\n🎯 Test Summary: {passed}/{total} tests passed")
    
    # Generate report if requested
    if args.report:
        report_content = tester.generate_test_report()
        Path(args.report).write_text(report_content, encoding='utf-8')
        print(f"📄 Report saved to: {args.report}")
    
    # Exit with appropriate code
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()