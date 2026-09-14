"""Offline authentication checks for the Homework 2 endpoints."""

from __future__ import annotations

import asyncio

import pytest
from fastapi import HTTPException


def _isolated_server(monkeypatch: pytest.MonkeyPatch, tmp_path):
    from server import app as server_app

    monkeypatch.setattr(server_app, "_SESSIONS", {})
    monkeypatch.setattr(server_app, "SESSIONS_DB", tmp_path / "sessions.db")
    return server_app


def test_create_session_rejects_role_different_from_database(
    world, monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    server_app = _isolated_server(monkeypatch, tmp_path)

    with pytest.raises(HTTPException) as exc_info:
        server_app.create_session(
            server_app.SessionCreate(user_id=9002, role="shopper")
        )

    assert exc_info.value.status_code == 403
    assert server_app._SESSIONS == {}


def test_token_cannot_authorize_a_different_session(
    world, monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    server_app = _isolated_server(monkeypatch, tmp_path)
    session = server_app.create_session(
        server_app.SessionCreate(user_id=1, role="shopper")
    )
    other_session = server_app.create_session(
        server_app.SessionCreate(user_id=1, role="shopper")
    )
    assert other_session["session_id"] != session["session_id"]

    def unexpected_agent_build(*args, **kwargs):
        pytest.fail("an unauthorized request must not build the agent")

    class NoModelRun:
        @staticmethod
        async def run(*args, **kwargs):
            pytest.fail("an unauthorized request must not run the agent")

    monkeypatch.setattr(server_app, "build_agent", unexpected_agent_build)
    monkeypatch.setattr(server_app, "Runner", NoModelRun)

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            server_app.post_message(
                other_session["session_id"],
                server_app.MessageIn(message="Show my recent orders."),
                authorization=f"Bearer {session['token']}",
            )
        )

    assert exc_info.value.status_code == 403


def test_litellm_generation_span_records_usage_and_output(monkeypatch) -> None:
    """Record LiteLLM data through the installed app instrumentation."""
    import json

    from agents.tracing import generation_span, trace
    from agents.tracing.provider import DefaultTraceProvider
    from agents.tracing.setup import get_trace_provider, set_trace_provider
    from opentelemetry.instrumentation.openai_agents import OpenAIAgentsInstrumentor
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
    from observability import instrument

    previous_provider = get_trace_provider()
    agents_provider = DefaultTraceProvider()
    otel_provider = TracerProvider()
    exporter = InMemorySpanExporter()
    otel_provider.add_span_processor(SimpleSpanProcessor(exporter))
    monkeypatch.setenv("TRACELOOP_TRACE_CONTENT", "true")
    monkeypatch.setattr(instrument, "_genai_instrumented", False)
    set_trace_provider(agents_provider)
    try:
        instrument.instrument_genai(otel_provider)
        with trace("offline-generation"):
            with generation_span(
                input=[],
                output=[{"role": "assistant", "content": "Hello"}],
                model="openrouter/openai/gpt-5.5",
                usage={"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
            ):
                pass
        spans = exporter.get_finished_spans()
    finally:
        instrumentor = OpenAIAgentsInstrumentor()
        if instrumentor.is_instrumented_by_opentelemetry:
            instrumentor.uninstrument()
        set_trace_provider(previous_provider)
        agents_provider.shutdown()
        otel_provider.shutdown()

    generation = next(span for span in spans if span.name == "openai.response")
    assert generation.attributes["gen_ai.usage.input_tokens"] == 10
    assert generation.attributes["gen_ai.usage.output_tokens"] == 5
    assert generation.attributes["gen_ai.usage.total_tokens"] == 15
    assert json.loads(str(generation.attributes["gen_ai.output.messages"])) == [
        {
            "role": "assistant",
            "parts": [{"type": "text", "content": "Hello"}],
        }
    ]
