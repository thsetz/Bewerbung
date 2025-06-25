# Project Requirements Document: Bewerbung Generator

## 1. Introduction

### 1.1 Purpose
The purpose of this document is to define the functional and non-functional requirements for the **Bewerbung Generator** project. It serves as a comprehensive guide for development, testing, and stakeholder alignment.

<!-- Template content: The purpose of this document is to define the functional and non-functional requirements for the **[Project Name]** project. It serves as a comprehensive guide for development, testing, and stakeholder alignment. -->

The Bewerbung Generator is an AI-powered system designed to automate the creation of professional German job application documents. The system generates personalized cover letters (Anschreiben), resumes (Lebenslauf), and attachment lists (Anlagen) using multiple AI providers with intelligent fallback mechanisms.

### 1.2 Scope
This section describes what the project will and will not cover.

<!-- Template content: 
* **In Scope:** [Briefly describe the key functionalities and areas the project will address.]
* **Out of Scope:** [Briefly describe what the project will *not* address.]
-->

* **In Scope:** 
  - Automated generation of German job application documents (Anschreiben, Lebenslauf, Anlagen)
  - Multi-provider AI content generation (Claude, Llama/Ollama, sample fallback)
  - Template-based document rendering with Jinja2
  - PDF conversion and HTML preview generation
  - Directory-based organization with provider-specific outputs
  - Comprehensive documentation and regeneration scripts
  - CLI interface for batch processing
  - German language optimization and professional formatting

* **Out of Scope:** 
  - Web-based user interface or GUI application
  - Integration with job portals or application tracking systems
  - Multi-language support beyond German
  - Real-time collaborative editing
  - User account management or authentication systems
  - Cloud hosting or SaaS deployment

### 1.3 Definitions and Acronyms

<!-- Template content: [List and define any key terms, acronyms, or jargon used throughout the document.]
* **[Term]:** [Definition]
* **[Acronym]:** [Full form]
-->

* **Anschreiben:** German cover letter - personalized letter introducing the applicant
* **Lebenslauf:** German CV/resume - structured overview of qualifications and experience
* **Anlagen:** German attachments list - inventory of supporting documents
* **AI Provider:** External service or local model for generating personalized content
* **CLI:** Command Line Interface - text-based user interface for system interaction
* **PDF:** Portable Document Format - standardized document format for professional presentation
* **Jinja2:** Python templating engine for dynamic content generation
* **Ollama:** Local AI model management platform for privacy-focused generation
* **WeasyPrint:** Python library for HTML to PDF conversion

### 1.4 References

<!-- Template content: [List any documents or resources referenced in this document, e.g., business case, previous project documentation, industry standards.] -->

* Project README.md - System overview and quick start guide
* API Documentation - Anthropic Claude API and Ollama API specifications
* German Job Application Standards - DIN 5008 and professional formatting guidelines
* Sphinx Documentation - Complete technical documentation at docs/
* GitHub Repository - https://github.com/thsetz/Bewerbung

## 2. Stakeholders

### 2.1 Key Stakeholders

<!-- Template content: [Identify the main individuals or groups who have an interest in the project and their roles.]
* **[Stakeholder Role/Name]:** [Brief description of their involvement/interest]
-->

* **Job Seekers (Primary Users):** Individuals seeking employment in German-speaking markets who need professional application documents
* **Project Developer/Maintainer:** Technical lead responsible for system architecture, AI integration, and feature development
* **AI Service Providers:** External vendors (Anthropic Claude) and open-source communities (Ollama/Llama) providing content generation capabilities
* **Document Reviewers:** HR professionals and recruitment specialists who will evaluate generated application documents
* **System Administrators:** Technical personnel responsible for deployment, monitoring, and maintenance of the generation pipeline
* **Open Source Community:** Contributors and users who may extend, modify, or integrate the system

## 3. High-Level Project Goals & Objectives

<!-- Template content: [Clearly state the overarching goals and specific, measurable, achievable, relevant, and time-bound (SMART) objectives of the project.]

* **Goal 1:** [Description of goal]
    * **Objective 1.1:** [SMART objective]
    * **Objective 1.2:** [SMART objective]
* **Goal 2:** [Description of goal]
    * **Objective 2.1:** [SMART objective]
-->

