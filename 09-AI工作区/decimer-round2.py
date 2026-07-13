# -*- coding: utf-8 -*-
"""
DECIMER Round 2: Benchmark + Vault test
Part A: Generate clean structures with RDKit, test DECIMER recognition accuracy
Part B: Test vault images that are close to standard 2D structures
"""
import os, sys, time, json
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

VAULT = r"C:\Obsidion\妙妙屋"
MEDIA = os.path.join(VAULT, "media")
OUTPUT = os.path.join(VAULT, "09-AI工作区", "decimer-test-results")
os.makedirs(OUTPUT, exist_ok=True)

from rdkit import Chem
from rdkit.Chem import Draw, AllChem, Descriptors
from DECIMER import predict_SMILES

print("=" * 70)
print("  DECIMER Round 2: Benchmark + Vault Structure Test")
print("=" * 70)

# ============================================================
# PART A: Generate clean 2D structures with RDKit
# ============================================================
print("\n--- PART A: RDKit-generated benchmark (ideal conditions) ---\n")

benchmark_molecules = [
    ("benzene",         "c1ccccc1"),
    ("toluene",         "Cc1ccccc1"),
    ("phenol",          "Oc1ccccc1"),
    ("aniline",         "Nc1ccccc1"),
    ("acetophenone",    "CC(=O)c1ccccc1"),
    ("benzoic_acid",    "OC(=O)c1ccccc1"),
    ("naphthalene",     "c1ccc2ccccc2c1"),
    ("anthracene",      "c1ccc2cc3ccccc3cc2c1"),
    ("cyclohexane",     "C1CCCCC1"),
    ("cyclohexanone",   "O=C1CCCCC1"),
    ("glucose",         "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O"),
    ("caffeine",        "Cn1c(=O)c2c(ncn2C)n(C)c1=O"),
    ("aspirin",         "CC(=O)Oc1ccccc1C(=O)O"),
    ("ibuprofen",       "CC(C)Cc1ccc(cc1)C(C)C(=O)O"),
    ("cholesterol",     "C[C@H](CCCC(C)C)[C@H]1CC[C@@H]2[C@@]1(CC[C@H]3[C@H]2CC=C4[C@@]3(CCC(C4)O)C)C"),
    ("ATP_simplified",  "c1nc(c2c(n1)ncn2C[C@H]1OC(COP(=O)(O)OP(=O)(O)OP(=O)(O)O)[C@@H](O)[C@@H]1O)N"),
    ("morphine",        "CN1CCC23c4c5ccc(O)c4O[C@H]2[C@@H](O)C=C[C@H]3[C@H]1C5"),
    ("penicillin_G",    "CC1([C@@H](N2[C@H](S1)[C@@H](C2=O)NC(=O)Cc3ccccc3)C(=O)O)C"),
    ("paracetamol",     "CC(=O)Nc1ccc(O)cc1"),
    ("vitamin_C",       "OC[C@H]1OC(=O)C(O)=C1O"),
]

# Save generated images
gen_dir = os.path.join(OUTPUT, "generated-structures")
os.makedirs(gen_dir, exist_ok=True)

benchmark_results = []
for name, smi in benchmark_molecules:
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        print(f"  [SKIP] {name} - invalid SMILES")
        continue

    AllChem.Compute2DCoords(mol)
    img_path = os.path.join(gen_dir, f"{name}.png")
    Draw.MolToFile(mol, img_path, size=(350, 300))

    # Run DECIMER
    t0 = time.time()
    try:
        pred_smiles = predict_SMILES(img_path)
    except Exception as e:
        print(f"  [ERROR] {name}: {e}")
        benchmark_results.append({"name": name, "status": "error", "input_smiles": smi})
        continue
    elapsed = time.time() - t0

    # Validate
    pred_mol = Chem.MolFromSmiles(pred_smiles) if pred_smiles else None
    valid = pred_mol is not None

    # Compare using canonical SMILES
    cano_input = Chem.MolToSmiles(mol) if mol else None
    cano_pred = Chem.MolToSmiles(pred_mol) if pred_mol else None
    exact_match = (cano_input == cano_pred) if cano_input and cano_pred else False

    # Tanimoto similarity using Morgan fingerprints
    tanimoto = None
    if valid:
        from rdkit.Chem import AllChem as AC
        fp1 = AC.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
        fp2 = AC.GetMorganFingerprintAsBitVect(pred_mol, 2, nBits=2048)
        from rdkit.DataStructs import TanimotoSimilarity
        tanimoto = round(TanimotoSimilarity(fp1, fp2), 3)

    icon = "EXACT" if exact_match else ("SIMILAR" if (tanimoto and tanimoto > 0.7) else ("PARTIAL" if valid else "FAIL"))
    mw = round(Descriptors.MolWt(mol), 1)
    print(f"  [{icon:7s}] {name:20s} | tan={tanimoto} | MW={mw:7.1f} | {elapsed:.1f}s")
    if not exact_match and pred_smiles:
        print(f"           input:  {smi}")
        print(f"           pred:   {pred_smiles[:80]}{'...' if len(pred_smiles)>80 else ''}")

    benchmark_results.append({
        "name": name, "input_smiles": smi, "pred_smiles": pred_smiles,
        "valid": valid, "exact_match": exact_match, "tanimoto": tanimoto,
        "mw": mw, "time_s": round(elapsed, 2),
    })

