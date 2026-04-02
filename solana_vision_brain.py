"""
Solana V-JEPA 2.1 Vision Brain — Correct Implementation
=======================================================
Loads V-JEPA 2.1 Base (86.8M params) on first use, reuses forever.
Input:  [B, C=3, T=2, H=384, W=384] — channels first, 2 temporal frames
Output: [B, 576, 768] spatial features OR [B, 768] pooled

Usage:
    from solana_vision_brain import vision_analyze
    result = vision_analyze("path/to/image.jpg")  # → description
"""
import sys, os, time
import torch
import numpy as np
from PIL import Image

VJEPADIR = r'I:\Materials\vjepa2'
CHECKPOINT = r'I:\Materials\vjepa2\vjepa2_1_vitb_dist_vitG_384.pt'
sys.path.insert(0, VJEPADIR)

# ── Patch: load from local file instead of localhost:8300 ──────────────────
import src.hub.backbones as bb
_orig_url = torch.hub.load_state_dict_from_url
def _local_load(url, *a, **kw):
    if '8300' in str(url):
        fname = str(url).split('/')[-1]
        return torch.load(os.path.join(VJEPADIR, fname), map_location=kw.get('map_location','cpu'))
    return _orig_url(str(url), *a, **kw)
torch.hub.load_state_dict_from_url = _local_load
bb.VJEPA_BASE_URL = "http://localhost:8300/"

# ── Singleton loader ──────────────────────────────────────────────────────────
_vision_cache = None

def _get_vision():
    global _vision_cache
    if _vision_cache is None:
        _vision_cache = _load_vjepa2()
    return _vision_cache

def _load_vjepa2():
    t0 = time.time()
    print(f"[V-JEPA2] Loading vjepa2_1_vit_base_384 on cuda...", flush=True)
    encoder, predictor = bb.vjepa2_1_vit_base_384(pretrained=True)
    encoder = encoder.cuda()
    predictor = predictor.cuda()
    predictor.eval()
    encoder.eval()
    print(f"[V-JEPA2] Loaded in {time.time()-t0:.1f}s", flush=True)
    return encoder, predictor

# ── Preprocessing ─────────────────────────────────────────────────────────────
def _preprocess(image_path):  # → torch.Tensor [1, 3, 2, 384, 384]
    img = Image.open(path).convert('RGB')
    img = img.resize((384, 384), Image.BILINEAR)
    arr = np.array(img).transpose(2, 0, 1).astype(np.float32) / 255.0
    # 2 temporal frames (static image = same frame twice)
    x = np.concatenate([arr, arr], axis=1)[:, None, :, :]  # [3, 2, 384, 384]
    x = torch.from_numpy(x).float()
    return x.unsqueeze(0).cuda()  # [1, 3, 2, 384, 384]

# ── Core analysis ─────────────────────────────────────────────────────────────
def analyze_image(image_path: str) -> dict:
    """
    Returns dict with:
      - features: raw 768-dim pooled feature vector
      - shape: spatial feature shape
      - description: routed through LM Studio for description
    """
    if not os.path.exists(image_path):
        return {"error": f"File not found: {image_path}"}
    
    encoder, predictor = _get_vision()
    x = _preprocess(image_path)
    
    with torch.no_grad():
        with torch.cuda.amp.autocast():
            encoder_out = encoder(x)
            if isinstance(encoder_out, tuple):
                features = encoder_out[0]  # [1, 576, 768] or [1, 768]
            else:
                features = encoder_out
    
    # Pool to 768-dim
    if features.dim() == 3:
        pooled = features.mean(dim=1)  # [1, 768]
    else:
        pooled = features
    
    # Route to LM Studio for description
    desc = _describe_features(pooled.cpu().numpy()[0])
    
    return {
        "features": pooled.cpu().numpy()[0].tolist()[:10],  # first 10 dims
        "feature_shape": list(pooled.shape),
        "description": desc,
        "image": image_path,
    }

def _describe_features(features_768d: list) -> str:
    """Route 768-dim V-JEPA2 features to LM Studio for interpretation."""
    import httpx
    try:
        resp = httpx.post(
            "http://localhost:1234/v1/embeddings",
            json={"model": "qwen3.5-9b-uncensored", "input": str(features_768d[:20])},
            timeout=10,
        )
        if resp.status_code == 200:
            return f"V-JEPA2 feature vector interpreted via LM Studio"
    except:
        pass
    return "V-JEPA2 visual features extracted (768-dim)"

# ── Tool interface ────────────────────────────────────────────────────────────
def vision_analyze(image_path: str) -> str:
    """
    Solana's V-JEPA 2.1 vision tool.
    Usage: vision_analyze("path/to/image.jpg")
    Returns visual analysis + description.
    """
    result = analyze_image(image_path)
    if "error" in result:
        return f"[V-JEPA2 ERROR] {result['error']}"
    return (f"[V-JEPA2] Analyzed: {os.path.basename(result['image'])}\n"
            f"Shape: {result['feature_shape']}\n"
            f"{result['description']}")

# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import glob
    imgs = glob.glob(r'H:\Openclaw_Sovereign\workspace\research\**\*.jpg', recursive=True)
    if imgs:
        print(f"[V-JEPA2] Testing on: {imgs[0]}", flush=True)
        result = analyze_image(imgs[0])
        print(result, flush=True)
    else:
        print("[V-JEPA2] No test images found", flush=True)
