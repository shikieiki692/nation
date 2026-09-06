import importlib.util
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.argv = ["build_module_book.py", "--strict"]
spec = importlib.util.spec_from_file_location(
    "bmb", os.path.join(os.path.dirname(__file__), "build_module_book.py")
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

for module in ("结构化学", "化学原理", "有机化学", "元素与分析"):
    pool = m.gather_questions(module)
    empty = []
    for it in pool:
        q, a = m.split_question_answer(it["body"])
        q = m.clean_section_text(q)
        a = m.clean_section_text(a)
        q = m.strip_teaching_blocks(q)
        a = m.strip_teaching_blocks(a)
        if not a.strip():
            empty.append((it.get("path", "?"), it.get("submodule", "?"), q[:160]))
    print(f"{module}: pool={len(pool)} empty_answers={len(empty)}")
    for rel, sub, head in empty:
        print(f"  {rel} | {sub} | {head}")
