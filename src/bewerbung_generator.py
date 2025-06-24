#!/usr/bin/env python3
"""
Bewerbung Generator - Generates German job applications from profiles and job descriptions
"""

import os
import re
from pathlib import Path
from typing import Optional, Tuple, Dict

class BewerbungGenerator:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.profil_dir = self.base_dir / "profil"
        self.stellenbeschreibung_dir = self.base_dir / "Stellenbeschreibung"
        self.ausgabe_dir = self.base_dir / "Ausgabe"
    
    def get_newest_file_by_date_pattern(self, directory: Path, pattern: str = r"(\d{8})_.*") -> Optional[Path]:
        """
        Find the newest file in directory based on YYYYMMDD date pattern
        """
        if not directory.exists():
            print(f"Directory {directory} does not exist")
            return None
            
        files = []
        for file_path in directory.iterdir():
            if file_path.is_file():
                match = re.match(pattern, file_path.name)
                if match:
                    date_str = match.group(1)
                    files.append((date_str, file_path))
        
        if not files:
            print(f"No files matching pattern found in {directory}")
            return None
            
        # Sort by date string (YYYYMMDD format sorts naturally)
        files.sort(key=lambda x: x[0], reverse=True)
        newest_file = files[0][1]
        
        print(f"Found newest file: {newest_file}")
        return newest_file
    
    def read_newest_profile(self) -> Optional[Path]:
        """
        Step 1: Read the newest profile file from profil/ directory
        """
        print("=== Step 1: Reading newest profile ===")
        return self.get_newest_file_by_date_pattern(self.profil_dir, r"(\d{8})_.*\.pdf")
    
    def read_newest_job_description(self) -> Optional[Path]:
        """
        Step 2: Read the newest job description from Stellenbeschreibung/ directory
        """
        print("=== Step 2: Reading newest job description ===")
        return self.get_newest_file_by_date_pattern(self.stellenbeschreibung_dir, r"(\d{8})_.*\.txt")
    
    def extract_file_identifiers(self, profile_file: Path, job_file: Path) -> Tuple[str, str, str, str]:
        """
        Extract date and identifier parts from profile and job filenames
        Returns: (profile_date, profile_id, job_date, job_id)
        """
        # Extract profile parts
        profile_match = re.match(r"(\d{8})_(.*)\.pdf", profile_file.name)
        if not profile_match:
            raise ValueError(f"Invalid profile filename format: {profile_file.name}")
        profile_date, profile_id = profile_match.groups()
        
        # Extract job parts  
        job_match = re.match(r"(\d{8})_(.*)\.txt", job_file.name)
        if not job_match:
            raise ValueError(f"Invalid job filename format: {job_file.name}")
        job_date, job_id = job_match.groups()
        
        return profile_date, profile_id, job_date, job_id
    
    def create_output_directory(self, profile_file: Path, job_file: Path) -> Path:
        """
        Step 3: Create output directory with proper naming pattern
        Pattern: {job_date}_{job_id}-{profile_date}_{profile_id}
        """
        print("=== Step 3: Creating output directory ===")
        
        profile_date, profile_id, job_date, job_id = self.extract_file_identifiers(profile_file, job_file)
        
        # Create output directory name
        output_dir_name = f"{job_date}_{job_id}-{profile_date}_{profile_id}"
        output_path = self.ausgabe_dir / output_dir_name
        
        # Create Ausgabe directory if it doesn't exist
        self.ausgabe_dir.mkdir(exist_ok=True)
        
        # Create output directory
        output_path.mkdir(exist_ok=True)
        
        print(f"Created output directory: {output_path}")
        return output_path
    
    def generate_application_documents(self, output_dir: Path, profile_file: Path, job_file: Path) -> Dict[str, Path]:
        """
        Step 4: Generate application documents (cover letter, CV, attachments) with AI content
        """
        print("=== Step 4: Generating application documents ===")
        
        # Import AI classes locally to avoid import issues
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent))
            from template_manager import TemplateManager
            from claude_api_client import ClaudeAPIClient
        except ImportError as e:
            print(f"Error importing AI modules: {e}")
            print("Falling back to basic document generation")
            return self._generate_basic_documents(output_dir, profile_file, job_file)
        
        # Initialize managers
        template_manager = TemplateManager(str(self.base_dir))
        claude_client = ClaudeAPIClient(str(self.base_dir))
        
        # Read input content
        job_content = job_file.read_text(encoding='utf-8')
        profile_content = f"Profile: {profile_file.name}"  # Placeholder for actual profile content
        
        # Extract company and position info
        if claude_client.is_available():
            company_info = claude_client.extract_company_and_position(job_content)
            company_name = company_info['company_name']
            position_title = company_info['position_title']
        else:
            company_name = "Beispiel Unternehmen GmbH"
            position_title = "Software Engineer"
            company_info = {
                'company_name': company_name,
                'position_title': position_title,
                'adressat_firma': company_name,
                'adressat_strasse': 'Musterstraße 1',
                'adressat_plz_ort': '12345 Musterstadt',
                'adressat_land': 'Deutschland'
            }
        
        print(f"Company: {company_name}, Position: {position_title}")
        
        # Generate AI content for cover letter
        if claude_client.is_available():
            print("Generating AI content...")
            ai_content = claude_client.generate_all_cover_letter_content(
                job_description=job_content,
                profile_content=profile_content,
                company_name=company_name,
                position_title=position_title
            )
        else:
            print("Using sample AI content...")
            from ai_content_generator import generate_sample_ai_content
            ai_content = generate_sample_ai_content()
        
        # Addressee data for cover letter (lowercase for dynamic content)
        adressat_data = {
            'position': position_title,
        }
        
        # Set Adressat and job variables as environment variables (uppercase for template)
        import os
        os.environ['ADRESSAT_FIRMA'] = company_info.get('adressat_firma', company_name)
        os.environ['ADRESSAT_STRASSE'] = company_info.get('adressat_strasse', '')
        os.environ['ADRESSAT_PLZ_ORT'] = company_info.get('adressat_plz_ort', '')
        os.environ['ADRESSAT_LAND'] = company_info.get('adressat_land', 'Deutschland')
        os.environ['STELLE'] = company_info.get('stelle', position_title)
        os.environ['STELLEN_ID'] = company_info.get('stellen_id', '')
        
        print(f"Adressat: {os.environ['ADRESSAT_FIRMA']}")
        print(f"Stelle: {os.environ['STELLE']}")
        print(f"Stellen-ID: {os.environ['STELLEN_ID']}")
        
        # Generate documents
        generated_files = {}
        
        try:
            # Generate cover letter
            print("Rendering cover letter...")
            anschreiben_md = template_manager.render_anschreiben(adressat_data, ai_content)
            anschreiben_path = output_dir / "anschreiben.md"
            template_manager.save_rendered_template(anschreiben_md, anschreiben_path)
            generated_files['anschreiben.md'] = anschreiben_path
            
            # Generate CV
            print("Rendering CV...")
            lebenslauf_md = template_manager.render_lebenslauf()
            lebenslauf_path = output_dir / "lebenslauf.md"
            template_manager.save_rendered_template(lebenslauf_md, lebenslauf_path)
            generated_files['lebenslauf.md'] = lebenslauf_path
            
            # Generate attachments list
            print("Generating attachments list...")
            attachments_content = self._generate_attachments_list(profile_file)
            attachments_path = output_dir / "anlagen.md"
            attachments_path.write_text(attachments_content, encoding='utf-8')
            generated_files['anlagen.md'] = attachments_path
            
            print("✓ Application documents generated successfully")
            return generated_files
            
        except Exception as e:
            print(f"Error generating documents: {e}")
            return self._generate_basic_documents(output_dir, profile_file, job_file)
    
    def _generate_basic_documents(self, output_dir: Path, profile_file: Path, job_file: Path) -> Dict[str, Path]:
        """Fallback method for basic document generation without AI"""
        print("Generating basic documents without AI...")
        
        generated_files = {}
        
        # Basic cover letter
        basic_anschreiben = f"""# Anschreiben

**Max Mustermann**
Musterstraße 123
12345 Berlin

---

Sehr geehrte Damen und Herren,

mit großem Interesse habe ich Ihre Stellenausschreibung gelesen.

Basierend auf der Stellenbeschreibung ({job_file.name}) und meinem Profil ({profile_file.name}) bewerbe ich mich hiermit um die ausgeschriebene Position.

Mit freundlichen Grüßen
Max Mustermann
"""
        
        anschreiben_path = output_dir / "anschreiben.md"
        anschreiben_path.write_text(basic_anschreiben, encoding='utf-8')
        generated_files['anschreiben.md'] = anschreiben_path
        
        # Basic CV
        basic_lebenslauf = f"""# Lebenslauf

**Max Mustermann**

Detaillierte Informationen siehe Profildokument: {profile_file.name}
"""
        
        lebenslauf_path = output_dir / "lebenslauf.md"
        lebenslauf_path.write_text(basic_lebenslauf, encoding='utf-8')
        generated_files['lebenslauf.md'] = lebenslauf_path
        
        # Attachments
        attachments_content = self._generate_attachments_list(profile_file)
        attachments_path = output_dir / "anlagen.md"
        attachments_path.write_text(attachments_content, encoding='utf-8')
        generated_files['anlagen.md'] = attachments_path
        
        return generated_files
    
    def _generate_attachments_list(self, profile_file: Path) -> str:
        """Generate attachments list"""
        return f"""# Anlagen

Die folgenden Dokumente sind dieser Bewerbung beigefügt:

1. Anschreiben
2. Lebenslauf
3. Profildokument: {profile_file.name}
4. Zeugnisse und Zertifikate
5. Referenzen

---

*Hinweis: Das Profildokument enthält detaillierte Informationen zu Qualifikationen und Berufserfahrung.*
"""
    
    def create_pdf_directory(self, output_dir: Path) -> Path:
        """
        Step 5: Create pdf/ subdirectory in output directory
        """
        print("=== Step 5: Creating PDF directory ===")
        
        pdf_dir = output_dir / "pdf"
        pdf_dir.mkdir(exist_ok=True)
        
        print(f"Created PDF directory: {pdf_dir}")
        return pdf_dir
    
    def convert_documents_to_pdf(self, markdown_files: Dict[str, Path], pdf_dir: Path) -> Dict[str, Path]:
        """
        Step 6: Convert documents to PDF format
        """
        print("=== Step 6: Converting documents to PDF ===")
        
        # Import PDF generator locally
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent))
            from pdf_generator import PDFGenerator
        except ImportError as e:
            print(f"Error importing PDF generator: {e}")
            return {}
        
        pdf_generator = PDFGenerator(str(self.base_dir))
        
        # Check if PDF generation is available
        validation = pdf_generator.validate_dependencies()
        if not validation['weasyprint']:
            print("⚠️  WeasyPrint not available - PDF generation skipped")
            print("   Install system dependencies: brew install pango")
            return {}
        
        generated_pdfs = {}
        
        for md_name, md_path in markdown_files.items():
            try:
                # Read markdown content
                markdown_content = md_path.read_text(encoding='utf-8')
                
                # Generate PDF filename
                pdf_name = md_name.replace('.md', '.pdf')
                pdf_path = pdf_dir / pdf_name
                
                # Convert to PDF
                title = md_name.replace('.md', '').replace('_', ' ').title()
                pdf_generator.markdown_to_pdf(markdown_content, pdf_path, title)
                
                generated_pdfs[md_name] = pdf_path
                
                # Also save HTML preview
                html_name = md_name.replace('.md', '.html')
                html_path = pdf_dir / html_name
                html_content = pdf_generator.markdown_to_html(markdown_content, title)
                pdf_generator.save_html_preview(html_content, html_path)
                
            except Exception as e:
                print(f"Error converting {md_name} to PDF: {e}")
                continue
        
        print(f"✓ Converted {len(generated_pdfs)} documents to PDF")
        return generated_pdfs

