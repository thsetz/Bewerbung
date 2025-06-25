# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a German job application (Bewerbung) generation system that creates personalized application documents based on profiles and job descriptions.

## Common Commands

Build/test/lint commands will be defined during this development session.

## Directory Structure

- `profil/` - Contains profile documents (PDFs) following naming pattern `YYYYMMDD_*.pdf`
- `Stellenbeschreibung/` - Contains job descriptions following pattern `YYYYMMDD_*.txt` 
- `Ausgabe/` - Output directory where generated applications are created

## Application Generation Process

The system follows a 7-step process:

0. **AI Cache Clearing**: Clears existing AI content cache (`.cache/ai_content_cache.json`) to ensure fresh content generation
1. **Profile Reading**: Reads the newest profile file from `profil/` directory based on date pattern
2. **Job Description Reading**: Reads the newest job description from `Stellenbeschreibung/` directory  
3. **Output Directory Creation**: Creates output directory using pattern `{job_date}_{job_name}-{profile_date}_{profile_name}`
4. **Document Generation**: Creates application documents (cover letter, CV, attachments) using multi-provider AI with fresh, non-cached content
5. **PDF Directory Creation**: Creates `pdf/` subdirectory in output directory
6. **PDF Conversion**: Converts generated documents to PDF format and places them in `pdf/` subdirectory

## File Naming Conventions

- Profile files: `YYYYMMDD_*.pdf` (newest by date is selected)
- Job description files: `YYYYMMDD_*.txt` (newest by date is selected)
- Output directories: `{job_date}_{job_identifier}-{profile_date}_{profile_identifier}`

## Key Architecture Notes

This is a document processing system driven by file naming patterns and automatic selection of the most recent documents by date prefix.

## AI Provider Integration

- **Multi-Provider Support**: Claude API, Ollama/Llama local models, and sample content fallback
- **Intelligent Fallback**: Primary provider order: Llama → Claude → Sample
- **Directory-Only Output**: Each AI provider generates content in its own subdirectory
- **Cache Management**: Automatic AI cache clearing for fresh content generation

## Performance Requirements

- Complete document generation within 30 seconds for 95% of applications
- Support processing of 100+ applications per day
- AI content generation within 10 seconds per section
- PDF conversion within 5 seconds per application package