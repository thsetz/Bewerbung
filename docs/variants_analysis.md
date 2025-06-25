# Content Variants Analysis

> **{{ project }} v{{ version }}** - Content Variants Analysis Documentation

The Bewerbung generator includes a powerful content variants analyzer that compares AI-generated content across different client/model combinations.

:::{note}
**Version:** {{ version }} | **Documentation for:** {{ project }}
:::

## Overview

The variants analyzer examines all generated job applications and provides:
- Content comparison across different AI providers (Claude, Llama, Sample)
- Statistical analysis of text variations
- Detailed content breakdowns by AI variable
- Variation percentage calculations

## Usage

### Basic Analysis
```bash
make variants
```

Displays:
- Summary of found client/model combinations
- Content variation percentages by AI variable
- Formatted tables with character/word counts
- Statistical summaries

### Detailed Analysis
```bash
make variants-detailed
```

Includes everything from basic analysis plus:
- Full text content for each AI variable
- Side-by-side content comparisons
- Detailed character and word counts

## Features

### AI Variables Analyzed
The analyzer examines these AI-generated content sections:
- `einstiegstext` - Opening paragraph
- `fachliche_passung` - Technical qualifications  
- `motivationstext` - Motivation section
- `mehrwert` - Value proposition
- `abschlusstext` - Professional closing

### Content Detection
The analyzer automatically:
- Scans all output directories in `Ausgabe/`
- Identifies client-model specific subdirectories
- Extracts metadata from `generation_info.json`
- Parses AI content from rendered markdown files

### Provider Identification
For each content variant, the analyzer shows:
- Client/model folder name (e.g., `claude_sonnet-3-5`)
- AI provider name (e.g., `claude`)
- Model identifier (e.g., `sonnet-3-5`)

### Statistics
The analyzer calculates:
- Character count and word count for each content piece
- Variation percentages between different providers
- Content length ranges and averages
- Number of variants per AI variable

## Example Output

```
🔍 AI Content Variants Analysis
══════════════════════════════════════════════════

📊 Found 3 client/model combinations:
   - claude_sonnet-3-5 (claude/sonnet-3-5)
   - llama_3-2-latest (llama/3-2-latest)
   - sample_content (sample/content)

🔄 Content Variation Summary:
   - einstiegstext: 56% variation (365 chars difference)
   - fachliche_passung: 63% variation (483 chars difference)
   - motivationstext: 53% variation (324 chars difference)
   - mehrwert: 32% variation (203 chars difference)
   - abschlusstext: 18% variation (56 chars difference)

📝 Content Variable: einstiegstext
┌─────────────────────┬────────────┬─────────┬──────────────────────┐
│ Client/Model        │ Characters │   Words │ Preview              │
├─────────────────────┼────────────┼─────────┼──────────────────────┤
│ claude_sonnet-3-5   │        491 │      63 │ Mit großem Interesse…│
│ llama_3-2-latest    │        649 │      84 │ Ich bin sehr interes…│
│ sample_content      │        284 │      35 │ mit großem Interesse…│
└─────────────────────┴────────────┴─────────┴──────────────────────┘
```

## Use Cases

### Content Quality Assessment
- Compare AI provider output quality
- Identify which providers generate more detailed content
- Assess content variation for consistency evaluation

### Provider Selection
- Analyze differences between Claude and Llama outputs
- Evaluate sample content as fallback quality
- Make informed decisions about AI provider preferences

### Regeneration Validation
- Verify that regeneration scripts use correct providers
- Confirm content differences validate provider-specific generation
- Test that different providers actually produce different results

### Development Testing
- Debug AI integration issues
- Validate content extraction from templates
- Test metadata parsing and provider identification

## Technical Details

### File Structure
```
src/content_variants_analyzer.py  # Main analyzer script
Makefile                         # Contains variants targets
docs/variants_analysis.md        # This documentation
```

### Content Extraction
The analyzer uses regex patterns to extract content from markdown:
- Looks for section headers like `## Meine Qualifikationen`
- Extracts content between sections
- Handles various markdown formatting

### Metadata Sources
Provider/model information comes from:
1. `generation_info.json` files (primary)
2. Directory naming patterns (fallback)
3. Content analysis (last resort)

## Configuration

The analyzer can be extended by modifying:
- `ai_variables` list - Add new content sections to analyze
- Regex patterns - Adjust content extraction logic
- Output formatting - Customize table and display formats
- Statistical calculations - Add new metrics

## Dependencies

- Python 3.8+
- Standard library modules (json, re, pathlib, collections)
- Generated job application content in `Ausgabe/` directory