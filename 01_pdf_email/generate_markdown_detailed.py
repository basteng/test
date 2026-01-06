#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成详细Markdown文件 - 专家和院系介绍
基于expert_info JSON文件生成详细的专家介绍Markdown
"""

import os
import sys
import json
from collections import defaultdict
from datetime import datetime

def generate_detailed_markdown(json_file, output_file=None):
    """生成详细的Markdown文件"""

    if not os.path.exists(json_file):
        print(f"错误：文件不存在 - {json_file}")
        print("\n提示：请先运行 search_experts.py 生成JSON文件")
        return False

    print("="*80)
    print("详细Markdown生成工具")
    print("="*80)
    print(f"\n正在读取专家信息: {json_file}")

    # 读取JSON文件
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            expert_info = json.load(f)
    except Exception as e:
        print(f"错误：无法读取JSON文件 - {str(e)}")
        return False

    print(f"读取到 {len(expert_info)} 个专家信息")

    # 按机构分组
    print("正在按机构分组...")
    institution_groups = defaultdict(lambda: defaultdict(list))

    for email, info in expert_info.items():
        institution = info.get('institution', 'Unknown Institution')
        department = info.get('department', 'General')

        institution_groups[institution][department].append(info)

    print(f"找到 {len(institution_groups)} 个机构")

    # 生成Markdown内容
    print("正在生成Markdown...")
    markdown_lines = []

    # 文件头
    markdown_lines.append("# 专家详细介绍")
    markdown_lines.append("")
    markdown_lines.append(f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    markdown_lines.append(f"**数据源:** {json_file}")
    markdown_lines.append("")

    # 统计信息
    total_experts = len(expert_info)
    verified_count = sum(1 for info in expert_info.values() if info.get('verified'))
    high_confidence = sum(1 for info in expert_info.values() if info.get('confidence') == 'high')

    markdown_lines.append("**统计信息:**")
    markdown_lines.append(f"- 专家总数: {total_experts}")
    markdown_lines.append(f"- 已验证: {verified_count}")
    markdown_lines.append(f"- 高可信度: {high_confidence}")
    markdown_lines.append(f"- 待补充: {total_experts - high_confidence}")
    markdown_lines.append("")
    markdown_lines.append("---")
    markdown_lines.append("")

    # 按机构排序
    sorted_institutions = sorted(institution_groups.items())

    # 为每个机构生成章节
    for institution, departments in sorted_institutions:
        # 一级标题：机构
        markdown_lines.append(f"# {institution}")
        markdown_lines.append("")

        # 计算该机构的专家数
        total_in_inst = sum(len(experts) for experts in departments.values())
        markdown_lines.append(f"**该机构专家数:** {total_in_inst}")
        markdown_lines.append("")

        # 按院系排序
        sorted_departments = sorted(departments.items())

        for department, experts in sorted_departments:
            # 二级标题：院系
            markdown_lines.append(f"## {department}")
            markdown_lines.append("")

            # 为每个专家生成详细信息
            for expert in experts:
                name = expert.get('name', 'Unknown')
                email = expert.get('email', '')
                title = expert.get('title', '')
                research_areas = expert.get('research_areas', [])
                research_interests = expert.get('research_interests', '')
                h_index = expert.get('h_index')
                pub_count = expert.get('publication_count', 0)
                first_file = expert.get('first_file', '')
                serial = expert.get('serial_number', '')
                confidence = expert.get('confidence', 'low')
                verified = expert.get('verified', False)

                # 三级标题：专家姓名
                status_icon = "✓" if verified else ("?" if confidence == 'low' else "~")
                markdown_lines.append(f"### {status_icon} {name}")
                markdown_lines.append("")

                # 基本信息
                markdown_lines.append(f"**Email:** {email}  ")
                if title and title != "待填写":
                    markdown_lines.append(f"**Title:** {title}  ")
                markdown_lines.append(f"**Department:** {department}  ")

                # 如果信息未完善，标注
                if confidence == 'low':
                    markdown_lines.append(f"**Status:** ⚠️ 信息待补充  ")
                elif not verified:
                    markdown_lines.append(f"**Status:** ~ 信息待验证  ")

                markdown_lines.append("")

                # 研究领域
                if research_areas:
                    markdown_lines.append(f"**Research Areas:**")
                    for area in research_areas:
                        markdown_lines.append(f"- {area}")
                    markdown_lines.append("")

                # 研究兴趣描述
                if research_interests and research_interests != "待填写":
                    markdown_lines.append(f"**Research Interests:**")
                    markdown_lines.append(f"{research_interests}")
                    markdown_lines.append("")

                # 学术指标
                if h_index is not None or pub_count:
                    markdown_lines.append(f"**Academic Metrics:**")
                    if h_index:
                        markdown_lines.append(f"- h-index: {h_index}")
                    if pub_count:
                        markdown_lines.append(f"- Publications in Dataset: {pub_count}篇")
                    markdown_lines.append("")

                # 数据集中的出版物
                markdown_lines.append(f"**Publications in Dataset:** {pub_count}篇文献")
                if first_file:
                    markdown_lines.append(f"- 首次出现: {first_file} (序号: {serial})")
                markdown_lines.append("")

                # 链接
                website = expert.get('personal_website', '')
                scholar = expert.get('google_scholar', '')
                if website or scholar:
                    markdown_lines.append(f"**Links:**")
                    if website:
                        markdown_lines.append(f"- [Personal Website]({website})")
                    if scholar:
                        markdown_lines.append(f"- [Google Scholar]({scholar})")
                    markdown_lines.append("")

                markdown_lines.append("---")
                markdown_lines.append("")

            markdown_lines.append("")

    # 保存Markdown文件
    if output_file is None:
        output_file = "PDF_Email提取报告_专家详细介绍.md"

    print(f"\n正在保存文件: {output_file}")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_lines))

        print("✓ Markdown文件生成成功！")
        print("="*80)
        print(f"\n文件详情:")
        print(f"  输出文件: {output_file}")
        print(f"  机构数: {len(institution_groups)}")
        print(f"  专家总数: {total_experts}")
        print(f"  已验证: {verified_count}")
        print(f"  待补充: {total_experts - high_confidence}")

        return True

    except Exception as e:
        print(f"错误：无法保存Markdown文件 - {str(e)}")
        return False

def main():
    """主函数"""
    print("="*80)
    print("详细Markdown生成工具")
    print("="*80)
    print()

    # 确定输入文件
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = "expert_info_template.json"
        if not os.path.exists(json_file):
            # 尝试查找其他JSON文件
            json_file = "expert_info.json"
            if not os.path.exists(json_file):
                print("使用方法:")
                print("  python generate_markdown_detailed.py [JSON文件路径]")
                print()
                print("示例:")
                print("  python generate_markdown_detailed.py expert_info.json")
                print()
                print("错误：当前目录未找到专家信息JSON文件")
                print("请先运行 search_experts.py 生成JSON文件")
                return

    # 生成Markdown
    success = generate_detailed_markdown(json_file)

    if success:
        print("\n✓ 处理完成！")

if __name__ == "__main__":
    main()
