# V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning

**Paper:** arXiv:2506.09985 (June 2025)
**Authors:** M. Assran, A. Bardes, D. Fan, Q. Garrido, R. Howes, M. Komeili, M. Muckley, A. Rizvi, C. Roberts, K. Sinha, A. Zholus, S. Arnaud, A. Gejji, A. Martin, F. R. Hogan, D. Dugas, P. Bojanowski, V. Khalidov, P. Labatut, F. Massa, M. Szafraniec, K. Krishnakumar, Y. Li, X. Ma, S. Chandar, F. Meier, Y. LeCun, M. Rabbat, N. Ballas (Meta FAIR)

**Source:** https://arxiv.org/abs/2506.09985

---

## Core Contribution

V-JEPA 2 is a self-supervised video foundation model that learns world understanding from internet-scale video (1M hours) without action labels. It achieves state-of-the-art on motion understanding, action anticipation, and video QA — then can be post-trained with just 62 hours of robot data to enable zero-shot planning on new robot arms.

**Key insight:** Predict in latent space, not pixel space. Ignores unpredictable details (every blade of grass), focuses on predictable aspects (trajectory of motion, object physics).

---

## Architecture

### Two-Stage Training

**Stage 1: Action-Free Pretraining**
- Input: Raw video → patchified into tokens (ViT architecture)
- Mask: Drop a subset of tokens (masked denoising)
- Encoder: Processes masked video sequence
- Predictor: Predicts masked regions in LATENT representation space
- Training data: 1M hours internet video + 1M images

**Stage 2: V-JEPA 2-AC (Action-Conditioned)**
- Freeze pretrained encoder
- Add 300M parameter action-conditioned predictor transformer
- Block-causal attention (autoregressive next-frame prediction)
- Post-train on only 62 hours of Droid robot trajectory data
- Deploy zero-shot on new Franka arms — no robot-specific training needed

### V-JEPA 2.1 Improvements (March 2026)

We have V-JEPA 2.1 checkpoint: `vjepa2_1_vitb_dist_vitG_384.pt` (ViT-B/16, 80M params, 384×384)

1. **Dense Predictive Loss** — ALL tokens contribute to loss, not just masked ones
2. **Deep Self-Supervision** — Loss applied at multiple intermediate layers
3. **Multi-Modal Tokenizers** — Separate tokenizers for images AND videos
4. **Model + Data Scaling** — Bigger models trained on more data

---

## Benchmarks

| Benchmark | V-JEPA 2 | Previous Best |
|-----------|----------|---------------|
| Something-Something v2 (motion) | **77.3%** | 69.7% (InternVideo2-1B) |
| Epic-Kitchens-100 (anticipation) | **39.7 R@5** | ~27% (PlausiVL) |
| Diving48 (fine-grained motion) | **90.2%** | 86.4% |
| PerceptionTest (Video QA) | **84.0%** | — |
| TempCompass (Video QA) | **76.9%** | 75.3% (Tarsier 2) |
| MVP (Video QA) | **44.5%** | 39.9% (InternVL-2.5) |

### Robot Manipulation (V-JEPA 2-AC)

| Task | Octo | Cosmos | V-JEPA 2-AC |
|------|------|--------|-------------|
| Reach | 100% | 80% | **100%** |
| Grasp Cup | 10% | 0% | **60%** |
| Grasp Box | 0% | 20% | **20%** |
| Pick-and-Place Cup | 10% | 0% | **80%** |
| Pick-and-Place Box | 10% | 0% | **50%** |

---

## Relevance to Solana OS

### What V-JEPA 2 Gives Us

1. **Motion understanding** — Classify fine-grained physical interactions from camera feed
2. **Action anticipation** — Predict what will happen next in a scene
3. **World model** — Internal representation of how physical objects behave
4. **Planning capability** — V-JEPA 2-AC shows it can plan actions from visual goals

### The Gap They're Admitting

From their own intro:
> "Humans learn an internal model of the world by integrating low-level sensory inputs to represent and predict future states"

Yet V-JEPA is **purely visual**. They muted audio in training because internet video audio is chaotic. This is a known limitation.

### Marvin's Multi-Sensor Insight

V-JEPA 2 proves the architecture works for visual world modeling. The next step — which Marvin identified 2 years ago — is **multi-sensor fusion**:

| Modality | What It Captures | V-JEPA Gap |
|----------|------------------|------------|
| Vision | Motion, appearance, spatial | ✅ Covered |
| Audio | Material properties, causality, sounds=physics | ❌ Missing |
| Touch | Weight, texture, resistance | ❌ Missing |
| Motor | Agency, consequence | Partially (2-AC) |

**We have AudioMAE in our stack.** The path forward: dual-encode visual + audio tokens through cross-attention fusion.

---

## Files in This Repo

- `I:\Materials\vjepa2\` — Full V-JEPA 2.1 source code + checkpoints
- `vjepa2_1_vitb_dist_vitG_384.pt` — ViT-B/16 checkpoint (80M params, 384×384)

---

## Citation

```bibtex
@article{assran2025vjepa2,
  title={Self-Supervised Video Models Enable Understanding, Prediction and Planning},
  author={Assran, Mahmoud and Bardes, Adrien and Fan, David and others},
  journal={arXiv:2506.09985},
  year={2025}
}
```

---

*Added to Solana OS research: April 5, 2026*
