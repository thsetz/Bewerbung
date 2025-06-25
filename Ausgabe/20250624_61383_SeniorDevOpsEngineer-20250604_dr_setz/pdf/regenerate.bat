<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Regenerate</title>
    <style>
/* CSS Framework for Professional German Job Application Documents */

/* ==========================================================================
   Base Styles
   ========================================================================== */

@page {
    size: A4;
    margin: 2.5cm 2cm;
    @bottom-center {
        content: "Seite " counter(page) " von " counter(pages);
        font-size: 10pt;
        color: #666;
    }
}

* {
    box-sizing: border-box;
}

body {
    font-family: 'Arial', 'Helvetica', sans-serif;
    font-size: 11pt;
    line-height: 1.4;
    color: #333;
    margin: 0;
    padding: 0;
    background: white;
}

/* ==========================================================================
   Typography
   ========================================================================== */

h1 {
    font-size: 18pt;
    font-weight: bold;
    color: #2c3e50;
    margin: 0 0 20pt 0;
    padding-bottom: 8pt;
    border-bottom: 2pt solid #3498db;
}

h2 {
    font-size: 14pt;
    font-weight: bold;
    color: #2c3e50;
    margin: 20pt 0 10pt 0;
    padding-bottom: 4pt;
    border-bottom: 1pt solid #bdc3c7;
}

h3 {
    font-size: 12pt;
    font-weight: bold;
    color: #34495e;
    margin: 15pt 0 8pt 0;
}

p {
    margin: 0 0 10pt 0;
    text-align: justify;
}

strong {
    font-weight: bold;
    color: #2c3e50;
}

/* ==========================================================================
   Document Structure
   ========================================================================== */

.document {
    max-width: 100%;
    margin: 0 auto;
}

.header {
    margin-bottom: 30pt;
}

.sender-info {
    background: #f8f9fa;
    padding: 15pt;
    border-left: 4pt solid #3498db;
    margin-bottom: 20pt;
}

.sender-info h2 {
    margin-top: 0;
    border-bottom: none;
}

.contact-info {
    display: flex;
    flex-wrap: wrap;
    gap: 15pt;
    margin-top: 10pt;
}

.contact-item {
    flex: 1;
    min-width: 120pt;
}

.recipient {
    margin: 20pt 0;
    padding: 10pt 0;
}

.date-location {
    text-align: right;
    margin: 20pt 0;
    font-style: italic;
}

/* ==========================================================================
   Content Sections
   ========================================================================== */

.section {
    margin: 20pt 0;
    page-break-inside: avoid;
}

.section-title {
    background: #ecf0f1;
    padding: 8pt 12pt;
    margin: 0 0 12pt 0;
    font-weight: bold;
    color: #2c3e50;
    border-left: 4pt solid #3498db;
}

.experience-item {
    margin-bottom: 15pt;
    padding-left: 10pt;
    border-left: 2pt solid #ecf0f1;
}

.experience-period {
    font-weight: bold;
    color: #3498db;
    margin-bottom: 4pt;
}

.experience-title {
    font-weight: bold;
    margin-bottom: 2pt;
}

.experience-company {
    font-style: italic;
    color: #7f8c8d;
    margin-bottom: 6pt;
}

.experience-description ul {
    margin: 6pt 0;
    padding-left: 15pt;
}

.experience-description li {
    margin-bottom: 3pt;
}

/* ==========================================================================
   Skills and Qualifications
   ========================================================================== */

.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150pt, 1fr));
    gap: 15pt;
    margin: 15pt 0;
}

.skill-category {
    background: #f8f9fa;
    padding: 10pt;
    border-radius: 3pt;
    border-left: 3pt solid #3498db;
}

.skill-category h4 {
    margin: 0 0 8pt 0;
    font-weight: bold;
    color: #2c3e50;
}

.skill-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.skill-list li {
    margin-bottom: 3pt;
    padding-left: 12pt;
    position: relative;
}

.skill-list li:before {
    content: "▪";
    color: #3498db;
    position: absolute;
    left: 0;
}

/* ==========================================================================
   Personal Information
   ========================================================================== */