* **Goal 1:** Automate Professional German Job Application Creation
    * **Objective 1.1:** Generate complete application packages (cover letter, CV, attachments) in under 30 seconds per application
    * **Objective 1.2:** Achieve 95% user satisfaction with generated document quality and personalization
    * **Objective 1.3:** Support processing of 100+ applications per day without performance degradation

* **Goal 2:** Provide Reliable Multi-Provider AI Integration
    * **Objective 2.1:** Maintain 99.5% system availability with intelligent fallback mechanisms
    * **Objective 2.2:** Support 3+ AI providers (Claude, Llama, sample content) with seamless switching
    * **Objective 2.3:** Achieve sub-10 second response times for AI content generation

* **Goal 3:** Enable Clean Output Organization and Reproducibility
    * **Objective 3.1:** Implement directory-only structure with zero root files in output folders
    * **Objective 3.2:** Generate 100% reproducible outputs through regeneration scripts
    * **Objective 3.3:** Provide comprehensive documentation for each generated application package

---

## 4. Functional Requirements

Functional requirements describe what the system **must do**. These are often expressed as user stories or use cases.

<!-- Template content: Functional requirements describe what the system **must do**. These are often expressed as user stories or use cases. -->

### 4.1 User Roles

<!-- Template content: [If applicable, define different types of users who will interact with the system.]
* **[User Role 1]:** [Description of their responsibilities and typical interactions]
* **[User Role 2]:** [Description]
-->

* **Job Seeker:** Primary user who provides profile and job description inputs to generate personalized application documents
* **System Administrator:** Technical user responsible for configuring AI providers, managing templates, and maintaining the generation pipeline

### 4.2 Core Features / Modules

<!-- Template content: [Organize functional requirements by major features or modules of the system.] -->

#### 4.2.1 Document Generation Workflow

* **FR-1.1:** As a job seeker, I want to generate a complete application package from my profile and a job description so that I can apply professionally with minimal manual effort.
    * **Description:** The system shall execute a 7-step workflow: (0) Clear AI cache, (1) Read newest profile, (2) Read newest job description, (3) Create output directory, (4) Generate AI content, (5) Create PDF directory, (6) Convert to PDF.
    * **Acceptance Criteria:**
        * System automatically discovers newest profile file matching pattern `YYYYMMDD_*.pdf` in `profil/` directory
        * System automatically discovers newest job description file matching pattern `YYYYMMDD_*.txt` in `Stellenbeschreibung/` directory
        * Output directory follows naming pattern: `{job_date}_{job_id}-{profile_date}_{profile_id}`
        * Generated documents include Anschreiben, Lebenslauf, and Anlagen in Markdown format
        * PDF conversion produces professional-quality documents with proper formatting
    * **Priority:** Critical
    * **Status:** Approved

* **FR-1.2:** As a job seeker, I want the system to clear AI content cache before generation so that I receive fresh, non-cached content for each application.
    * **Description:** System shall clear existing AI content cache (`.cache/ai_content_cache.json`) before each generation to ensure personalized content.
    * **Acceptance Criteria:**
        * Cache file is deleted automatically before content generation
        * User can control cache behavior via `CLEAR_CACHE_ON_START` environment variable
        * System provides clear feedback when cache is cleared or preserved
    * **Priority:** High
    * **Status:** Approved

#### 4.2.2 Multi-Provider AI Integration

* **FR-2.1:** As a job seeker, I want the system to generate content using multiple AI providers so that I have reliable content generation with intelligent fallbacks.
    * **Description:** System shall support Claude API, Ollama/Llama local models, and sample content with automatic provider selection and fallback.
    * **Acceptance Criteria:**
        * Primary provider order: Llama → Claude → Sample
        * Each available provider generates content in its own subdirectory
        * Provider failures don't prevent generation (graceful degradation)
        * `GENERATE_ALL_PROVIDERS=true` enables multi-provider mode (default)
    * **Priority:** Critical
    * **Status:** Approved

* **FR-2.2:** As a system administrator, I want to configure AI provider settings so that I can optimize performance and cost for different use cases.
    * **Description:** System shall allow configuration of AI provider preferences, model selection, and API parameters through environment variables.
    * **Acceptance Criteria:**
        * Support `AI_PROVIDER` environment variable for provider preference
        * Support model-specific configuration (e.g., `LLAMA_MODEL`, `CLAUDE_MODEL`)
        * Support API key configuration via `.env.local` files
        * Validate provider availability before generation
    * **Priority:** High
    * **Status:** Approved

