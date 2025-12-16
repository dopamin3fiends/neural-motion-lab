# Style Transfer Video Guide

Learn how to apply different artistic styles to your video generation using LoRAs and style-specific workflows.

## What is Style Transfer?

Style transfer in video generation applies specific artistic aesthetics to your motion:
- Anime/manga style
- Photorealistic rendering
- Painterly/artistic effects
- Cinematic film looks
- Fantasy/surreal aesthetics

The style is maintained consistently across all frames.

## Prerequisites

- Completed [basic_usage.md](basic_usage.md)
- Style LoRAs downloaded (anime, realistic, artistic, etc.)
- Understanding of LoRA basics

## Available Style Presets

Check `configs/lora_presets.yaml` for all available styles:

### Anime Style
- **File**: `style_anime_lora.safetensors`
- **Strength**: 0.7
- **Best for**: Character animation, vibrant colors, expressive motion
- **Prompt additions**: "anime style, vibrant colors, expressive"

### Realistic Style
- **File**: `style_realistic_lora.safetensors`
- **Strength**: 0.8
- **Best for**: Natural motion, photographic quality
- **Prompt additions**: "photorealistic, detailed, natural lighting"

### Artistic/Painterly
- **File**: `style_artistic_lora.safetensors`
- **Strength**: 0.75
- **Best for**: Creative projects, artistic expression
- **Prompt additions**: "artistic, painterly, creative composition"

### Cinematic
- **File**: `style_cinematic_lora.safetensors`
- **Strength**: 0.8
- **Best for**: Film-quality videos, dramatic scenes
- **Prompt additions**: "cinematic, film grain, dramatic lighting"

### Fantasy
- **File**: `style_fantasy_lora.safetensors`
- **Strength**: 0.7
- **Best for**: Magical scenes, otherworldly aesthetics
- **Prompt additions**: "fantasy, magical, ethereal atmosphere"

## Method 1: Single Style Application

### Step 1: Load LoRA Workflow

```bash
# In ComfyUI
Load: neural-motion-lab/workflows/lora_i2v.json
```

### Step 2: Select Style LoRA

In the **LoraLoader** node:
1. Click on LoRA file dropdown
2. Select your desired style (e.g., `style_anime_lora.safetensors`)
3. Set strength values (use preset recommendations)

### Step 3: Craft Style-Appropriate Prompt

Match your prompt to the style:

**Anime Style:**
```
Anime character with expressive eyes walking through vibrant city, 
dynamic motion, colorful environment, anime aesthetic, smooth animation
```

**Realistic Style:**
```
Person walking down urban street, natural lighting, photorealistic details, 
subtle motion, realistic physics, cinematic realism
```

**Artistic Style:**
```
Painterly figure moving through impressionist landscape, 
artistic brushstrokes, creative composition, flowing motion
```

**Cinematic Style:**
```
Subject walking in dramatic lighting, film grain texture, 
cinematic color grading, professional filmmaking, 35mm aesthetic
```

**Fantasy Style:**
```
Magical character moving through mystical forest, ethereal atmosphere, 
fantasy lighting, otherworldly effects, dreamlike quality
```

### Step 4: Adjust Style Intensity

Control style strength through LoRA values:

- **Subtle (0.5-0.6)**: Light style influence
- **Balanced (0.7-0.8)**: Clear style, maintains quality
- **Strong (0.9-1.0)**: Maximum style, may affect coherence

### Step 5: Configure Complementary Settings

**For Anime/Fantasy:**
- CFG Scale: 6.5-7.5 (higher for style adherence)
- Steps: 30-35
- Sampler: dpmpp_2m

**For Realistic/Cinematic:**
- CFG Scale: 6.0-7.0
- Steps: 30-40 (higher for detail)
- Sampler: dpmpp_sde or ddim

**For Artistic:**
- CFG Scale: 5.5-7.0 (lower for creativity)
- Steps: 25-35
- Sampler: euler_a or dpmpp_2m

## Method 2: Multi-Style Combinations

### Load Advanced Workflow

```bash
# In ComfyUI
Load: neural-motion-lab/workflows/advanced_variations.json
```

This workflow supports multiple LoRAs stacked together.

### Common Combinations

#### Anime + Character Consistency
```yaml
LoRA 1: style_anime_lora (0.7)
LoRA 2: character_consistency_lora (0.85)
Use: Character-focused anime videos
```

#### Cinematic + Smooth Motion
```yaml
LoRA 1: style_cinematic_lora (0.8)
LoRA 2: motion_smooth_lora (0.6)
Use: Film-quality smooth sequences
```

#### Realistic + Detail Enhancer
```yaml
LoRA 1: style_realistic_lora (0.8)
LoRA 2: detail_enhancer_lora (0.5)
Use: Ultra-detailed photorealistic videos
```

#### Fantasy + Character + Detail
```yaml
LoRA 1: style_fantasy_lora (0.7)
LoRA 2: character_consistency_lora (0.85)
LoRA 3: detail_enhancer_lora (0.5)
Use: High-quality fantasy character animation
```

### Balancing Multiple LoRAs

**Rule of thumb:**
1. **Primary style**: Highest strength (0.7-0.8)
2. **Secondary effect**: Medium strength (0.6-0.7)
3. **Enhancement**: Lower strength (0.4-0.5)

**Total combined strength shouldn't exceed ~2.0** to avoid over-fitting.

## Style-Specific Techniques

### Anime Style Optimization

**Best practices:**
- Use vibrant, saturated colors in reference images
- Include "anime" in prompt
- Reference anime character designs
- Higher CFG for style consistency

