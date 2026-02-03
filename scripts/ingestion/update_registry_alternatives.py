#!/usr/bin/env python3
"""
Update law registry with alternative verified sources.

This script:
1. Adds new laws (LFPPI, LGTAIP, LORCME)
2. Updates existing law URLs (LH)
3. Marks invalid entries (LGIMH)
4. Logs all changes
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

def update_registry():
    registry_path = Path("data/law_registry.json")
    
    # Backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = registry_path.with_suffix(f'.json.backup_{timestamp}')
    shutil.copy2(registry_path, backup_path)
    print(f"✅ Created backup: {backup_path}")
    
    # Load
    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    laws = registry['federal_laws']
    changes = []
    
    # 1. Add LFPPI (replaces old LPI)
    lfppi = {
        "id": "lfppi",
        "name": "Ley Federal de Protección a la Propiedad Industrial",
        "short_name": "LFPPI",
        "url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPPI.pdf",
        "remote_path": "pdf/LFPPI.pdf",
        "publication_date": "2020-07-01",
        "status": "active",
        "priority": 2,
        "tier": "commercial",
        "category": "federal",
        "slug": "lfppi",
        "notes": "Replaces old Ley de Propiedad Industrial (2018). Source verified 2026-02-03 from Cámara de Diputados."
    }
    
    # Check if already exists
    if not any(law['id'] == 'lfppi' for law in laws):
        laws.append(lfppi)
        changes.append("Added LFPPI (Industrial Property Protection)")
    
    # 2. Add LGTAIP
    lgtaip = {
        "id": "lgtaip",
        "name": "Ley General de Transparencia y Acceso a la Información Pública",
        "short_name": "LGTAIP",
        "url": "https://www.diputados.gob.mx/LeyesBiblio/pdf/LGTAIP.pdf",
        "remote_path": "pdf/LGTAIP.pdf",
        "publication_date": "2015-05-04",
        "status": "active",
        "priority": 1,
        "tier": "administrative",
        "category": "federal",
        "slug": "lgtaip",
        "notes": "General Transparency Law. Source verified 2026-02-03 from Cámara de Diputados."
    }
    
    if not any(law['id'] == 'lgtaip' for law in laws):
        laws.append(lgtaip)
        changes.append("Added LGTAIP (General Transparency)")
    
    # 3. Update LH URL
    for law in laws:
        if law['id'] == 'lh':
            old_url = law.get('url', '')
            law['url'] = "https://www.diputados.gob.mx/LeyesBiblio/pdf/LHidro.pdf"
            law['remote_path'] = "pdf/LHidro.pdf"
            if 'notes' not in law:
                law['notes'] = ''
            law['notes'] += f" URL corrected 2026-02-03. Original: {old_url}"
            changes.append("Updated LH URL to /LHidro.pdf")
    
    # 4. Add LORCME (historical/abrogated)
    lorcme = {
        "id": "lorcme",
        "name": "Ley de los Órganos Reguladores Coordinados en Materia Energética",
        "short_name": "LORCME",
        "url": "https://www.diputados.gob.mx/LeyesBiblio/abro/lorcme/LORCME_abro.pdf",
        "remote_path": "abro/lorcme/LORCME_abro.pdf",
        "publication_date": "2014-08-11",
        "status": "abrogated",
        "abrogation_date": "2025-03-18",
        "priority": 3,
        "tier": "energy",
        "category": "federal",
        "slug": "lorcme",
        "notes": "Abrogated March 2025 by energy sector reforms. Historical preservation. Source: Cámara de Diputados archive."
    }
    
    if not any(law['id'] == 'lorcme' for law in laws):
        laws.append(lorcme)
        changes.append("Added LORCME (abrogated energy law - historical)")
    
    # 5. Mark LGIMH as invalid
    for law in laws:
        if law['id'] == 'lgimh':
            law['status'] = 'invalid'
            law['notes'] = "Law does not exist. Erroneous registry entry. Research confirmed no 'Ley General de la Industria Minero-Hidrocarburos' exists in Mexican legislation."
            changes.append("Marked LGIMH as invalid (law never existed)")
    
    # Save
    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=4, ensure_ascii=False)
    
    print(f"\n✅ Registry updated successfully")
    print(f"\n📝 Changes made:")
    for i, change in enumerate(changes, 1):
        print(f"   {i}. {change}")
    
    print(f"\n📊 Registry stats:")
    print(f"   Total laws: {len(laws)}")
    print(f"   Active: {sum(1 for law in laws if law.get('status') == 'active')}")
    print(f"   Abrogated: {sum(1 for law in laws if law.get('status') == 'abrogated')}")
    print(f"   Invalid: {sum(1 for law in laws if law.get('status') == 'invalid')}")

if __name__ == "__main__":
    update_registry()
