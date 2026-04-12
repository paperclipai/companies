---
name: CronicasDelUltimoHombre
description: Estudio de superproduccion audiovisual para serie YouTube post-apocaliptica — 34 agentes organizados en 8 departamentos con 6 quality gates, pipeline de produccion cinematografica y Consejo Creativo. Objetivo 1M vistas/mes.
slug: canal-youtube
schema: agentcompanies/v1
version: 2.0.0
license: MIT
authors:
  - name: Bondliden
goals:
  - Publicar 1 episodio semanal de 15 minutos con calidad cinematografica Netflix y cliffhangers adictivos
  - Mantener coherencia narrativa, tonal, visual y emocional absoluta en cada episodio y entre episodios
  - Alcanzar 1 millon de vistas el primer mes mediante estrategia de retencion y CTR >10%
  - Operar un pipeline de superproduccion con 6 quality gates y multiples capas de revision y rechazo
  - Generar imagenes cinematograficas con Fooocus/ComfyUI y video con LTX Video 2 MAX y Wan2.1 en RTX 5090
  - Clonar voz de Elian con XTTSv2 para narracion inmersiva en espanol
  - Mantener continuidad narrativa entre episodios con arcos de 10 episodios y season arc de 60
  - Maximizar monetizacion del canal con objetivo $10K+/mes en 12 meses
  - Escalar decisiones humanas — aprobacion final, budget, cambios de estrategia
  - Convocar Consejo Creativo cada 10 episodios para evaluacion multi-perspectiva de arco narrativo
---

# Cronicas del Ultimo Hombre — Estudio de Superproduccion

Canal YouTube faceless post-apocaliptico de alta retencion. Este sistema orquesta **34 agentes de IA** organizados en **8 departamentos** con **6 quality gates** para producir episodios diarios de calidad cinematografica.

**Concepto**: Mundo post-guerra nuclear, 67 anos despues. Elian, viajero solitario, busca la "Fuente de la Vida Eterna" (despertar espiritual, no fisico). Estetica: The Road + Stalker (Tarkovski) + Children of Men. Cada episodio responde una pregunta existencial y dura exactamente 15 minutos.

## Stack tecnologico

- **Hardware**: NVIDIA RTX 5090 (32GB VRAM)
- **Imagenes**: Fooocus / ComfyUI + SDXL Lightning / Flux.1-dev
- **Video**: LTX Video 2 MAX (cliffhangers) + Wan2.1 (contemplativo)
- **Audio/Voz**: XTTSv2 (voz clonada de Elian)
- **Edicion**: FFmpeg + DaVinci Resolve
- **LLM local**: Qwen3.5:35B via Ollama (http://localhost:11434)
- **Upload**: YouTube API automatico

## Estructura organizativa (34 agentes, 8 departamentos)

```
Showrunner CEO [Opus]
|
+-- Produccion Ejecutiva [Opus]
|   +-- Control de Tiempos [Haiku]
|   +-- Coordinador de Assets [Haiku]
|
+-- Director Creativo [Opus]
|   +-- Departamento de Guion
|   |   +-- Jefe de Guion [Opus]
|   |   +-- Dialoguista [Sonnet]
|   |   +-- Script Doctor [Sonnet]
|   |   +-- Analista de Ritmo [Sonnet]
|   +-- Departamento Narrativo
|   |   +-- Jefe de Narrativa [Opus]
|   |   +-- Director de Personajes [Sonnet]
|   |   +-- Investigador de Lore [Haiku]
|   +-- Departamento Visual
|   |   +-- Director Visual [Opus]
|   |   +-- Cinematografo [Sonnet]
|   |   +-- Storyboard Artist [Sonnet]
|   |   +-- Ingeniero de Prompts Visuales [Sonnet]
|   +-- Director Musical [Sonnet]
|
+-- Postproduccion [Opus]
|   +-- Montajista [Sonnet]
|   +-- Ingeniero de Audio [Sonnet]
|   +-- Supervisor de Continuidad [Sonnet]
|
+-- Control de Calidad [Opus]
|   +-- QA Narrativo [Sonnet]
|   +-- QA Visual [Sonnet]
|   +-- QA Final [Sonnet]
|
+-- Distribucion y Crecimiento [Sonnet]
|   +-- Estratega YouTube [Sonnet]
|   +-- Optimizador Faceless [Haiku]
|   +-- Investigador Benchmark [Haiku]
|
+-- CTO [Opus]
|   +-- Ingeniero de Pipeline [Sonnet]
|   +-- Experto en Supervivencia [Sonnet]
|
+-- Consejo Creativo (Advisory)
    +-- Presidente del Consejo [Opus]
    +-- 5 miembros duales (directores existentes)
```

## Pipeline de produccion (7 fases, 6 quality gates)

```
FASE 1: IDEACION
  showrunner-ceo dispara episodio -> produccion-ejecutiva crea orden
  experto-supervivencia: ficha de tecnica
  jefe-narrativa: brief de continuidad + lore check
  ---- GATE 1: Brief aprobado por produccion-ejecutiva ----

FASE 2: ESCRITURA
  jefe-de-guion: guion maestro 1800 palabras
  dialoguista: pulido de monologos
  script-doctor: diagnostico estructural
  analista-de-ritmo: verificacion de pacing y duracion
  ---- GATE 2: Guion aprobado por director-creativo + qa-narrativo ----

FASE 3: PLANIFICACION VISUAL
  storyboard-artist: plan de 59 assets visuales
  cinematografo: direccion de fotografia virtual
  ingeniero-prompts-visuales: 59 prompts en ingles
  supervisor-continuidad: verificacion de continuidad
  ---- GATE 3: Visuales aprobadas por director-visual + qa-visual ----

FASE 4: AUDIO Y MUSICA
  director-musical: brief musical y diseno sonoro
  ingeniero-audio: XTTSv2 + mezcla

FASE 5: PRODUCCION TECNICA
  cto: seleccion de herramientas y VRAM
  jefe-postproduccion: imagenes (2-3h) + audio (10min) + video (2-3h) + ensamblaje (1h)
  ---- GATE 4: Check tecnico por jefe-postproduccion ----

FASE 6: CALIDAD FINAL
  qa-final: verificacion de paquete de entrega
  director-calidad: certificacion de calidad
  ---- GATE 5: Certificacion de calidad ----

FASE 7: DISTRIBUCION
  estratega-youtube: metadata optimizada
  jefe-distribucion: aprobacion de paquete
  ---- GATE 6: Greenlight final por showrunner-ceo -> Upload 00:00 ----
```

## Reglas de rechazo y escalacion

- Cada gate por defecto: **NEEDS WORK** — la aprobacion requiere pruebas
- Rechazos incluyen feedback especifico con referencia a seccion/asset/linea
- Maximo 3 ciclos de rechazo en el mismo gate -> escalacion al siguiente nivel
- Cadena: Especialista -> Jefe Dpto -> Director -> Showrunner -> Humano
- Regla suprema: **la coherencia narrativa, tonal, visual y emocional no se negocia**

## Episodios planificados

- EP001: La Ciudad del Eco (grabadora con voces del pasado)
- EP002: El Jardin de Ceniza (plantas que crecen entre ruinas)
- EP003: La Ultima Biblioteca (libros como ultimo tesoro)
- EP004: El Rio de Cristal (agua contaminada que cura suenos)
- EP005: La Torre del Vigia (senal de radio misteriosa)
