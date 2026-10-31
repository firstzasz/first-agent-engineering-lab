"""Frozen, deterministic S02 operator decision-question recognizer.

This file is HOST/GRADER only. Never expose it or its answers to the contestant.
"""
import re

FROZEN_ANSWERS = {
    "pause_in_progress_run": "An already-running Run continues to its terminal outcome. Pausing does not cancel it.",
    "scheduled_start_while_paused": "A scheduled start occurring while paused is skipped, not queued.",
    "manual_run_while_paused": "An operator may still manually start a Run while a Job is paused.",
    "resume_behavior": "Resuming only allows future scheduled runs; do not catch up missed work.",
}

def _has(text, pattern):
    return re.search(pattern, text, flags=re.I) is not None

def classify(question):
    """Conservatively match distinct, explicitly requested user-owned semantics."""
    if not isinstance(question, str):
        return []
    q = " ".join(question.strip().split()).lower()
    if len(q) < 10 or len(q) > 800:
        return []
    found = []
    if _has(q, r"\bpaus(?:e|ed|ing)?\b") and _has(q, r"\bruns?\b|\battempts?\b|\bexecutions?\b"):
        if _has(q, r"\balready\b|\bin.progress\b|\bin.flight\b|\bcurrently\b|\bongoing\b|\bactive\b|\brunning\b|\bstarted\b"):
            found.append("pause_in_progress_run")
    if _has(q, r"\bpaus(?:e|ed|ing)?\b") and _has(q, r"\bschedul(?:ed|er|ing|e)?\b|\bdue\b|\btrigger\b"):
        if _has(q, r"\bstart\b|\bfire\b|\boccur\b|\bduring\b|\bwhile\b|\bmiss(?:ed)?\b|\bqueue\b|\bskip\b|\bhappen\b|\ballow\b|\bblock\b"):
            found.append("scheduled_start_while_paused")
    if _has(q, r"\bpaus(?:e|ed|ing)?\b") and _has(q, r"\bmanual(?:ly)?\b") and _has(q, r"\brun\b|\bstart\b|\btrigger\b|\bexecute\b"):
        found.append("manual_run_while_paused")
    if _has(q, r"\bresum(?:e|ed|ing)?\b|\bunpaus(?:e|ed|ing)?\b") and _has(q, r"\bcatch.?up\b|\bmiss(?:ed)?\b|\bbacklog\b|\bqueue\b|\bschedul(?:e|ed|er|ing)?\b|\bskip(?:ped)?\b|\bprevious\b|\bpast\b|\bmake.?up\b"):
        found.append("resume_behavior")
    return found

def respond(questions):
    """Answer only specific decision questions, never volunteer another policy."""
    if not isinstance(questions, list) or not (1 <= len(questions) <= 8):
        return {"ok": False, "error": "QUESTIONS_MUST_BE_ARRAY_LENGTH_1_TO_8"}, []
    feedback = []
    events = []
    for question in questions:
        if not isinstance(question, str) or len(question) > 800:
            return {"ok": False, "error": "INVALID_QUESTION"}, []
        ids = classify(question)
        events.append({"question": question, "matched": ids})
        feedback.append({
            "question": question,
            "classification": "PRODUCT_POLICY" if ids else "UNCLASSIFIED",
            "answers": [{"topic": k, "answer": FROZEN_ANSWERS[k]} for k in ids],
            "notice": "No additional product policy was provided." if ids else
                      "Question was not recognized as a precise unresolved product policy. Inspect workspace facts autonomously, or ask a more specific product decision.",
        })
    return {"ok": True, "responses": feedback}, events
