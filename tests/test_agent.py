from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.agent import KnowledgeTriageAgent


def test_rag_returns_citation():
    r = KnowledgeTriageAgent().answer("What is prompt injection?")
    assert r.route == "rag"
    assert r.citations
    assert "Source:" in r.answer


def test_calculator_tool():
    r = KnowledgeTriageAgent().answer("calculate 125 * 0.08")
    assert r.route == "tool:calculator"
    assert "10" in r.answer


def test_source_lookup_tool():
    r = KnowledgeTriageAgent().answer("show source NIST_AI_RMF")
    assert r.route == "tool:source_lookup"
    assert "NIST" in r.answer


def test_policy_tool():
    r = KnowledgeTriageAgent().answer("policy secret")
    assert "API keys" in r.answer


def test_empty_question_rejected():
    import pytest
    with pytest.raises(ValueError):
        KnowledgeTriageAgent().answer("   ")