**Prompt template:**
```
anime style, [character] [action], vibrant colors, expressive motion, 
clean lines, anime aesthetic, detailed animation
```

**Common issues:**
- Style too weak → Increase LoRA to 0.8
- Colors washed out → Add "vibrant, saturated" to prompt
- Looks Western → Add "japanese anime style"

### Realistic Style Optimization

**Best practices:**
- Use actual photographs as references
- Include lighting descriptions
- Focus on natural physics
- Describe materials and textures

**Prompt template:**
```
photorealistic [subject] [action], natural lighting, detailed textures, 
realistic physics, cinematic realism, high quality photography
```

**Common issues:**
- Looks artificial → Increase steps to 40
- Too stylized → Reduce other LoRAs
- Lighting flat → Specify lighting in prompt

### Cinematic Style Optimization

**Best practices:**
- Reference film stills
- Describe camera and lighting
- Use film terminology
- Embrace grain and imperfections

**Prompt template:**
```
cinematic [subject] [action], dramatic lighting, film grain, 
color grading, 35mm film aesthetic, professional cinematography
```

**Color grading options:**
- "teal and orange grading"
- "warm sunset tones"
- "cool blue tones"
- "desaturated aesthetic"

### Artistic Style Optimization

**Best practices:**
- Reference famous art styles
- Embrace abstraction
- Focus on composition
- Allow creative interpretation

**Prompt template:**
```
artistic [subject] [action], painterly style, impressionist brushstrokes, 
creative composition, expressive colors, artistic interpretation
```

**Specific art styles:**
- "impressionist painting style"
- "oil painting aesthetic"
- "watercolor style"
- "digital art style"

## Advanced Style Techniques

### Style Morphing

Create videos that transition between styles:

1. Generate with Style A (LoRA strength 0.8)
2. Generate with Style B (LoRA strength 0.8)
3. Use video editing to crossfade
4. Or: Intermediate render with both LoRAs (0.5 each)

### Regional Style Application

Apply different styles to different regions:

1. Use segmentation/masking nodes
2. Apply style LoRA to specific regions
3. Blend regions in post-processing

*Note: Requires advanced ComfyUI node setup*

### Style Intensity Animation

Vary style strength across the video:

- Start: High style (0.9) for dramatic opening
- Middle: Medium style (0.7) for action
- End: Subtle style (0.5) for naturalistic close

*Requires multiple renders or custom nodes*

## Prompt Engineering for Styles

### Style Keywords Library

**Anime/Manga:**
- anime, manga, cel shaded, vibrant, expressive
- japanese animation, studio quality, anime aesthetic

**Realistic:**
- photorealistic, realistic, detailed, natural
- photography, real life, lifelike, authentic

**Artistic:**
- painterly, artistic, impressionist, expressive
- brushstrokes, canvas texture, artistic interpretation

**Cinematic:**
- cinematic, film grain, color grading, dramatic
- 35mm, anamorphic, professional filmmaking

**Fantasy:**
- fantasy, magical, ethereal, mystical, otherworldly
- enchanted, supernatural, dreamlike

### Negative Prompts by Style

**Anime:**
```
realistic, photographic, western style, 3D render, low quality
```

**Realistic:**
```
anime, cartoon, artistic, stylized, painting, drawn
```

**Artistic:**
```
photographic, realistic, digital, sharp, clinical
```

**Cinematic:**
```
amateur, low budget, digital video, smartphone quality
```

## Quality Comparison

### Resolution Impact on Style

- **480p**: Styles appear softer, details reduced
- **720p**: Good balance for most styles (recommended)
- **1080p**: Maximum detail, best for realistic/detailed styles

### Step Count Impact

- **20 steps**: Style present but rough
- **25-30 steps**: Good quality for most styles
- **35-40 steps**: Best quality, especially for realistic
- **40+ steps**: Diminishing returns

## Troubleshooting

### Style Too Weak
- Increase LoRA strength by 0.1-0.2
- Add style keywords to prompt
- Increase CFG scale
- Reduce conflicting LoRAs

### Style Too Strong
- Decrease LoRA strength
- Lower CFG scale
- Add variety terms to prompt
- Balance with other LoRAs

### Style Inconsistent
- Increase steps to 35+
- Use karras scheduler
- Increase CFG scale
- Simplify prompt

### Colors Wrong
- Adjust style LoRA strength
- Add color terms to prompt
- Check reference image colors
- Try different sampler

## Style Examples Gallery

### Anime Character Walk
```yaml
Input: Character portrait
Style: Anime (0.7)
Prompt: "Anime character walking confidently, vibrant colors, expressive"
Settings: 30 steps, CFG 7.0
```

### Cinematic Street Scene
```yaml
Input: Urban photograph
Style: Cinematic (0.8)
Prompt: "Person walking down moody street, film noir, dramatic lighting"
Settings: 35 steps, CFG 6.5
```

### Fantasy Magic Cast
```yaml
Input: Fantasy character
Style: Fantasy (0.7) + Detail (0.5)
Prompt: "Mage casting spell, magical particles, ethereal atmosphere"
Settings: 35 steps, CFG 7.0
```

## Batch Style Processing

Process one image with multiple styles:

```python
# Pseudo-code for batch processing
for style in ['anime', 'realistic', 'cinematic']:
    load_lora(f'style_{style}_lora.safetensors')
    generate_video(input_image, style_prompt)
```

## Next Steps

- Experiment with style combinations
- Train custom style LoRAs
- Create style preset libraries
- Share results with community

Master the art of style transfer! 🎨
