# Character Animation Guide

This guide covers creating character-consistent animations where the character maintains their appearance, features, and identity throughout the video.

## What is Character Consistency?

Character consistency ensures that:
- Facial features remain stable
- Clothing and accessories don't morph
- Body proportions stay consistent
- Character identity is maintained across all frames

## Prerequisites

- Completed [basic_usage.md](basic_usage.md) tutorial
- Character consistency LoRA (downloaded or trained)
- High-quality reference image of your character

## Preparing Your Character Reference

### Image Requirements

**Essential:**
- Clear, well-lit portrait or full body shot
- Character facing forward or 3/4 view
- High resolution (1024px+ recommended)
- Sharp focus on character
- Minimal background distractions

**Recommended:**
- Neutral or simple background
- Good contrast between character and background
- Character centered in frame
- Natural pose (not extreme angles)

### Multiple Reference Images

For best results, you can prepare:
1. **Primary reference**: Front-facing, clear features
2. **Secondary reference**: Side profile or 3/4 view
3. **Full body reference**: Complete character appearance

## Method 1: Using Character Consistent Workflow

### Step 1: Load the Workflow

```bash
# In ComfyUI
Load: neural-motion-lab/workflows/character_consistent.json
```

### Step 2: Configure Reference Image

1. **LoadImage node**: Select your character reference image
2. The image feeds into multiple nodes:
   - VAE Encode (for latent representation)
   - IPAdapter (for feature extraction)
   - ControlNet (for pose guidance)

### Step 3: Configure LoRA

In the **LoraLoader** node:
- **LoRA file**: Select `character_consistency_lora.safetensors`
- **Strength (model)**: 0.85 (recommended starting point)
- **Strength (clip)**: 0.85

**Strength Guidelines:**
- **0.6-0.7**: Subtle consistency, allows more variation
- **0.8-0.9**: Strong consistency (recommended)
- **0.9-1.0**: Maximum consistency, may reduce motion quality

### Step 4: Configure IPAdapter

The **IPAdapter** node helps maintain visual features:
- **Weight**: 0.7 (recommended)
- Lower for more flexibility, higher for stricter consistency

### Step 5: Configure ControlNet

The **ControlNet** node maintains pose structure:
- **Strength**: 0.8 (recommended)
- Uses OpenPose or similar for pose preservation

### Step 6: Write Character-Aware Prompts

**Positive Prompt Template:**
```
[Character description], [action/motion], maintaining consistent features, 
character walking forward, high quality animation, detailed face, 
consistent clothing, smooth motion
```

**Example:**
```
A young woman with long brown hair and blue eyes, wearing a red jacket, 
walking forward confidently, maintaining facial features, smooth natural movement, 
high quality, detailed, consistent appearance
```

**Negative Prompt:**
```
blurry, low quality, distorted, artifacts, inconsistent character, 
face morphing, changing features, different clothing, style inconsistency
```

### Step 7: Adjust Sampling Settings

For character consistency, use:
- **Steps**: 30-35 (higher helps stability)
- **CFG Scale**: 7.0 (higher enforces consistency)
- **Sampler**: dpmpp_2m (balanced)
- **Scheduler**: karras

### Step 8: Generate and Evaluate

1. Generate first video
2. Review for consistency issues
3. Adjust LoRA strength if needed
4. Regenerate with tweaked settings

## Method 2: Using LoRA-Enhanced Workflow

For simpler character consistency without IPAdapter/ControlNet:

### Load Workflow
```bash
# In ComfyUI
Load: neural-motion-lab/workflows/lora_i2v.json
```

This workflow uses only the LoRA for consistency, which is:
- **Faster** to generate
- **Simpler** to configure
- **Good enough** for many use cases

Follow the same LoRA configuration steps as Method 1.

## Advanced Techniques

### Multi-Angle Character Animation

To animate from different angles:

1. **Generate front view**: Use front-facing reference
2. **Generate side view**: Use side profile reference
3. **Generate 3/4 view**: Use angled reference

Keep prompts consistent except for angle descriptions.

### Training Custom Character LoRAs

