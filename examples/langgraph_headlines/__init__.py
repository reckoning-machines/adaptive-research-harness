"""Headline sentiment persistence: an experiment supplied from outside the core.

Everything the team supplies lives in this directory: the setup, the
experiment profile, a deterministic fake provider, a LangGraph researcher
and an evaluator. The core imports none of it. The host freezes this
directory into a bundle and pins every tool module's bytes.
"""