.personal-data {
    background: #f8f9fa;
    padding: 15pt;
    border-radius: 5pt;
    margin: 15pt 0;
}

.personal-data-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120pt, 1fr));
    gap: 10pt;
}

.personal-data-item {
    display: flex;
    flex-direction: column;
}

.personal-data-label {
    font-weight: bold;
    color: #7f8c8d;
    font-size: 9pt;
    margin-bottom: 2pt;
}

/* ==========================================================================
   Footer and Signature
   ========================================================================== */

.signature-section {
    margin-top: 30pt;
    text-align: left;
}

.signature-line {
    margin-top: 40pt;
    border-bottom: 1pt solid #bdc3c7;
    width: 200pt;
}

.attachments {
    margin-top: 25pt;
    background: #f8f9fa;
    padding: 12pt;
    border-radius: 3pt;
}

.attachments h3 {
    margin-top: 0;
}

.attachments ul {
    margin: 8pt 0 0 0;
    padding-left: 15pt;
}

.attachments li {
    margin-bottom: 3pt;
}

/* ==========================================================================
   Page Breaks and Print Optimization
   ========================================================================== */

.page-break {
    page-break-before: always;
}

.no-break {
    page-break-inside: avoid;
}

.keep-together {
    page-break-inside: avoid;
    page-break-after: avoid;
}

/* ==========================================================================
   Responsive Adjustments for HTML Preview
   ========================================================================== */

@media screen {
    body {
        background: #f5f5f5;
        padding: 20px;
    }
    
    .document {
        background: white;
        padding: 30pt;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        border-radius: 5px;
        max-width: 210mm;
        margin: 0 auto;
    }
}

/* ==========================================================================
   Utility Classes
   ========================================================================== */

.text-center { text-align: center; }
.text-right { text-align: right; }
.text-left { text-align: left; }

.font-small { font-size: 9pt; }
.font-large { font-size: 13pt; }

.color-primary { color: #3498db; }
.color-secondary { color: #7f8c8d; }
.color-dark { color: #2c3e50; }

.mb-small { margin-bottom: 5pt; }
.mb-medium { margin-bottom: 10pt; }
.mb-large { margin-bottom: 20pt; }

.mt-small { margin-top: 5pt; }
.mt-medium { margin-top: 10pt; }
.mt-large { margin-top: 20pt; }
    </style>
</head>
<body>
    <div class="document">
<p>@echo off<br />
REM Auto-generated regeneration script for job application<br />
REM Created: 2025-06-25T02:00:21.042481<br />
REM AI Provider: Unknown (Unknown)</p>
<p>echo 🔄 Regenerating job application with same configuration...<br />
echo 📊 Original generation: 2025-06-25T02:00:21.042481<br />
echo 🤖 AI Provider: Unknown (Unknown)</p>
<p>REM Check if we're in the right directory<br />
if not exist "Makefile" (<br />
    echo ❌ Error: Not in project root directory<br />
    echo Please run this script from the Bewerbung project root<br />
    exit /b 1<br />
)</p>
<p>REM Check Python<br />
python --version &gt;nul 2&gt;&amp;1<br />
if errorlevel 1 (<br />
    echo ❌ Python not found<br />
    exit /b 1<br />
)</p>
<p>REM Check virtual environment<br />
if not exist ".venv" (<br />
    echo ⚠️  Virtual environment not found, creating one...<br />
    python -m venv .venv<br />
)</p>
<p>REM Activate virtual environment<br />
call .venv\Scripts\activate.bat</p>
<p>REM Install dependencies<br />
echo 📦 Installing dependencies...<br />
pip install -r requirements.txt</p>
<p>REM Set environment variables for exact reproduction<br />
set AI_PROVIDER=claude<br />
set OUTPUT_STRUCTURE=by_model<br />
set INCLUDE_GENERATION_METADATA=true</p>
<p>REM Run generation<br />
echo 🚀 Starting generation...<br />
make generate</p>
<p>echo ✅ Regeneration completed successfully!<br />
echo 📁 Check output in: Ausgabe/<br />
echo 🔍 Compare with original using: python tests/test_regeneration.py</p>
<p>pause</p>
    </div>
</body>
</html>