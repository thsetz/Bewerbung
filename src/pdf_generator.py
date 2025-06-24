#!/usr/bin/env python3
"""
PDF Generator - Converts markdown templates to professional PDF documents
"""

from pathlib import Path
from typing import Optional, Dict, Any
import markdown
import tempfile
import os

# WeasyPrint imports with error handling
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError as e:
    print(f"WeasyPrint not available: {e}")
    WEASYPRINT_AVAILABLE = False
    # Create dummy classes for testing
    class HTML:
        def __init__(self, *args, **kwargs):
            pass
        def write_pdf(self, *args, **kwargs):
            raise RuntimeError("WeasyPrint not available")
    
    class CSS:
        def __init__(self, *args, **kwargs):
            pass


class PDFGenerator:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.css_dir = self.base_dir / "Ausgabe" / "css"
        self.css_file = self.css_dir / "bewerbung.css"
        
        # Markdown extensions for better formatting
        self.md_extensions = [
            'markdown.extensions.extra',      # Tables, footnotes, etc.
            'markdown.extensions.nl2br',      # Newline to <br>
            'markdown.extensions.sane_lists', # Better list handling
        ]
    
    def markdown_to_html(self, markdown_content: str, title: str = "Bewerbungsdokument") -> str:
        """
        Convert markdown content to HTML with professional styling
        """
        # Convert markdown to HTML
        md = markdown.Markdown(extensions=self.md_extensions)
        html_content = md.convert(markdown_content)
        
        # Wrap in complete HTML document
        html_template = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{self.get_css_content()}
    </style>
</head>
<body>
    <div class="document">
{html_content}
    </div>
</body>
</html>"""
        
        return html_template
    
    def get_css_content(self) -> str:
        """
        Get CSS content for styling
        """
        if self.css_file.exists():
            return self.css_file.read_text(encoding='utf-8')
        else:
            # Fallback basic CSS if file doesn't exist
            return """
            body { font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.4; }
            h1 { font-size: 18pt; color: #2c3e50; border-bottom: 2pt solid #3498db; }
            h2 { font-size: 14pt; color: #2c3e50; border-bottom: 1pt solid #bdc3c7; }
            """
    
    def html_to_pdf(self, html_content: str, output_path: Path) -> None:
        """
        Convert HTML content to PDF using WeasyPrint
        """
        if not WEASYPRINT_AVAILABLE:
            raise RuntimeError("WeasyPrint is not available. Please install system dependencies first.")
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Create HTML object from string
            html_doc = HTML(string=html_content, base_url=str(self.base_dir))
            
            # Generate PDF
            html_doc.write_pdf(str(output_path))
            print(f"PDF generated successfully: {output_path}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate PDF: {str(e)}")
    
    def markdown_to_pdf(self, markdown_content: str, output_path: Path, title: str = "Bewerbungsdokument") -> None:
        """
        Complete pipeline: Markdown → HTML → PDF
        """
        print(f"Converting markdown to PDF: {output_path}")
        
        # Step 1: Markdown to HTML
        html_content = self.markdown_to_html(markdown_content, title)
        
        # Step 2: HTML to PDF
        self.html_to_pdf(html_content, output_path)
    
    def save_html_preview(self, html_content: str, output_path: Path) -> None:
        """
        Save HTML for preview/debugging purposes
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content, encoding='utf-8')
        print(f"HTML preview saved: {output_path}")
    
    def generate_document_set(self, markdown_files: Dict[str, str], output_dir: Path, 
                            save_html: bool = False) -> Dict[str, Path]:
        """
        Generate a complete set of PDF documents from markdown content
        
        Args:
            markdown_files: Dict with filename -> markdown content
            output_dir: Directory to save PDFs
            save_html: Whether to also save HTML previews
            
        Returns:
            Dict with filename -> generated PDF path
        """
        generated_files = {}
        
        for filename, markdown_content in markdown_files.items():
            # Generate PDF filename
            pdf_filename = filename.replace('.md', '.pdf')
            pdf_path = output_dir / pdf_filename
            
            # Generate title from filename
            title = filename.replace('.md', '').replace('_', ' ').title()
            
            try:
                # Generate PDF
                self.markdown_to_pdf(markdown_content, pdf_path, title)
                generated_files[filename] = pdf_path
                
                # Optionally save HTML preview
                if save_html:
                    html_content = self.markdown_to_html(markdown_content, title)
                    html_path = output_dir / filename.replace('.md', '.html')
                    self.save_html_preview(html_content, html_path)
                    
            except Exception as e:
                print(f"Error generating PDF for {filename}: {str(e)}")
                continue
        
        return generated_files
    
    def validate_dependencies(self) -> Dict[str, bool]:
        """
        Check if all required dependencies are available
        """
        validation = {
            'markdown': False,
            'weasyprint': False,
            'css_file': False
        }
        
        try:
            import markdown
            validation['markdown'] = True
        except ImportError:
            pass
        
        validation['weasyprint'] = WEASYPRINT_AVAILABLE
        validation['css_file'] = self.css_file.exists()
        
        return validation
    
    def get_pdf_info(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Get information about generated PDF
        """
        if not pdf_path.exists():
            return {'exists': False}
        
        stat = pdf_path.stat()
        return {
            'exists': True,
            'size_bytes': stat.st_size,
            'size_kb': round(stat.st_size / 1024, 1),
            'modified': stat.st_mtime,
            'path': str(pdf_path)
        }