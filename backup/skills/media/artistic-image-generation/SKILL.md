---
name: artistic-image-generation
description: Generate artistic images with polli CLI.
category: media
---

# Artistic Image Generation

Generate high-quality artistic images using Pollinations CLI (klein model) with detailed, descriptive prompts.

## When to use
- User wants artistic/illustrative images (paintings, surreal art, concepts)
- Prompt requires detailed artistic description (style, lighting, mood)
- Need image for articles, presentations, or creative projects

## Model
Always use `--model klein` (FLUX.2 Klein 4B) — fast, high-quality, supports up to 2.4MP.

## Command Template
```bash
export PATH="/opt/data/.local/bin:$PATH"
polli gen image "<detailed prompt>" --model klein --output /opt/data/hermes/<agent>/reports/<filename>.png
```

## Prompt Engineering Tips
1. **Start with medium/style**: "A surrealist oil painting", "An acrylic watercolor illustration", "A digital painting"
2. **Specify artist influence** (optional): "Salvador Dali style", "Art Nouveau inspired", "Impressionist style"
3. **Describe scene composition**: subject, setting, perspective
4. **Add lighting**: "warm sunset light", "moonlight glow", "golden hour", "dramatic shadows"
5. **Include mood/atmosphere**: "ethereal", "melancholic", "dreamlike", "mystical"
6. **Specify details**: "intricate details", "highly detailed brush strokes", "soft focus"
7. **Add texture**: "classical oil painting texture", "canvas texture", "smooth digital"

## Example Prompts

### Surrealist
```
A surrealist oil painting, Salvador Dali style, an infinite desert with melting horizon, giant floating fish swimming in the sky above the desert, intricate details, soft dreamy clouds, warm sunset light, barren desert with a single dead tree, highly detailed brush strokes, ethereal, melancholic mood, classical oil painting texture, golden hour lighting, surreal perspective, dreamlike atmosphere
```

### Night Scene
```
A mystical moonlit forest scene, a serene lake reflecting the full moon, a small wooden boat floating on still water, towering ancient trees with glowing fireflies, starry night sky, soft mist rising from water surface, cinematic lighting, dreamy atmosphere, detailed fantasy illustration, deep blues and silvers, tranquil mood
```

### Fantasy Landscape
```
An epic fantasy landscape painting, ancient stone ruins overgrown with glowing crystals, waterfall cascading into crystal clear pool, bioluminescent plants, dramatic storm clouds parting to reveal golden sunlight, mountains in distance, highly detailed digital painting, concept art style, atmospheric perspective, magical realism
```

## Output Convention
- Save to agent-specific reports folder: `/opt/data/hermes/<agent>/reports/`
- Filename format: `<theme>-<style>.png`
- After generation: upload via FTP and commit to GitHub

## Workflow
1. Generate image with polli
2. Upload: `python3 /opt/data/hermes/shared/ftp_upload.py <file> /<agent>/`
3. Commit: `git -C /opt/data/hermes add <file> && git -C /opt/data/hermes commit -m "<Agent>: <filename>"`
4. Push: `git -C /opt/data/hermes push origin main`
5. Return URL: `https://taraka.id/hermes/<agent>/<filename>`

## Notes
- API key has limited permissions (no balance check), but generation works
- Always use `--output` flag to specify exact file path
- Use `klein` model by default unless user specifies otherwise