#### 4.2.3 Directory-Only Output Organization

* **FR-3.1:** As a job seeker, I want all generated files organized in provider-specific subdirectories so that I can easily compare outputs and maintain clean organization.
    * **Description:** System shall create only subdirectories in output folders, with each AI provider getting its own dedicated folder containing all generated documents.
    * **Acceptance Criteria:**
        * No files created in root output directory
        * Each AI provider creates subdirectory (e.g., `claude_sonnet-3-5/`, `llama_3-2-latest/`, `sample_content/`)
        * Each subdirectory contains complete application package with PDF conversion
        * Each subdirectory includes regeneration scripts and documentation
    * **Priority:** Critical
    * **Status:** Approved

#### 4.2.4 Template System and Personalization

* **FR-4.1:** As a job seeker, I want the system to extract company and position information from job descriptions so that my applications are properly addressed and personalized.
    * **Description:** System shall parse job descriptions to extract company name, position title, address information, and reference numbers for template population.
    * **Acceptance Criteria:**
        * Extract company name, position title, and contact information
        * Handle various job description formats and layouts
        * Provide fallback values for missing information
        * Populate template variables with extracted data
    * **Priority:** High
    * **Status:** Approved

* **FR-4.2:** As a job seeker, I want AI-generated content sections that are contextually relevant to the specific job and company so that my applications demonstrate genuine interest and fit.
    * **Description:** System shall generate five distinct content sections: Einstiegstext, Fachliche Passung, Motivationstext, Mehrwert, and Abschlusstext, each tailored to the specific opportunity.
    * **Acceptance Criteria:**
        * Generate personalized opening paragraph (Einstiegstext)
        * Create technical qualifications match (Fachliche Passung)
        * Develop motivation and interest section (Motivationstext)
        * Articulate value proposition (Mehrwert)
        * Compose professional closing (Abschlusstext)
        * Each section contains relevant keywords from job description
    * **Priority:** High
    * **Status:** Approved

#### 4.2.5 PDF Generation and Documentation

* **FR-5.1:** As a job seeker, I want professional PDF versions of all application documents so that I can submit properly formatted applications to employers.
    * **Description:** System shall convert all Markdown documents to PDF format with professional styling and layout using WeasyPrint.
    * **Acceptance Criteria:**
        * Generate PDF files for all Markdown documents (Anschreiben, Lebenslauf, Anlagen, README)
        * Apply consistent professional styling and formatting
        * Include HTML preview versions for quick review
        * Maintain proper German typography and layout standards
    * **Priority:** High
    * **Status:** Approved

* **FR-5.2:** As a job seeker, I want comprehensive documentation and regeneration scripts for each application so that I can reproduce or modify generated content later.
    * **Description:** System shall generate README.md files, regeneration scripts, and metadata for each application package.
    * **Acceptance Criteria:**
        * Create detailed README.md with generation information and reproduction instructions
        * Generate platform-specific regeneration scripts (Linux/macOS: `.sh`, Windows: `.bat`)
        * Include metadata JSON with generation statistics and AI provider information
        * Provide troubleshooting guidance and validation instructions
    * **Priority:** Medium
    * **Status:** Approved

---

## 5. Non-Functional Requirements

Non-functional requirements describe **how** the system performs a function. They define quality attributes and constraints.

<!-- Template content: Non-functional requirements describe **how** the system performs a function. They define quality attributes and constraints. -->

### 5.1 Performance Requirements

<!-- Template content: 
* **NFR-Perf-1:** The system shall [e.g., respond to user requests within X seconds for Y% of interactions].
* **NFR-Perf-2:** The system shall support [X concurrent users] without degradation in performance.
-->

* **NFR-Perf-1:** The system shall complete document generation within 30 seconds for 95% of applications when all AI providers are available.
* **NFR-Perf-2:** The system shall support processing of 100+ applications per day without memory leaks or performance degradation.
* **NFR-Perf-3:** AI content generation shall complete within 10 seconds for individual content sections under normal network conditions.
* **NFR-Perf-4:** PDF conversion shall process all documents in an application package within 5 seconds.

### 5.2 Security Requirements

<!-- Template content:
* **NFR-Sec-1:** All user authentication shall require a minimum password length of [X characters] and include [e.g., uppercase, lowercase, numbers, special characters].
* **NFR-Sec-2:** All sensitive data shall be encrypted both in transit and at rest.
* **NFR-Sec-3:** The system shall be resilient to common web vulnerabilities (e.g., SQL injection, XSS).
-->

