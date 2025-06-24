# AI Content Generator

Das AI Content Generator System erstellt intelligente, personalisierte Inhalte für deutsche Bewerbungen basierend auf Stellenbeschreibungen und Bewerberprofilen.

## Hauptkomponenten

### 1. ContentType Enum
Definiert verschiedene Arten von AI-generiertem Content:
- `EINSTIEGSTEXT`: Persönlicher Einstieg ins Anschreiben
- `FACHLICHE_PASSUNG`: Match zwischen Qualifikationen und Stellenanforderungen  
- `MOTIVATIONSTEXT`: Motivation für die spezifische Position
- `MEHRWERT`: Wertversprechen für das Unternehmen
- `ABSCHLUSSTEXT`: Höflicher Abschluss des Anschreibens
- `BERUFSERFAHRUNG`: Verbesserte Berufserfahrung für Lebenslauf
- `AUSBILDUNG`: Verbesserte Ausbildungssektion
- `FACHKENNTNISSE`: Verbesserte technische Kenntnisse

### 2. Datenstrukturen

#### AIContentRequest
Anfrage-Struktur für AI Content Generation:
```python
@dataclass
class AIContentRequest:
    content_type: ContentType
    job_description: str
    profile_content: str
    company_name: str
    position_title: str
    additional_context: Optional[Dict[str, Any]] = None
```

#### AIContentResponse  
Antwort-Struktur mit generiertem Content:
```python
@dataclass
class AIContentResponse:
    content_type: ContentType
    generated_text: str
    confidence: float
    tokens_used: int
    processing_time: float
    metadata: Optional[Dict[str, Any]] = None
```

### 3. AIContentVariables Klasse

Definiert alle AI-Content-Variablen mit Metadaten:

#### Cover Letter Variables (Anschreiben)
- **einstiegstext**: Personalisierter Einstiegsabsatz (max. 300 Zeichen)
- **fachliche_passung**: Qualifikations-Match (max. 500 Zeichen)  
- **motivationstext**: Motivation für Position/Unternehmen (max. 400 Zeichen)
- **mehrwert**: Wertversprechen für Unternehmen (max. 300 Zeichen)
- **abschlusstext**: Professioneller Abschluss (max. 150 Zeichen)

#### CV Variables (Lebenslauf)
- **berufserfahrung_enhanced**: Verbesserte Berufserfahrung 
- **ausbildung_enhanced**: Verbesserte Ausbildungssektion
- **fachkenntnisse_enhanced**: Kategorisierte technische Kenntnisse

Jede Variable enthält:
- `description`: Beschreibung des Zwecks
- `example`: Beispieltext
- `max_length`: Maximale Textlänge
- `tone`: Gewünschter Tonfall
- `format`: Textformat (markdown, plain)

### 4. AIContentPrompts Klasse

#### System Prompt
Grundinstruktionen für AI-Modell:
- Deutsche Bewerbungsstandards
- Professioneller, natürlicher Ton
- Spezifisch auf Stellenausschreibung eingehen
- Konkret und präzise (keine Floskeln)

#### Content-spezifische Prompts
Für jeden ContentType existiert ein detaillierter Prompt mit:
- Stellenbeschreibung als Input
- Bewerberprofil als Kontext
- Spezifische Anweisungen für Tonfall und Stil
- Strukturierte Ausgabe-Anforderungen

Beispiel für EINSTIEGSTEXT:
```
Erstelle einen persönlichen Einstiegstext für ein Anschreiben.
- Warum diese spezielle Position interessant ist
- Bezug zur konkreten Stellenausschreibung  
- Erste Andeutung der Passung
Stil: Professionell, aber persönlich. Keine Standard-Floskeln.
```

### 5. ContentCache Klasse

Intelligentes Caching-System:
- **JSON-basierte Persistierung** von generierten Inhalten
- **Hash-basierte Cache-Keys** aus Request-Parametern
- **Automatische Serialisierung** von Request/Response-Objekten
- **Performance-Optimierung** durch Vermeidung doppelter API-Aufrufe

Funktionen:
- `get(request)`: Cached Response abrufen
- `set(request, response)`: Response cachen  
- `clear()`: Cache leeren
- `_generate_key()`: Eindeutigen Cache-Key erstellen

### 6. Sample Content Generator

Erstellt Beispiel-Inhalte für Tests ohne AI-API:
```python
def generate_sample_ai_content() -> Dict[str, str]:
    return {
        'einstiegstext': 'mit großem Interesse habe ich...',
        'fachliche_passung': 'Mit über 7 Jahren Erfahrung...',
        # ... weitere Beispiele
    }
```

## Workflow Integration

Das System integriert sich in den Bewerbungs-Generator:

1. **Template-Variablen** (lowercase) werden von AI generiert
2. **Umgebungsvariablen** (UPPERCASE) kommen aus .env
3. **Jinja2-Templates** verwenden beide Variablen-Typen
4. **Caching** verhindert redundante AI-Aufrufe
5. **Validation** stellt sicher, dass alle Variablen definiert sind

## Verwendung

```python
# Variable-Definitionen abrufen
variables = AIContentVariables.get_all_variables()
cover_vars = AIContentVariables.get_cover_letter_variables()

# Prompt für Content-Type generieren
prompt = AIContentPrompts.get_prompt(
    ContentType.EINSTIEGSTEXT,
    job_description="...",
    profile_content="...",
    company_name="TechCorp",
    position_title="DevOps Engineer"
)

# Caching verwenden
cache = ContentCache(Path("cache"))
cached_response = cache.get(request)
```

## Zukünftige Erweiterungen

- **Claude API Integration** für echte AI-Generierung
- **Interaktiver Modus** für Content-Verfeinerung  
- **Multi-Language Support** für internationale Bewerbungen
- **Template-spezifische Prompts** für verschiedene Branchen
- **Quality Scoring** für generierte Inhalte