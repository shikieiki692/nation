#!/usr/bin/env python3
import os
import re
import random
import difflib
from pathlib import Path
import yaml
from datetime import datetime

def parse_frontmatter(content):
    """解析Markdown文件的frontmatter"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        frontmatter_yaml = match.group(1)
        try:
            return yaml.safe_load(frontmatter_yaml)
        except:
            data = {}
            for line in frontmatter_yaml.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if value.startswith('[') and value.endswith(']'):
                        value = [v.strip().strip('"\'') for v in value[1:-1].split(',')]
                    data[key] = value
            return data
    return {}

def extract_answer(content):
    """提取## 参考答案之后的所有内容"""
    match = re.search(r'## 参考答案\s*\n(.*)', content, re.DOTALL)
    if match:
        answer = match.group(1).strip()
        # 移除开头的引用块标记
        answer = re.sub(r'^>\s*', '', answer, flags=re.MULTILINE)
        # 移除“原书解答”行
        answer = re.sub(r'^\*\*原书解答.*\*\*\s*\n', '', answer, flags=re.MULTILINE)
        return answer.strip()
    return ''

def find_answer_in_source(source_content, problem_id):
    """在原始OCR文件中查找指定题号的答案"""
    lines = source_content.split('\n')
    start_index = -1
    for i, line in enumerate(lines):
        if re.match(r'^#{1,4}\s*【', line) and re.search(r'【\s*' + re.escape(problem_id) + r'\s*】', line):
            start_index = i
            break
    
    if start_index == -1:
        return ''
    
    end_index = len(lines)
    for i in range(start_index + 1, len(lines)):
        if re.match(r'^#{1,4}\s*【', lines[i]):
            end_index = i
            break
    
    section = '\n'.join(lines[start_index:end_index]).strip()
    
    # 提取解之后的内容
    answer_match = re.search(r'\*\*解\*\*\s*\n(.*?)(?=\n\*\*【评注】\*\*|\n#{1,4}\s*【|\Z)', section, re.DOTALL)
    if not answer_match:
        answer_match = re.search(r'解\s*\n(.*?)(?=\n\*\*【评注】\*\*|\n#{1,4}\s*【|\Z)', section, re.DOTALL)
    if answer_match:
        return answer_match.group(1).strip()
    return section

