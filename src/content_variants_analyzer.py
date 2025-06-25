#!/usr/bin/env python3
"""
Content Variants Analyzer - Analyzes AI-generated content across different client/model combinations
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class ContentVariant:
    """Represents a content variant from a specific AI client/model"""
    client_model: str
    ai_provider: str
    ai_model: str
    content: str
    char_count: int
    word_count: int
    preview: str
    
    @classmethod
    def from_content(cls, client_model: str, ai_provider: str, ai_model: str, content: str) -> 'ContentVariant':
        """Create ContentVariant from raw content"""
        char_count = len(content.strip())
        word_count = len(content.strip().split())
        preview = content.strip()[:50] + "..." if len(content.strip()) > 50 else content.strip()
        
        return cls(
            client_model=client_model,
            ai_provider=ai_provider,
            ai_model=ai_model,
            content=content.strip(),
            char_count=char_count,
            word_count=word_count,
            preview=preview
        )

class ContentVariantsAnalyzer:
    """Analyzes content variations across different AI client/model combinations"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.ausgabe_dir = self.base_dir / "Ausgabe"
        
        # AI content variables to analyze
        self.ai_variables = [
            "einstiegstext",
            "fachliche_passung", 
            "motivationstext",
            "mehrwert",
            "abschlusstext"
        ]
    
    def find_output_directories(self) -> List[Path]:
        """Find all application output directories"""
        output_dirs = []
        
        if not self.ausgabe_dir.exists():
            return output_dirs
            
        for item in self.ausgabe_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                output_dirs.append(item)
                
        return sorted(output_dirs)
    
    def find_client_model_directories(self, output_dir: Path) -> List[Path]:
        """Find all client-model subdirectories in an output directory"""
        client_dirs = []
        
        for item in output_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Check if it looks like a client-model directory
                if ('_' in item.name or item.name == 'sample_content') and item.name not in ['pdf']:
                    client_dirs.append(item)
                    
        return sorted(client_dirs)
    
    def extract_metadata(self, client_dir: Path) -> Tuple[str, str]:
        """Extract AI provider and model from metadata"""
        metadata_file = client_dir / "generation_info.json"
        
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    
                gen_info = metadata.get('generation_info', {})
                provider = gen_info.get('ai_provider', 'unknown')
                model = gen_info.get('ai_model', 'unknown')
                
                return provider, model
            except (json.JSONDecodeError, KeyError):
                pass
        
        # Fallback: extract from directory name
        dir_name = client_dir.name
        if 'claude' in dir_name:
            return 'claude', dir_name.replace('claude_', '')
        elif 'llama' in dir_name:
            return 'llama', dir_name.replace('llama_', '')
        elif dir_name == 'sample_content':
            return 'sample', 'content'
        else:
            return 'unknown', 'unknown'
    
    def extract_ai_content(self, client_dir: Path) -> Dict[str, str]:
        """Extract AI-generated content from rendered documents"""
        content = {}
        anschreiben_file = client_dir / "anschreiben.md"
        
        if not anschreiben_file.exists():
            return content
            
        try:
            with open(anschreiben_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Extract content sections based on markdown structure
            content['einstiegstext'] = self._extract_introduction(text)
            content['fachliche_passung'] = self._extract_qualifications(text)
            content['motivationstext'] = self._extract_motivation(text)
            content['mehrwert'] = self._extract_value_proposition(text)
            content['abschlusstext'] = self._extract_closing(text)
            
        except Exception as e:
            print(f"⚠️  Error reading {anschreiben_file}: {e}")
            
        return content
    
    def _extract_introduction(self, text: str) -> str:
        """Extract the introduction paragraph"""
        # Look for content after "Sehr geehrte Damen und Herren," and before "## Meine Qualifikationen"
        pattern = r"Sehr geehrte Damen und Herren,\s*\n\n(.*?)\n\n## Meine Qualifikationen"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def _extract_qualifications(self, text: str) -> str:
        """Extract the qualifications section"""
        pattern = r"## Meine Qualifikationen\s*\n\n(.*?)\n\n## Motivation"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def _extract_motivation(self, text: str) -> str:
        """Extract the motivation section"""
        pattern = r"## Motivation\s*\n\n(.*?)\n\n## Mehrwert"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def _extract_value_proposition(self, text: str) -> str:
        """Extract the value proposition section"""
        pattern = r"## Mehrwert für Ihr Unternehmen\s*\n\n(.*?)\n\n(?:Ich freue mich|Mit freundlichen Grüßen)"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def _extract_closing(self, text: str) -> str:
        """Extract the closing paragraph"""
        pattern = r"(Ich freue mich.*?)\n\nMit freundlichen Grüßen"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def analyze_variants(self) -> Dict[str, List[ContentVariant]]:
        """Analyze all content variants and return organized results"""
        variants = defaultdict(list)
        
        output_dirs = self.find_output_directories()
        
        for output_dir in output_dirs:
            client_dirs = self.find_client_model_directories(output_dir)
            
            for client_dir in client_dirs:
                client_model = client_dir.name
                provider, model = self.extract_metadata(client_dir)
                ai_content = self.extract_ai_content(client_dir)
                
                # Create variants for each AI variable
                for var_name in self.ai_variables:
                    if var_name in ai_content and ai_content[var_name]:
                        variant = ContentVariant.from_content(
                            client_model=client_model,
                            ai_provider=provider,
                            ai_model=model,
                            content=ai_content[var_name]
                        )
                        variants[var_name].append(variant)
        
        return dict(variants)
    
    def format_table_row(self, variant: ContentVariant, col_widths: Dict[str, int]) -> str:
        """Format a table row for a content variant"""
        client = variant.client_model[:col_widths['client']-1] + "…" if len(variant.client_model) > col_widths['client'] else variant.client_model
        chars = str(variant.char_count)
        words = str(variant.word_count)
        preview = variant.preview[:col_widths['preview']-1] + "…" if len(variant.preview) > col_widths['preview'] else variant.preview
        
        return f"│ {client:<{col_widths['client']}} │ {chars:>{col_widths['chars']}} │ {words:>{col_widths['words']}} │ {preview:<{col_widths['preview']}} │"
    
    def format_table_separator(self, col_widths: Dict[str, int], style: str = "middle") -> str:
        """Format table separator line"""
        if style == "top":
            return f"┌─{'─' * col_widths['client']}─┬─{'─' * col_widths['chars']}─┬─{'─' * col_widths['words']}─┬─{'─' * col_widths['preview']}─┐"
        elif style == "bottom":
            return f"└─{'─' * col_widths['client']}─┴─{'─' * col_widths['chars']}─┴─{'─' * col_widths['words']}─┴─{'─' * col_widths['preview']}─┘"
        else:  # middle
            return f"├─{'─' * col_widths['client']}─┼─{'─' * col_widths['chars']}─┼─{'─' * col_widths['words']}─┼─{'─' * col_widths['preview']}─┤"
    
    def display_variants(self, variants: Dict[str, List[ContentVariant]]):
        """Display variants in a formatted table"""
        if not variants:
            print("🔍 No content variants found.")
            return
        
        print("🔍 AI Content Variants Analysis")
        print("═" * 50)
        print()
        
        # Count unique client/model combinations
        all_clients = set()
        provider_mapping = {}
        for var_variants in variants.values():
            for variant in var_variants:
                all_clients.add(variant.client_model)
                provider_mapping[variant.client_model] = (variant.ai_provider, variant.ai_model)
        
        print(f"📊 Found {len(all_clients)} client/model combinations:")
        for client in sorted(all_clients):
            provider, model = provider_mapping.get(client, ("unknown", "unknown"))
            print(f"   - {client} ({provider}/{model})")
        print()
        
        # Show content differences summary
        if len(all_clients) > 1:
            print("🔄 Content Variation Summary:")
            for var_name, var_variants in variants.items():
                if len(var_variants) > 1:
                    char_counts = [v.char_count for v in var_variants]
                    variation = max(char_counts) - min(char_counts)
                    variation_pct = int((variation / max(char_counts)) * 100) if max(char_counts) > 0 else 0
                    print(f"   - {var_name}: {variation_pct}% variation ({variation} chars difference)")
            print()
        
        # Display each content variable
        for var_name, var_variants in variants.items():
            if not var_variants:
                continue
                
            print(f"📝 Content Variable: {var_name}")
            
            # Calculate column widths
            col_widths = {
                'client': max(15, max(len(v.client_model) for v in var_variants) + 2),
                'chars': 10,
                'words': 7,
                'preview': 50
            }
            
            # Table header
            print(self.format_table_separator(col_widths, "top"))
            print(f"│ {'Client/Model':<{col_widths['client']}} │ {'Characters':>{col_widths['chars']}} │ {'Words':>{col_widths['words']}} │ {'Preview':<{col_widths['preview']}} │")
            print(self.format_table_separator(col_widths, "middle"))
            
            # Table rows
            for variant in sorted(var_variants, key=lambda x: x.client_model):
                print(self.format_table_row(variant, col_widths))
            
            print(self.format_table_separator(col_widths, "bottom"))
            print()
        
        # Summary statistics
        print("📈 Summary Statistics:")
        for var_name, var_variants in variants.items():
            if var_variants:
                char_counts = [v.char_count for v in var_variants]
                word_counts = [v.word_count for v in var_variants]
                
                print(f"   {var_name}:")
                print(f"     - Character range: {min(char_counts)}-{max(char_counts)} (avg: {sum(char_counts)//len(char_counts)})")
                print(f"     - Word range: {min(word_counts)}-{max(word_counts)} (avg: {sum(word_counts)//len(word_counts)})")
                print(f"     - Variants: {len(var_variants)}")
        print()

def main():
    """Main entry point"""
    import sys
    
    show_content = "--content" in sys.argv
    
    analyzer = ContentVariantsAnalyzer()
    variants = analyzer.analyze_variants()
    analyzer.display_variants(variants)
    
    # Show detailed content if requested
    if show_content and variants:
        print("📄 Detailed Content Comparison:")
        print("═" * 50)
        
        for var_name, var_variants in variants.items():
            if len(var_variants) > 1:
                print(f"\n🔍 {var_name.upper()}:")
                print("-" * 40)
                
                for i, variant in enumerate(sorted(var_variants, key=lambda x: x.client_model)):
                    print(f"\n[{variant.client_model}] ({variant.char_count} chars, {variant.word_count} words)")
                    print(f"{variant.content}")
                    
                    if i < len(var_variants) - 1:
                        print("\n" + "·" * 80)

if __name__ == "__main__":
    main()