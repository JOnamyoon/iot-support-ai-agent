from __future__ import annotations
import ast
import csv
import operator as op
from pathlib import Path
from typing import Dict

ROOT = Path(__file__).resolve().parents[1]

_ALLOWED = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
    ast.Pow: op.pow, ast.USub: op.neg, ast.Mod: op.mod,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression")


def calculator(expression: str) -> float:
    tree = ast.parse(expression, mode="eval")
    return float(_eval(tree.body))


def source_lookup(source_id: str) -> Dict[str, str]:
    with (ROOT / "data" / "sources.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["source_id"].lower() == source_id.lower():
                return row
    raise KeyError(f"Unknown source_id: {source_id}")


def policy_lookup(topic: str) -> str:
    policy = {
        "secret": "Never commit API keys, passwords, access tokens, private company data, or personal information.",
        "citation": "Answers should display source title/URL and separate retrieved evidence from generated text.",
        "feedback": "Store only the minimum feedback needed for evaluation; avoid unnecessary personal data.",
    }
    key = topic.strip().lower()
    for k, v in policy.items():
        if k in key:
            return v
    return "No local policy matched. Try: secret, citation, feedback."
