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

The system follows a 6-step process:

1. **Profile Reading**: Reads the newest profile file from `profil/` directory based on date pattern
2. **Job Description Reading**: Reads the newest job description from `Stellenbeschreibung/` directory  
3. **Output Directory Creation**: Creates output directory using pattern `{job_date}_{job_name}-{profile_date}_{profile_name}`
4. **Document Generation**: Creates application documents (cover letter, CV, attachments) in output directory
5. **PDF Directory Creation**: Creates `pdf/` subdirectory in output directory
6. **PDF Conversion**: Converts generated documents to PDF format and places them in `pdf/` subdirectory

## File Naming Conventions

- Profile files: `YYYYMMDD_*.pdf` (newest by date is selected)
- Job description files: `YYYYMMDD_*.txt` (newest by date is selected)
- Output directories: `{job_date}_{job_identifier}-{profile_date}_{profile_identifier}`

## Key Architecture Notes

This is a document processing system driven by file naming patterns and automatic selection of the most recent documents by date prefix.