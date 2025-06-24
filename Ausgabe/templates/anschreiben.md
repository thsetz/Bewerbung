# Anschreiben

---

## Briefkopf Absender

**{{ ABSENDER_VORNAME }} {{ ABSENDER_NACHNAME }}**  
{{ ABSENDER_TITEL }}  
{{ ABSENDER_STRASSE }} {{ ABSENDER_HAUSNUMMER }}  
{{ ABSENDER_PLZ }} {{ ABSENDER_ORT }}  

**Kontakt:**  
Telefon: {{ ABSENDER_TELEFON }}  
Mobil: {{ ABSENDER_MOBIL }}  
E-Mail: {{ ABSENDER_EMAIL }}  
{% if ABSENDER_LINKEDIN %}LinkedIn: {{ ABSENDER_LINKEDIN }}{% endif %}  
{% if ABSENDER_XING %}XING: {{ ABSENDER_XING }}{% endif %}  

---

## Adressat

**{{ ADRESSAT_FIRMA }}**  
{% if ADRESSAT_ABTEILUNG %}{{ ADRESSAT_ABTEILUNG }}{% endif %}  
{% if ADRESSAT_ANSPRECHPARTNER %}z.Hd. {{ ADRESSAT_ANSPRECHPARTNER }}{% endif %}  
{{ ADRESSAT_STRASSE }}  
{{ ADRESSAT_PLZ_ORT }}  
{% if ADRESSAT_LAND and ADRESSAT_LAND != 'Deutschland' %}{{ ADRESSAT_LAND }}{% endif %}

---

**{{ ABSENDER_ORT }}, {{ DATUM }}**

## Bewerbung um die Stelle als {{ STELLE }}
{% if STELLEN_ID %}Referenz: {{ STELLEN_ID }}{% endif %}

Sehr geehrte{% if adressat_ansprechpartner_geschlecht == "weiblich" %} Frau {{ adressat_ansprechpartner_nachname }}{% elif adressat_ansprechpartner_geschlecht == "männlich" %} Herr {{ adressat_ansprechpartner_nachname }}{% else %} Damen und Herren{% endif %},

{{ einstiegstext }}

## Meine Qualifikationen

{{ fachliche_passung }}

## Motivation

{{ motivationstext }}

## Mehrwert für Ihr Unternehmen

{{ mehrwert }}

{{ abschlusstext }}

Mit freundlichen Grüßen

{{ ABSENDER_VORNAME }} {{ ABSENDER_NACHNAME }}

---

**Anlagen:**
- Lebenslauf
- Zeugnisse und Zertifikate
- Referenzen