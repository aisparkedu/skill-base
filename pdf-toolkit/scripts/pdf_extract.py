#!/usr/bin/env python3
"""提取 PDF 文本。原创实现，基于 PyMuPDF(fitz)。

用法: python3 pdf_extract.py 文件.pdf [--pages 1-3 | --pages 2]
"""
import argparse
import fitz


def main():
    ap = argparse.ArgumentParser(description="提取 PDF 文本")
    ap.add_argument("input")
    ap.add_argument("--pages", help="页码范围，如 1-3 或 2（页码从 1 起）")
    args = ap.parse_args()

    doc = fitz.open(args.input)
    start, end = 1, doc.page_count
    if args.pages:
        if '-' in args.pages:
            a, b = args.pages.split('-')
            start, end = int(a), int(b)
        else:
            start = end = int(args.pages)
    end = min(end, doc.page_count)
    for n in range(start, end + 1):
        print(f"\n===== 第 {n} 页 =====")
        print(doc[n - 1].get_text())


if __name__ == "__main__":
    main()