For perfect character consistency, train your own LoRA:

1. **Gather dataset**: 10-20 images of character from different angles
2. **Preprocess images**: Crop, resize, caption
3. **Train LoRA**: Use LoRA training tools
4. **Test and iterate**: Adjust training parameters

**Recommended tools:**
- kohya_ss scripts
- LoRA training extensions
- Captioning tools

### Combining Multiple LoRAs

Stack LoRAs for enhanced results:

```
LoRA 1: Character Consistency (0.85)
LoRA 2: Style (anime/realistic) (0.7)
LoRA 3: Motion Enhancement (0.6)
```

Use `advanced_variations.json` workflow for multiple LoRAs.

## Common Issues and Solutions

### Face Morphing

**Problem**: Character's face changes between frames

**Solutions:**
- Increase LoRA strength to 0.9-1.0
- Increase CFG scale to 7.5-8.0
- Use more detailed face description in prompt
- Increase steps to 35-40

### Clothing Changes

**Problem**: Outfit shifts or changes color

**Solutions:**
- Add specific clothing details to prompt
- Increase character consistency LoRA strength
- Use reference image with clear clothing
- Add "consistent clothing" to positive prompt

### Over-Rigidity

**Problem**: Motion looks stiff or unnatural

**Solutions:**
- Decrease LoRA strength to 0.7-0.8
- Lower CFG scale to 6.0-6.5
- Reduce ControlNet strength if used
- Add motion-related terms to prompt

### Background Interference

**Problem**: Background elements merge with character

**Solutions:**
- Use reference image with simple background
- Add background description to prompt
- Increase IPAdapter weight for character focus
- Edit background from reference image

## Best Practices

### Reference Image Selection

✅ **Good references:**
- Studio-style portraits
- Clear character art
- Professional photography
- Clean backgrounds
- Good lighting

❌ **Avoid:**
- Group photos (multiple people)
- Extreme angles
- Heavy filters or effects
- Busy backgrounds
- Low resolution images

### Prompt Engineering

**DO:**
- Describe character completely
- Specify consistent features
- Include clothing details
- Mention motion clearly

**DON'T:**
- Use vague descriptions
- Contradict visual features
- Over-complicate prompts
- Ignore character details

### Workflow Optimization

1. **Test with preview settings** (lower steps/resolution)
2. **Iterate on prompt** before final render
3. **Save successful parameters** for reuse
4. **Document what works** for your character

## Example Workflows

### Anime Character Walk Cycle

```yaml
Reference: Anime character portrait
LoRA: character_consistency (0.85) + anime_style (0.7)
Prompt: "Anime character with [features] walking forward, smooth motion, 
        consistent appearance"
Steps: 30
CFG: 7.0
```

### Realistic Portrait Animation

```yaml
Reference: Professional headshot
LoRA: character_consistency (0.9) + realistic_style (0.8)
Prompt: "Realistic portrait of [person], subtle head movement, 
        natural expression, photorealistic"
Steps: 35
CFG: 7.5
```

### Fantasy Character Action

```yaml
Reference: Fantasy character design
LoRA: character_consistency (0.85) + fantasy_style (0.7)
Prompt: "[Fantasy character] casting spell with flowing movements, 
        magical effects, consistent character design"
Steps: 35
CFG: 7.0
```

## Batch Processing Multiple Characters

Use `workflow_loader.py` to process multiple characters:

```python
# Create character_list.txt with character names and references
# Run batch processing script
python scripts/batch_process.py --workflow character_consistent
```

## Quality Checklist

Before final render, verify:
- [ ] Reference image is high quality
- [ ] Character LoRA is loaded correctly
- [ ] Prompt includes all character details
- [ ] LoRA strength is optimized (tested)
- [ ] Sampling settings match use case
- [ ] Negative prompt includes consistency terms
- [ ] Output resolution matches needs

## Next Steps

- Explore [style_transfer.md](style_transfer.md) for artistic variations
- Review [advanced usage](../README.md#advanced-usage) in main README
- Join community to share character animations

Happy character animating! 🎭
