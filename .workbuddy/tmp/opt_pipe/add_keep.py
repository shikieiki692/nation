# -*- coding: utf-8 -*-
"""把「确认为真图」的被误删图追加到 noise_keep.json（去重、保留原顺序）。"""
import json, os

R = r"C:\Obsidion\妙妙屋"
P = os.path.join(R, ".workbuddy", "tmp", "opt_pipe", "noise_keep.json")

NEW = """
c0ab232a0f4c417bd4b6ab6d18e5c02a4314d059c4ff5c6480a48eafb771c15d.jpg
c1c8f6c039e39d48a2453b71f631f51187f9e431849d4c88d98fd121b7ac4a39.jpg
4ff91afe046f91b81c4ab5fa4e6ff443390380d853ca044452cae452b539e9b0.jpg
fc55dd9d8f546f7ab4be6d9a26ab57454a9f504a368cc286a03892adb8b82bc4.jpg
2ed21d28e62aacace01f12dcd627fe42eab1764803f9d539ad96e9d52d20e822.jpg
3352dff0d9604b0786514ee3757c73b0300f8c0f9e8167ad40fb4738ada61db5.jpg
3ecb6a8a1b7fd32a8dcffe4bfff506f47659c666d694d4a57d056d5d3f3f99c2.jpg
c3a16d55e20bbc48411af16c8bfca79c4d71549a2a41e38722408d600806d605.jpg
e8d0ed8e6bfbc246fe1f9dc7beff72f15ca470e4fd2437f443c9c0d7070d5e38.jpg
938072624ab6464773eb33a640c1c852919bb435bc149468556c23bdcb0af19c.jpg
9321cece39e5f1d8acf6464cdf165c591dcd81d2e91e30f6e2f6971021eea726.jpg
4ab949e194d3574dc965f684f80d294f459269defea582667281bd3bcc5d0c9b.jpg
f21863c46f3febace45df440e74056e9954e862632556b544c3619c74db2bc30.jpg
4cc205f0878ad4885c192eba0b802e3b197c70e50431705d13d8328306514010.jpg
869c6a8e9bd28369f64a4aaa5e6032c69ac0d00f2f8491ba0aff4335d244272e.jpg
""".split()

cur = json.load(open(P, encoding="utf-8"))
before = len(cur)
for n in NEW:
    if n not in cur:
        cur.append(n)
json.dump(cur, open(P, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print("noise_keep: %d → %d 条（新增 %d）" % (before, len(cur), len(cur) - before))
