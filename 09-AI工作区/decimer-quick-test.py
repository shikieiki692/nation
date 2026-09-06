# -*- coding: utf-8 -*-
"""Quick DECIMER test - import and run on 5 images"""
import os, sys, time, json
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

VAULT = r"C:\Obsidion\妙妙屋"
MEDIA = os.path.join(VAULT, "media")
OUTPUT = os.path.join(VAULT, "09-AI工作区", "decimer-test-results")
os.makedirs(OUTPUT, exist_ok=True)

# Test with 5 diverse images first
TESTS = [
    ("ethane-conformations.png", "conformation"),
    ("chiral-center.png", "stereochemistry"),
    ("cyclohexane-chair.png", "conformation"),
    ("amino-acid-zwitterions.png", "biomolecule"),
    ("eas-mechanism.png", "mechanism"),
]

print("=" * 60)
print("  DECIMER OCSR Quick Test (5 images)")
print("=" * 60)

print("\n[1] Loading DECIMER model (first run downloads ~570MB)...")
t0 = time.time()
try:
    from DECIMER import predict_SMILES
    print(f"  OK - model loaded in {time.time()-t0:.1f}s")
except Exception as e:
    print(f"  FAIL: {e}")
    sys.exit(1)

print("\n[2] Loading RDKit...")
try:
    from rdkit import Chem
    from rdkit.Chem import Draw, AllChem, Descriptors
    print("  OK")
except:
    print("  SKIP - RDKit not available")

print("\n[3] Running predictions...\n")

results = []
for fname, category in TESTS:
    fpath = os.path.join(MEDIA, fname)
    if not os.path.exists(fpath):
        print(f"  [{fname}] NOT FOUND")
        continue

    t1 = time.time()
    try:
        smiles = predict_SMILES(fpath)
    except Exception as e:
        print(f"  [{fname}] ERROR: {e}")
        results.append({"file": fname, "status": "error", "error": str(e)})
        continue
    elapsed = time.time() - t1

    rdkit_ok = False
    mw = None
    natoms = None
    canonical = None
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            rdkit_ok = True
            canonical = Chem.MolToSmiles(mol)
            mw = round(Descriptors.MolWt(mol), 1)
            natoms = mol.GetNumAtoms()
    except:
        pass

    icon = "OK" if rdkit_ok else "WARN"
    print(f"  [{icon}] {fname}")
    print(f"       SMILES: {smiles}")
    print(f"       MW={mw}  atoms={natoms}  time={elapsed:.2f}s")
    if canonical and canonical != smiles:
        print(f"       canonical: {canonical}")
    print()

    results.append({
        "file": fname, "status": "ok", "smiles": smiles,
        "canonical": canonical, "rdkit_valid": rdkit_ok,
        "mw": mw, "natoms": natoms, "time_s": round(elapsed, 3),
        "category": category,
    })

# Save results
json_path = os.path.join(OUTPUT, "decimer-quick-test.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Summary
ok = sum(1 for r in results if r.get("rdkit_valid"))
total = len(results)
print("=" * 60)
print(f"  SUMMARY: {ok}/{total} images => valid SMILES")
print(f"  Results saved to: 09-AI-workspace/decimer-test-results/")
print("=" * 60)
