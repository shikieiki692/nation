#!/usr/bin/env python3
import os
import re
import difflib
from pathlib import Path
import yaml  # 如果没有yaml，需要手动解析

def parse_frontmatter(content):
    """解析Markdown文件的frontmatter"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        frontmatter_yaml = match.group(1)
        try:
            return yaml.safe_load(frontmatter_yaml)
        except:
            # 手动解析简单的YAML
            data = {}
            for line in frontmatter_yaml.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    # 处理列表
                    if value.startswith('[') and value.endswith(']'):
                        value = [v.strip().strip('"\'') for v in value[1:-1].split(',')]
                    data[key] = value
            return data
    return {}

def extract_answer(content):
    """提取## 参考答案之后的内容（直到文件结束）"""
    match = re.search(r'## 参考答案\s*\n(.*)', content, re.DOTALL)
    if match:
        answer = match.group(1).strip()
        # 移除开头的引用块标记
        answer = re.sub(r'^>\s*', '', answer, flags=re.MULTILINE)
        # 移除“原书解答”行
        answer = re.sub(r'^\*\*原书解答.*\*\*\s*\n', '', answer, flags=re.MULTILINE)
        # 移除空行
        answer = re.sub(r'\n\s*\n', '\n', answer)
        return answer.strip()
    return ''

def find_answer_in_source(source_content, problem_id):
    """在原始OCR文件中查找指定题号的答案"""
    # 查找包含problem_id的标题行
    # 标题格式：## 【2.1】 或 ### 【1.1】
    lines = source_content.split('\n')
    start_index = -1
    for i, line in enumerate(lines):
        # 检查是否以#开头，并且包含【problem_id】
        if re.match(r'^#{1,4}\s*【', line) and re.search(r'【\s*' + re.escape(problem_id) + r'\s*】', line):
            start_index = i
            break
    
    if start_index == -1:
        return ''
    
    # 找到下一个标题行
    end_index = len(lines)
    for i in range(start_index + 1, len(lines)):
        if re.match(r'^#{1,4}\s*【', lines[i]):
            end_index = i
            break
    
    # 提取这部分内容
    section = '\n'.join(lines[start_index:end_index]).strip()
    
    # 提取解之后的内容
    # 尝试匹配 **解** 或 解
    answer_match = re.search(r'\*\*解\*\*\s*\n(.*?)(?=\n\*\*【评注】\*\*|\n#{1,4}\s*【|\Z)', section, re.DOTALL)
    if not answer_match:
        answer_match = re.search(r'解\s*\n(.*?)(?=\n\*\*【评注】\*\*|\n#{1,4}\s*【|\Z)', section, re.DOTALL)
    if answer_match:
        return answer_match.group(1).strip()
    # 如果找不到解，返回整个部分
    return section