def normalize_text(text):
    """标准化文本，用于比较"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def compare_answers(question_answer, source_answer):
    """比较两个答案的内容一致性"""
    # 标准化
    norm_question = normalize_text(question_answer)
    norm_source = normalize_text(source_answer)
    
    # 计算相似度
    similarity = difflib.SequenceMatcher(None, norm_question, norm_source).ratio()
    
    # 提取关键内容（移除公式、图片等）
    def extract_key_content(text):
        # 移除公式
        text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
        text = re.sub(r'\$.*?\$', '', text)
        # 移除图片引用
        text = re.sub(r'!\[\[.*?\]\]', '', text)
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    key_question = extract_key_content(question_answer)
    key_source = extract_key_content(source_answer)
    
    # 关键内容相似度
    key_similarity = difflib.SequenceMatcher(None, key_question, key_source).ratio()
    
    return similarity, key_similarity

def main():
    base_dir = Path('C:/Obsidion/妙妙屋')
    question_dir = base_dir / '04-题库' / '教材习题' / '结构化学基础'
    
    # 获取所有题库文件
    question_files = list(question_dir.glob('题-*-结构化学基础-*-习题*.md'))
    print(f"总题库文件数: {len(question_files)}")
    
    # 相似度<10%的题目（从之前报告中获取）
    low_similarity_files = [
        "题-285-结构化学基础-超分子-习题10.21.md",
        "题-001-结构化学基础-量子力学-习题1.1.md",
        "题-262-结构化学基础-离子化合物-习题9.20.md",
        "题-106-结构化学基础-对称性-习题4.24.md",
        "题-014-结构化学基础-量子力学-习题1.14.md",
        "题-099-结构化学基础-对称性-习题4.17.md",
        "题-089-结构化学基础-对称性-习题4.7.md",
        "题-097-结构化学基础-对称性-习题4.15.md",
        "题-104-结构化学基础-对称性-习题4.22.md",
        "题-088-结构化学基础-对称性-习题4.6.md",
        "题-243-结构化学基础-离子化合物-习题9.1.md"
    ]
    
    # 随机抽取20个题目（排除已包含的低相似度题目）
    remaining_files = [f for f in question_files if f.name not in low_similarity_files]
    random.seed(42)  # 固定随机种子，确保可重复
    random_files = random.sample(remaining_files, min(20, len(remaining_files)))
    
    # 合并验证列表
    validation_files = []
    for filename in low_similarity_files:
        filepath = question_dir / filename
        if filepath.exists():
            validation_files.append(filepath)
    
    validation_files.extend(random_files)
    
    # 去重
    validation_files = list(set(validation_files))
    
    print(f"验证题目数: {len(validation_files)}")
    
    results = []
    
    for q_file in validation_files:
        try:
            content = q_file.read_text(encoding='utf-8')
            frontmatter = parse_frontmatter(content)
            
            # 提取题号
            filename = q_file.stem
            match = re.search(r'题-(\d+)-结构化学基础-.*?-(习题\d+\.\d+)', filename)
            if not match:
                continue
            problem_id = match.group(2).replace('习题', '')
            
            # 提取题库答案
            answer_in_question = extract_answer(content)
            
            # 获取source_file
            source_file = frontmatter.get('source_file', '')
            if not source_file:
                results.append({
                    'file': q_file.name,
                    'problem_id': problem_id,
                    'status': '缺少source_file',
                    'similarity': 0,
                    'key_similarity': 0,
                    'question_len': len(answer_in_question),
                    'source_len': 0,
                    'issue': '缺少source_file字段'
                })
                continue
            
            source_path = base_dir / source_file
            if not source_path.exists():
                results.append({
                    'file': q_file.name,
                    'problem_id': problem_id,
                    'status': 'source_file不存在',
                    'similarity': 0,
                    'key_similarity': 0,
                    'question_len': len(answer_in_question),
                    'source_len': 0,
                    'issue': f'source_file不存在: {source_file}'
                })
                continue
            
            source_content = source_path.read_text(encoding='utf-8')
            answer_in_source = find_answer_in_source(source_content, problem_id)
            
            if not answer_in_source:
                results.append({
                    'file': q_file.name,
                    'problem_id': problem_id,
                    'status': '未找到原始答案',
                    'similarity': 0,
                    'key_similarity': 0,
                    'question_len': len(answer_in_question),
                    'source_len': 0,
                    'issue': '在source_file中未找到对应题号的答案'
                })
                continue
            
            # 比较答案
            similarity, key_similarity = compare_answers(answer_in_question, answer_in_source)
            
            # 判断问题类型
            if key_similarity < 0.3:
                status = '内容差异（关键内容不一致）'
            elif similarity < 0.5:
                status = '格式差异（内容一致，格式不同）'
            else:
                status = '基本一致'
            
            results.append({
                'file': q_file.name,
                'problem_id': problem_id,
                'status': status,
                'similarity': similarity,
                'key_similarity': key_similarity,
                'question_len': len(answer_in_question),
                'source_len': len(answer_in_source),
                'issue': ''
            })
            
        except Exception as e:
            results.append({
                'file': q_file.name,
                'problem_id': '未知',
                'status': '处理出错',
                'similarity': 0,
                'key_similarity': 0,
                'question_len': 0,
                'source_len': 0,
                'issue': str(e)
            })
    
    # 统计结果
    content_diff = [r for r in results if '内容差异' in r['status']]
    format_diff = [r for r in results if '格式差异' in r['status']]
    consistent = [r for r in results if '基本一致' in r['status']]
    
    print(f"\n验证结果统计:")
    print(f"内容差异数: {len(content_diff)}")
    print(f"格式差异数: {len(format_diff)}")
    print(f"基本一致数: {len(consistent)}")
    
    # 生成报告
    report_path = base_dir / '09-审计报告' / '2026-08-27-随机抽查验证报告.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('# 题库答案随机抽查验证报告\n\n')
        f.write(f'验证时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}\n')
        f.write(f'验证题目数: {len(validation_files)}\n')
        f.write(f'内容差异数: {len(content_diff)}\n')
        f.write(f'格式差异数: {len(format_diff)}\n')
        f.write(f'基本一致数: {len(consistent)}\n\n')
        
        if content_diff:
            f.write('## 内容差异题目（需人工核查）\n\n')
            f.write('| 文件 | 题号 | 关键内容相似度 | 整体相似度 | 问题 |\n')
            f.write('|------|------|----------------|------------|------|\n')
            for item in content_diff:
                f.write(f"| {item['file']} | {item['problem_id']} | {item['key_similarity']:.2%} | {item['similarity']:.2%} | {item['status']} |\n")
            
            f.write('\n### 详细比对\n\n')
            for i, item in enumerate(content_diff):
                f.write(f'#### {i+1}. {item["file"]} (题号: {item["problem_id"]})\n')
                f.write(f'**状态**: {item["status"]}\n')
                f.write(f'**关键内容相似度**: {item["key_similarity"]:.2%}\n')
                f.write(f'**整体相似度**: {item["similarity"]:.2%}\n\n')
                f.write('---\n\n')
        else:
            f.write('## 未发现内容差异题目\n\n')
            f.write('所有验证题目的关键内容相似度均≥30%，无内容差异。\n\n')
        
        f.write('## 验证明细\n\n')
        f.write('| 文件 | 题号 | 状态 | 关键内容相似度 | 整体相似度 | 题库答案长度 | 原始答案长度 |\n')
        f.write('|------|------|------|----------------|------------|--------------|--------------|\n')
        for item in results:
            f.write(f"| {item['file']} | {item['problem_id']} | {item['status']} | {item['key_similarity']:.2%} | {item['similarity']:.2%} | {item['question_len']} | {item['source_len']} |\n")
    
    print(f"验证报告已生成: {report_path}")

if __name__ == '__main__':
    main()