* **NFR-Sec-1:** All API keys and sensitive configuration shall be stored in environment variables or `.env.local` files, never committed to version control.
* **NFR-Sec-2:** All AI provider communications shall use HTTPS/TLS encryption for data in transit.
* **NFR-Sec-3:** The system shall not log or cache sensitive personal information from profiles or job descriptions beyond the intended AI content cache.
* **NFR-Sec-4:** Local AI processing (Ollama) shall be preferred for privacy-sensitive applications where external API calls are discouraged.

### 5.3 Usability Requirements

<!-- Template content:
* **NFR-Usab-1:** The user interface shall be intuitive and require minimal training for new users.
* **NFR-Usab-2:** Error messages shall be clear, concise, and provide actionable guidance.
-->

* **NFR-Usab-1:** The CLI interface shall provide clear progress indicators and step-by-step feedback during the 7-step generation process.
* **NFR-Usab-2:** Error messages shall be clear, concise, and provide actionable guidance including specific installation commands or configuration fixes.
* **NFR-Usab-3:** The system shall provide comprehensive documentation including quick start guides, troubleshooting, and FAQ sections.
* **NFR-Usab-4:** Generated README files shall include complete reproduction instructions and validation steps for non-technical users.

### 5.4 Reliability Requirements

<!-- Template content:
* **NFR-Rel-1:** The system shall have an uptime of at least [X%].
* **NFR-Rel-2:** The system shall be able to recover from a system failure within [X hours/minutes].
-->

* **NFR-Rel-1:** The system shall achieve 99.5% successful generation rate through intelligent AI provider fallback mechanisms.
* **NFR-Rel-2:** The system shall gracefully handle AI provider failures and continue generation with alternative providers or sample content.
* **NFR-Rel-3:** The system shall validate all dependencies and provide clear feedback when required components are missing or misconfigured.
* **NFR-Rel-4:** Generated documents shall be reproducible through provided regeneration scripts with 100% consistency.

### 5.5 Scalability Requirements

<!-- Template content:
* **NFR-Scal-1:** The system shall be able to scale to support [X% annual growth] in user base/data volume.
-->

* **NFR-Scal-1:** The system shall support processing multiple applications simultaneously through parallel execution capabilities.
* **NFR-Scal-2:** The multi-provider architecture shall allow easy addition of new AI providers without affecting existing functionality.
* **NFR-Scal-3:** The template system shall support easy customization and extension for different document types or languages.

### 5.6 Maintainability Requirements

<!-- Template content:
* **NFR-Maint-1:** The code shall be well-documented and follow established coding standards.
* **NFR-Maint-2:** The system architecture shall be modular to facilitate future enhancements and bug fixes.
-->

* **NFR-Maint-1:** The code shall be well-documented with comprehensive docstrings, type hints, and inline comments following Python PEP standards.
* **NFR-Maint-2:** The system architecture shall be modular with clear separation between AI providers, template management, and document generation components.
* **NFR-Maint-3:** The system shall include comprehensive test suites covering all major functionality and regression scenarios.
* **NFR-Maint-4:** All configuration shall be externalized through environment variables and configuration files to avoid code modifications for deployment.

### 5.7 Portability Requirements

<!-- Template content:
* **NFR-Port-1:** The system shall be compatible with [specify operating systems/browsers/devices].
-->

* **NFR-Port-1:** The system shall be compatible with macOS, Linux, and Windows operating systems through Python virtual environments.
* **NFR-Port-2:** All system dependencies shall be clearly documented with specific version requirements and installation instructions.
* **NFR-Port-3:** The system shall support both local AI models (Ollama) and cloud-based AI services (Claude API) for flexible deployment scenarios.

### 5.8 Legal and Compliance Requirements

<!-- Template content:
* **NFR-Legal-1:** The system shall comply with [e.g., GDPR, HIPAA, local regulations].
-->

* **NFR-Legal-1:** The system shall support GDPR compliance by providing local processing options and clear data handling transparency.
* **NFR-Legal-2:** Generated documents shall follow German professional standards and formatting conventions (DIN 5008).
* **NFR-Legal-3:** The system shall provide clear licensing information for all dependencies and AI provider usage terms.