# Benchmark summary
valid_count = sum(1 for r in benchmark_results if r.get("valid"))
exact_count = sum(1 for r in benchmark_results if r.get("exact_match"))
similar_count = sum(1 for r in benchmark_results if r.get("tanimoto") and r["tanimoto"] > 0.7)
total = len(benchmark_results)

print(f"\n  Benchmark Summary: {total} molecules")
print(f"    Valid SMILES:     {valid_count}/{total} ({valid_count/total*100:.0f}%)")
print(f"    Exact match:      {exact_count}/{total} ({exact_count/total*100:.0f}%)")
print(f"    Tanimoto > 0.7:   {similar_count}/{total} ({similar_count/total*100:.0f}%)")

# ============================================================
# PART B: Test vault images closest to standard structures
# ============================================================
print("\n\n--- PART B: Vault images (real-world conditions) ---\n")

vault_tests = [
    ("enantiomer.png",          "2-bromobutane enantiomers (clean bond-line)"),
    ("18-crown-6.png",          "18-crown-6 ether (macrocycle)"),
    ("aromatic-heterocycles.png", "5 heterocycles (multiple molecules)"),
    ("suzuki-cycle.png",        "Suzuki catalytic cycle"),
    ("sn1-coordinate.png",      "SN1 reaction coordinate"),
    ("beckmann-mechanism.png",  "Beckmann rearrangement"),
]

vault_results = []
for fname, desc in vault_tests:
    fpath = os.path.join(MEDIA, fname)
    if not os.path.exists(fpath):
        print(f"  [SKIP] {fname} - not found")
        continue
    # Check if it's actually an image
    if os.path.getsize(fpath) < 100:
        print(f"  [SKIP] {fname} - too small ({os.path.getsize(fpath)} bytes)")
        continue

    t0 = time.time()
    try:
        pred = predict_SMILES(fpath)
    except Exception as e:
        print(f"  [ERROR] {fname}: {e}")
        vault_results.append({"file": fname, "desc": desc, "status": "error"})
        continue
    elapsed = time.time() - t0

    pred_mol = Chem.MolFromSmiles(pred) if pred else None
    valid = pred_mol is not None
    mw = round(Descriptors.MolWt(pred_mol), 1) if pred_mol else None

    icon = "OK" if valid else "WARN"
    print(f"  [{icon}] {fname}")
    print(f"       Desc: {desc}")
    print(f"       SMILES: {pred[:100]}{'...' if len(pred)>100 else ''}")
    if mw:
        print(f"       MW={mw}  valid=True  time={elapsed:.1f}s")
    else:
        print(f"       valid=False  time={elapsed:.1f}s")
    print()

    vault_results.append({
        "file": fname, "desc": desc, "smiles": pred,
        "valid": valid, "mw": mw, "time_s": round(elapsed, 2),
    })

# Save all results
all_results = {"benchmark": benchmark_results, "vault": vault_results}
json_path = os.path.join(OUTPUT, "decimer-round2-results.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

vault_valid = sum(1 for r in vault_results if r.get("valid"))
vault_total = len(vault_results)
print("=" * 70)
print(f"  FINAL SUMMARY")
print(f"  Benchmark (ideal): {exact_count}/{total} exact, {valid_count}/{total} valid")
print(f"  Vault (real):      {vault_valid}/{vault_total} valid SMILES")
print(f"  Results: 09-AI-workspace/decimer-test-results/decimer-round2-results.json")
print("=" * 70)
