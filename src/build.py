#!/usr/bin/env python3
"""
data/products.json, data/rate_data.json 을 src/template.html 에 주입해
최종 index.html 을 생성합니다.

사용법:
    python3 src/build.py
(리포지토리 루트에서 실행)
"""
import json
import pathlib
from datetime import datetime, timezone, timedelta

ROOT = pathlib.Path(__file__).resolve().parent.parent

with open(ROOT / "data" / "products.json", encoding="utf-8") as f:
    products = json.load(f)
with open(ROOT / "data" / "rate_data.json", encoding="utf-8") as f:
    rates = json.load(f)

products_json = json.dumps(products, ensure_ascii=False)
rates_json = json.dumps(rates, ensure_ascii=False)

# KST timestamp so two people can compare and confirm they're on the same
# build (helps diagnose stale-browser-cache issues).
kst = timezone(timedelta(hours=9))
build_version = datetime.now(kst).strftime("%Y-%m-%d %H:%M KST")

with open(ROOT / "src" / "template.html", encoding="utf-8") as f:
    html = f.read()

html = html.replace("__PRODUCTS_JSON__", products_json)
html = html.replace("__RATES_JSON__", rates_json)
html = html.replace("__BUILD_VERSION__", build_version)

out_path = ROOT / "index.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"generated {out_path} ({len(html)} chars)")