def normalize_text(text):
    """标准化文本，用于比较"""
    # 移除空行、多余空格
    text = re.sub(r'\s+', ' ', text)
    # 移除图片引用
    text = re.sub(r'!\[\[.*?\]\]', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 移除公式标记
    text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
    text = re.sub(r'\$.*?\$', '', text)
    # 移除标题标记
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    return text.strip()

def main():
    base_dir = Path('C:/Obsidion/妙妙屋')
    question_dir = base_dir / '04-题库' / '教材习题' / '结构化学基础'
    
    # 获取所有题库文件
    question_files = list(question_dir.glob('题-*-结构化学基础-*-习题*.md'))
    print(f"找到 {len(question_files)} 个题库文件")
    
    results = []
    
    for q_file in question_files:
        try:
            content = q_file.read_text(encoding='utf-8')
            frontmatter = parse_frontmatter(content)
            
            # 检查是否为高考题（通过exam_stage或tags）
            exam_stage = frontmatter.get('exam_stage', '')
            tags = frontmatter.get('tags', [])
            if '高考' in exam_stage or '高考' in tags:
                continue
            
            # 提取题号
            filename = q_file.stem
            match = re.search(r'题-(\d+)-结构化学基础-.*?-(习题\d+\.\d+)', filename)
            if not match:
                continue
            problem_id = match.group(2)  # 例如：习题1.1 -> 1.1
            # 去掉“习题”前缀
            problem_id = problem_id.replace('习题', '')
            
            # 提取题库答案
            answer_in_question = extract_answer(content)
            
            # 获取source_file
            source_file = frontmatter.get('source_file', '')
            if not source_file:
                results.append({
                    'file': q_file.name,
                    'problem_id': problem_id,
                    'issue': '缺少source_file字段',
                    'similarity': 0,
                    'question_answer': answer_in_question[:200] + '...' if len(answer_in_question) > 200 else answer_in_question,
                    'source_answer': ''
                })
                continue
            
            source_path = base_dir / source_file
            if not source_path.exists():
                results.append({
                    'file': q_file.name,
                    'problem_id': problem_id,
                    'issue': f'source_file不存在: {source_file}',
                    'similarity': 0,
                    'question_answer': answer_in_question[:200] + '...' if len(answer_in_question) > 200 else answer_in_question,
                    'source_answer': ''
                })
                continue
            
            source_content = source_path.read_text(encoding='utf-8')
            answer_in_source = find_answer_in_source(source_content, problem_id)
            
            if not answer_in_source:
                results.append({
                    'file': q_file.name,
                    'problem_id': problem_id,
                    'issue': '在source_file中未找到对应题号的答案',
                    'similarity': 0,
                    'question_answer': answer_in_question[:200] + '...' if len(answer_in_question) > 200 else answer_in_question,
                    'source_answer': ''
                })
                continue
            
            # 标准化文本
            norm_question = normalize_text(answer_in_question)
            norm_source = normalize_text(answer_in_source)
            
            # 计算相似度
            similarity = difflib.SequenceMatcher(None, norm_question, norm_source).ratio()
            
            # 如果相似度低于阈值，记录
            if similarity < 0.8:
                results.append({
                    'file': q_file.name,
                    'problem_id': problem_id,
                    'issue': f'答案相似度过低: {similarity:.2%}',
                    'similarity': similarity,
                    'question_answer': answer_in_question[:500] + '...' if len(answer_in_question) > 500 else answer_in_question,
                    'source_answer': answer_in_source[:500] + '...' if len(answer_in_source) > 500 else answer_in_source
                })
        except Exception as e:
            results.append({
                'file': q_file.name,
                'problem_id': '未知',
                'issue': f'处理出错: {str(e)}',
                'similarity': 0,
                'question_answer': '',
                'source_answer': ''
            })
    
    # 按相似度排序
    results.sort(key=lambda x: x.get('similarity', 0))
    
    # 输出报告
    report_path = base_dir / '09-审计报告' / '2026-08-27-答案比对报告.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('# 题库答案比对报告\n\n')
        f.write(f'比对时间: {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")}\n')
        f.write(f'比对题目数: {len(question_files)}\n')
        f.write(f'发现问题数: {len(results)}\n\n')
        
        if results:
            f.write('## 问题列表\n\n')
            f.write('| 文件 | 题号 | 问题 | 相似度 |\n')
            f.write('|------|------|------|--------|\n')
            for item in results:
                f.write(f"| {item['file']} | {item['problem_id']} | {item['issue']} | {item.get('similarity', 0):.2%} |\n")
            
            f.write('\n## 详细比对（前10个最不相似）\n\n')
            for i, item in enumerate(results[:10]):
                f.write(f'### {i+1}. {item["file"]} (题号: {item["problem_id"]})\n')
                f.write(f'**问题**: {item["issue"]}\n')
                f.write(f'**相似度**: {item.get("similarity", 0):.2%}\n\n')
                f.write('**题库答案**:\n')
                f.write(f'```\n{item["question_answer"]}\n```\n\n')
                f.write('**原始OCR答案**:\n')
                f.write(f'```\n{item["source_answer"]}\n```\n\n')
                f.write('---\n\n')
        else:
            f.write('所有题目答案与原始OCR答案高度一致，未发现明显问题。\n')
    
    print(f"报告已生成: {report_path}")
    print(f"发现问题: {len(results)}")

if __name__ == '__main__':
    main()