---

## 6. Constraints

<!-- Template content: [List any limitations or restrictions that will impact the project, such as budget, timeline, technology, or resources.]

* **C-1:** Budget limited to [X currency].
* **C-2:** Project completion date by [Date].
* **C-3:** Must integrate with existing [System Name].
-->

* **C-1:** German language focus - system optimized specifically for German job market and application conventions.
* **C-2:** Python technology stack - all components must be compatible with Python 3.12+ and standard libraries.
* **C-3:** AI provider dependencies - system functionality dependent on external API availability and rate limits.
* **C-4:** CLI-only interface - no GUI or web interface planned for initial release.
* **C-5:** Local file system operations - system requires read/write access to local directories for input and output processing.
* **C-6:** WeasyPrint system dependencies - PDF generation requires platform-specific system libraries (pango, fonttools).

---

## 7. Assumptions

<!-- Template content: [Document any assumptions made during the requirements gathering process. If an assumption proves false, it could impact the project.]

* **A-1:** We assume that [e.g., key stakeholders will be available for regular feedback sessions].
* **A-2:** We assume that [e.g., necessary third-party APIs will be stable and well-documented].
-->

* **A-1:** We assume that users have basic command-line familiarity and can follow installation instructions for Python virtual environments.
* **A-2:** We assume that AI provider APIs (Anthropic Claude, Ollama) will remain stable and accessible with reasonable rate limits and pricing.
* **A-3:** We assume that input documents (profiles and job descriptions) will follow standard formats and be in German language.
* **A-4:** We assume that users have legitimate use cases for job application generation and will use the system ethically.
* **A-5:** We assume that system dependencies (Python, pip, system libraries) can be installed with standard package managers.
* **A-6:** We assume that generated documents will be reviewed and customized by users before submission to employers.

---

## 8. Open Issues

<!-- Template content: [List any unresolved questions or decisions that need to be made regarding the requirements.]

* **OI-1:** [Description of open issue and who is responsible for resolving it.]
-->

* **OI-1:** Integration with additional AI providers (OpenAI GPT, Google Gemini) - evaluate feasibility and demand for extended provider support.
* **OI-2:** Multi-language support expansion - assess requirements for English, French, or other European job markets.
* **OI-3:** Web interface development - determine if GUI/web interface would significantly improve user adoption and experience.
* **OI-4:** Integration with job portals - explore potential integrations with XING, LinkedIn, or German job boards for automated application submission.
* **OI-5:** Enterprise deployment model - evaluate requirements for organizational use, user management, and bulk processing capabilities.

---

## 9. Approval

<!-- Template content: [Sign-off section for key stakeholders to indicate their agreement with the documented requirements.]

* **Approved By:**
    * _________________________ (Name, Title, Date)
    * _________________________ (Name, Title, Date)
    * _________________________ (Name, Title, Date)
-->

* **Approved By:**
    * _________________________ (Project Lead/Developer, Date)
    * _________________________ (System Administrator, Date)
    * _________________________ (Primary User Representative, Date)

---

### Key Considerations When Using This Template:

<!-- Template content:
* **Tailor it:** This is a comprehensive template, but not every section will be relevant to every project. Remove or add sections as needed.
* **Involve Stakeholders:** Requirements gathering is a collaborative process. Ensure all relevant stakeholders are involved in defining and reviewing the requirements.
* **Prioritize:** Not all requirements are equally important. Prioritizing them helps in managing scope and making informed decisions.
* **Be Specific:** Vague requirements lead to misunderstandings. Be as clear and specific as possible.
* **Iterate:** Requirements are rarely perfect on the first try. Be prepared to refine and iterate as the project progresses.
-->

* **Tailor it:** This document reflects the current state and vision of the Bewerbung Generator project. Sections should be updated as the project evolves and new requirements emerge.
* **Involve Stakeholders:** Requirements gathering is a collaborative process. Regular feedback from job seekers, HR professionals, and technical users should inform requirement updates.
* **Prioritize:** Not all requirements are equally important. Critical features (document generation, AI integration) take precedence over convenience features (additional output formats).
* **Be Specific:** Vague requirements lead to misunderstandings. Performance metrics, acceptance criteria, and technical specifications provide clear implementation guidance.
* **Iterate:** Requirements are rarely perfect on the first try. The system architecture supports evolution through modular design and configuration-driven behavior.