#!/usr/bin/env python3
"""
Bewerbung Generator - Generates German job applications from profiles and job descriptions
"""

import os
import re
import json
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
            from ai_client_factory import AIClientFactory
        except ImportError as e:
            print(f"Error importing AI modules: {e}")
            print("Falling back to basic document generation")
            return self._generate_basic_documents(output_dir, profile_file, job_file)
        
        # Initialize managers
        template_manager = TemplateManager(str(self.base_dir))
        ai_factory = AIClientFactory(str(self.base_dir))
        ai_client = ai_factory.create_client()
        
        # Determine output structure
        output_structure = os.getenv("OUTPUT_STRUCTURE", "legacy").lower()
        include_metadata = os.getenv("INCLUDE_GENERATION_METADATA", "false").lower() == "true"
        
        # Create client-model specific output directory if needed
        if output_structure in ["by_model", "both"]:
            client_model_folder = ai_client.get_client_model_folder()
            model_output_dir = output_dir / client_model_folder
            model_output_dir.mkdir(parents=True, exist_ok=True)
            print(f"📁 Using model-specific output: {client_model_folder}")
        else:
            model_output_dir = output_dir
        
        # Read input content
        job_content = job_file.read_text(encoding='utf-8')
        profile_content = f"Profile: {profile_file.name}"  # Placeholder for actual profile content
        
        # Extract company and position info
        if ai_client.is_available():
            company_info = ai_client.extract_company_and_position(job_content)
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
        if ai_client.is_available():
            print("Generating AI content...")
            ai_content = ai_client.generate_all_cover_letter_content(
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
            # Generate documents
            print("Rendering cover letter...")
            anschreiben_md = template_manager.render_anschreiben(adressat_data, ai_content)
            
            print("Rendering CV...")
            lebenslauf_md = template_manager.render_lebenslauf()
            
            print("Generating attachments list...")
            attachments_content = self._generate_attachments_list(profile_file)
            
            # Save to model-specific directory
            self._save_documents_to_directory(
                model_output_dir, 
                anschreiben_md, 
                lebenslauf_md, 
                attachments_content,
                template_manager
            )
            generated_files['model_output_dir'] = model_output_dir
            
            # If "both" structure, also save to legacy location
            if output_structure == "both":
                print("📁 Also saving to legacy structure...")
                self._save_documents_to_directory(
                    output_dir,
                    anschreiben_md,
                    lebenslauf_md, 
                    attachments_content,
                    template_manager
                )
                generated_files['legacy_output_dir'] = output_dir
            
            # Generate metadata if requested
            if include_metadata:
                metadata = self._generate_metadata(ai_client, job_file, profile_file, ai_content)
                metadata_path = model_output_dir / "generation_info.json"
                metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
                print(f"📊 Generated metadata: {metadata_path}")
                generated_files['metadata'] = metadata_path
            
            # Generate documentation if requested
            generate_docs = os.getenv("GENERATE_DOCUMENTATION", "true").lower() == "true"
            if generate_docs:
                try:
                    from documentation_generator import DocumentationGenerator
                    doc_generator = DocumentationGenerator(str(self.base_dir))
                    
                    # Use metadata if available, otherwise create basic metadata
                    doc_metadata = metadata if include_metadata else self._generate_metadata(ai_client, job_file, profile_file, ai_content)
                    
                    docs = doc_generator.generate_documentation(
                        model_output_dir, 
                        doc_metadata, 
                        ai_content, 
                        profile_file, 
                        job_file
                    )
                    
                    generated_files.update(docs)
                    print(f"📚 Generated documentation: README.md, regeneration scripts")
                    
                except ImportError as e:
                    print(f"⚠️  Documentation generation failed: {e}")
                except Exception as e:
                    print(f"⚠️  Error generating documentation: {e}")
            
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
        Step 5: Create pdf/ subdirectory in output directory(ies)
        """
        print("=== Step 5: Creating PDF directory ===")
        
        # Handle new folder structure - check if we have model-specific folders
        output_structure = os.getenv("OUTPUT_STRUCTURE", "legacy").lower()
        
        if output_structure in ["by_model", "both"]:
            # Find model-specific folders and create PDF dirs in each
            pdf_dirs = []
            for item in output_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Check if this looks like a model folder (contains underscores)
                    if '_' in item.name:
                        pdf_dir = item / "pdf"
                        pdf_dir.mkdir(parents=True, exist_ok=True)
                        pdf_dirs.append(pdf_dir)
                        print(f"Created PDF directory: {pdf_dir}")
            
            # Also create legacy PDF dir if "both" structure
            if output_structure == "both":
                legacy_pdf_dir = output_dir / "pdf"
                legacy_pdf_dir.mkdir(parents=True, exist_ok=True)
                pdf_dirs.append(legacy_pdf_dir)
                print(f"Created legacy PDF directory: {legacy_pdf_dir}")
            
            return pdf_dirs[0] if pdf_dirs else output_dir / "pdf"  # Return first one for compatibility
        else:
            # Legacy structure
            pdf_dir = output_dir / "pdf"
            pdf_dir.mkdir(exist_ok=True)
            print(f"Created PDF directory: {pdf_dir}")
            return pdf_dir
    
    def convert_documents_to_pdf(self, markdown_files: Dict[str, Path], pdf_dir: Path) -> Dict[str, Path]:
        """
        Step 6: Convert documents to PDF format in all relevant directories
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
        
        # Determine which directories contain markdown files to convert
        output_structure = os.getenv("OUTPUT_STRUCTURE", "legacy").lower()
        conversion_dirs = []
        
        if output_structure in ["by_model", "both"]:
            # Find all model-specific directories that contain markdown files
            main_output_dir = pdf_dir.parent  # Get back to main output directory
            for item in main_output_dir.iterdir():
                if item.is_dir() and '_' in item.name:  # Model folder
                    md_files = list(item.glob("*.md"))
                    if md_files:
                        pdf_subdir = item / "pdf"
                        pdf_subdir.mkdir(exist_ok=True)
                        conversion_dirs.append((item, pdf_subdir, md_files))
            
            # Also handle legacy dir if "both" structure
            if output_structure == "both":
                legacy_md_files = list(main_output_dir.glob("*.md"))
                if legacy_md_files:
                    legacy_pdf_dir = main_output_dir / "pdf"
                    conversion_dirs.append((main_output_dir, legacy_pdf_dir, legacy_md_files))
        else:
            # Legacy structure - use provided parameters
            md_files = [path for path in markdown_files.values()]
            conversion_dirs.append((pdf_dir.parent, pdf_dir, md_files))
        
        generated_pdfs = {}
        total_converted = 0
        
        for source_dir, target_pdf_dir, md_files in conversion_dirs:
            print(f"Converting files in {source_dir.name}...")
            
            for md_path in md_files:
                try:
                    # Read markdown content
                    markdown_content = md_path.read_text(encoding='utf-8')
                    
                    # Generate PDF filename
                    pdf_name = md_path.name.replace('.md', '.pdf')
                    pdf_path = target_pdf_dir / pdf_name
                    
                    print(f"Converting markdown to PDF: {pdf_path}")
                    
                    # Convert to PDF
                    title = md_path.stem.replace('_', ' ').title()
                    pdf_generator.markdown_to_pdf(markdown_content, pdf_path, title)
                    
                    generated_pdfs[f"{source_dir.name}/{pdf_name}"] = pdf_path
                    total_converted += 1
                    
                    # Also save HTML preview
                    html_name = md_path.name.replace('.md', '.html')
                    html_path = target_pdf_dir / html_name
                    html_content = pdf_generator.markdown_to_html(markdown_content, title)
                    pdf_generator.save_html_preview(html_content, html_path)
                    
                except Exception as e:
                    print(f"Error converting {md_path.name} to PDF: {e}")
                    continue
        
        print(f"✓ Converted {total_converted} documents to PDF")
        return generated_pdfs
    
    def _save_documents_to_directory(self, target_dir: Path, anschreiben_md: str, 
                                   lebenslauf_md: str, attachments_content: str, 
                                   template_manager) -> Dict[str, Path]:
        """Save all documents to a specific directory"""
        generated_files = {}
        
        # Save cover letter
        anschreiben_path = target_dir / "anschreiben.md"
        template_manager.save_rendered_template(anschreiben_md, anschreiben_path)
        generated_files['anschreiben.md'] = anschreiben_path
        
        # Save CV
        lebenslauf_path = target_dir / "lebenslauf.md"
        template_manager.save_rendered_template(lebenslauf_md, lebenslauf_path)
        generated_files['lebenslauf.md'] = lebenslauf_path
        
        # Save attachments
        attachments_path = target_dir / "anlagen.md"
        attachments_path.write_text(attachments_content, encoding='utf-8')
        generated_files['anlagen.md'] = attachments_path
        
        return generated_files
    
    def _generate_metadata(self, ai_client, job_file: Path, profile_file: Path, 
                          ai_content: Dict[str, str]) -> Dict[str, any]:
        """Generate metadata about the content generation process"""
        import time
        from datetime import datetime
        
        metadata = {
            "generation_info": {
                "timestamp": datetime.now().isoformat(),
                "ai_provider": ai_client.get_provider_name(),
                "ai_model": ai_client.get_model_name(),
                "client_folder": ai_client.get_client_model_folder()
            },
            "input_files": {
                "job_description": job_file.name,
                "profile": profile_file.name
            },
            "generated_content": {
                "ai_variables": list(ai_content.keys()),
                "total_ai_variables": len(ai_content)
            },
            "ai_client_stats": ai_client.get_usage_stats()
        }
        
        # Add content lengths for analysis
        for key, content in ai_content.items():
            if isinstance(content, str):
                metadata["generated_content"][f"{key}_length"] = len(content)
                metadata["generated_content"][f"{key}_words"] = len(content.split())
        
        return metadata

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