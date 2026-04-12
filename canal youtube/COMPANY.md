---
name: CronicasDelUltimoHombre
description: Canal YouTube faceless post-apocalíptico — sistema multi-agente para producción autónoma diaria de episodios de 15 min con calidad cinematográfica. Objetivo: 1M de vistas el primer mes.
slug: canal-youtube
schema: agentcompanies/v1
version: 1.0.0
license: MIT
goals:
  - Publicar 1 episodio diario de 15 minutos estructurado como serie Netflix con cliffhangers
  - Alcanzar 1 millón de vistas el primer mes mediante estrategia de retención y CTR >10%
  - Generar imágenes cinematográficas con Fooocus/ComfyUI usando RTX 5090 (32GB VRAM)
  - Generar video con LTX Video 2 MAX y Wan2.1 en local (RTX 5090)
  - Clonar voz de Elián con XTTSv2 para narración en español
  - Mantener continuidad narrativa entre episodios (arcos de 10 episodios)
  - Maximizar monetización del canal (objetivo $10K+/mes en 12 meses)
  - Buscar y evaluar diariamente nuevas herramientas AI en GitHub (>100 estrellas, <7 días)
  - Escalar decisiones humanas: aprobación final de episodios, budget de ads, cambios de estrategia
---

# Crónicas del Último Hombre — Sistema Multi-Agente

Canal YouTube faceless post-apocalíptico de alta retención. Este sistema orquesta **9 agentes de IA especializados** coordinados por el CEO para producir episodios diarios de calidad cinematográfica de forma autónoma.

**Concepto del canal**: Mundo post-guerra nuclear. Elián, un viajero solitario, busca la "Fuente de la Vida Eterna" (que resulta ser un despertar espiritual, no físico). Estética: The Road + Stalker (Tarkovski) + Children of Men.

**Stack tecnológico**:
- Hardware: NVIDIA RTX 5090 (32GB VRAM)
- Imágenes: Fooocus / ComfyUI + SDXL Lightning / Flux.1-dev
- Video: LTX Video 2 MAX (cliffhangers) + Wan2.1 (contemplativo)
- Audio/Voz: XTTSv2 (voz clonada de Elián)
- Edición: FFmpeg + DaVinci Resolve
- LLM local: Qwen3.5:35B via Ollama
- Upload: YouTube API automático

## Estructura organizativa

```
CEO Orchestrator
├── CMO — Director Creativo
│   ├── YouTube Series Writer (guiones)
│   ├── Post-Apocalyptic Storyteller (lore y mundo)
│   └── YouTube Growth Strategist (algoritmo y CTR)
├── CTO — Director de Producción
│   ├── Visual Prompts Engineer (prompts imágenes/video)
│   ├── Video Production Coordinator (pipeline completo)
│   ├── Faceless Channel Optimizer (monetización)
│   └── GitHub Discovery CTO (nuevas tecnologías)
└── Survival Skills Expert (técnicas verificables)
```

## Pipeline de producción (6-8h por episodio)

```
STAGE 1: Pre-producción (1-2h)
├── YouTube Series Writer → guion completo 1800 palabras
├── Survival Skills Expert → técnica verificable del episodio
├── Post-Apocalyptic Storyteller → lore y continuidad
└── Visual Prompts Engineer → 59 prompts SDXL/LTX2 en inglés

STAGE 2: Audio (5-10 min)
└── XTTSv2 → voz de Elián en español

STAGE 3: Imágenes (2-3h)
└── Fooocus / ComfyUI + SDXL Lightning → batch 12 imágenes

STAGE 4: Video (2-3h)
├── LTX2-MAX → cliffhangers dinámicos (30-60fps)
└── Wan2.1 → escenas contemplativas (24fps)

STAGE 5: Ensamblaje (1h)
└── FFmpeg → video final + subtítulos

STAGE 6: Upload (5 min)
└── YouTube API → programado para las 00:00
```

## Episodios planificados

- EP001: La Ciudad del Eco (grabadora con voces del pasado)
- EP002: El Jardín de Ceniza (plantas que crecen entre ruinas)
- EP003: La Última Biblioteca (libros como último tesoro)
- EP004: El Río de Cristal (agua contaminada que cura sueños)
- EP005: La Torre del Vigía (señal de radio misteriosa)