def main():
    """
    Main orchestration script - executes all 6 steps of the application generation process
    """
    print("🚀 Starting Bewerbung Generator")
    print("=" * 50)
    
    generator = BewerbungGenerator()
    
    try:
        # Step 1: Read newest profile
        profile_file = generator.read_newest_profile()
        if not profile_file:
            print("❌ Error: No profile file found")
            return 1
        
        # Step 2: Read newest job description  
        job_file = generator.read_newest_job_description()
        if not job_file:
            print("❌ Error: No job description file found")
            return 1
            
        # Step 3: Create output directory
        output_dir = generator.create_output_directory(profile_file, job_file)
        
        # Step 4: Generate application documents with AI content
        markdown_files = generator.generate_application_documents(output_dir, profile_file, job_file)
        
        if not markdown_files:
            print("❌ Error: Failed to generate application documents")
            return 1
        
        # Step 5: Create PDF directory
        pdf_dir = generator.create_pdf_directory(output_dir)
        
        # Step 6: Convert documents to PDF
        pdf_files = generator.convert_documents_to_pdf(markdown_files, pdf_dir)
        
        # Summary
        print("\n" + "=" * 50)
        print("✅ Bewerbung generation completed successfully!")
        print(f"\n📁 Output Directory: {output_dir}")
        print(f"📄 Profile: {profile_file.name}")
        print(f"📄 Job Description: {job_file.name}")
        
        print(f"\n📝 Generated Documents:")
        for filename, path in markdown_files.items():
            print(f"   - {filename}")
        
        if pdf_files:
            print(f"\n📄 Generated PDFs:")
            for filename, pdf_path in pdf_files.items():
                size_kb = round(pdf_path.stat().st_size / 1024, 1)
                print(f"   - {pdf_path.name} ({size_kb} KB)")
        else:
            print(f"\n⚠️  No PDFs generated (WeasyPrint not available)")
        
        print(f"\n🎯 Ready for application submission!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        return 1

if __name__ == "__main__":
    exit(main())