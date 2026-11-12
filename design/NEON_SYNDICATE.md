# NEON SYNDICATE — interface and visual specification

**Repository:** Fragile-Baby  
**Project focus:** E2K PLATFORM / CPU IDENTITY / TOOLCHAIN QUALIFICATION  
**Visual category:** E2K QUALIFICATION / TARGET EVIDENCE PENDING

## Brand and color
NEON SYNDICATE uses Void Black `#050505`, Warning Yellow `#FCEE0A`, System Red `#FF003C`, Data Blue `#00F0FF` and Interface White `#FFFFFF`. Carbon panels use `#0D1115` / `#11171C`; muted text uses `#A6B2BC`. Do not copy proprietary game art, logos or UI assets. Pair every semantic color with a label or icon.

## Typography and layout
Orbitron/Rajdhani for uppercase display headings; Rajdhani/system sans-serif for body; Roboto Mono/Share Tech Mono for IDs, code and measurements. Use asymmetrical information grids, fine structural rules, chamfered panels, restrained hex textures and tabular numerals.

## Motion and accessibility
Use 120–260 ms transitions and restrained edge glow. Glitch effects must never obscure important content or focus. Respect `prefers-reduced-motion`. Maintain keyboard focus, minimum 40 px controls and 44 px touch targets. Never use color as the only state cue.

## Project-specific focus
E2K PLATFORM / CPU IDENTITY / TOOLCHAIN QUALIFICATION

- CPU IDENTITY
- TOOLCHAIN ABI
- MEMORY MAP
- Reference flow: IDENTIFY → MATCH ABI → BUILD EVIDENCE → QUALIFY

The SVG is a design/architecture concept, not proof of a GUI, firmware boot path or live telemetry.

## Screenshot policy
Capture real runtime screenshots from the actual running app at a stated viewport (prefer 1920×1080 or higher). Use PNG/WebP for screenshots, label sample data and remove secrets/personal paths. Do not upscale tiny raster sources and call them native-resolution captures. The 1920×1200 SVG is a vector preview, not a runtime screenshot.

## Assets
- `assets/neon-syndicate/overview.svg` — project-specific visual concept.
- `assets/neon-syndicate/theme.css` — reusable web theme.
- `design/neon-syndicate.tokens.json` — machine-readable tokens.
