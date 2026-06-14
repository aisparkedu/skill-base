#!/usr/bin/env python3
"""合并 / 拆分 PDF。原创实现，基于 PyMuPDF(fitz)。

合并: python3 pdf_merge.py merge 输出.pdf a.pdf b.pdf ...
拆分: python3 pdf_merge.py split 输入.pdf 输出前缀 [--every N]
"""
import argparse
import fitz


def merge(out, inputs):
    res = fitz.open()
    for p in inputs:
        with fitz.open(p) as src:
            res.insert_pdf(src)
    res.save(out)
    print(f"✅ 合并 {len(inputs)} 个 → {out}（{res.page_count} 页）")


def split(inp, prefix, every):
    doc = fitz.open(inp)
    n = doc.page_count
    part = 0
    for start in range(0, n, every):
        part += 1
        sub = fitz.open()
        sub.insert_pdf(doc, from_page=start, to_page=min(start + every, n) - 1)
        out = f"{prefix}_{part}.pdf"
        sub.save(out)
        print(f"✅ {out}（第 {start + 1}-{min(start + every, n)} 页）")


def main():
    ap = argparse.ArgumentParser(description="合并/拆分 PDF")
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("merge")
    m.add_argument("output")
    m.add_argument("inputs", nargs="+")
    s = sub.add_parser("split")
    s.add_argument("input")
    s.add_argument("prefix")
    s.add_argument("--every", type=int, default=1)
    args = ap.parse_args()
    if args.cmd == "merge":
        merge(args.output, args.inputs)
    else:
        split(args.input, args.prefix, args.every)


if __name__ == "__main__":
    main()
