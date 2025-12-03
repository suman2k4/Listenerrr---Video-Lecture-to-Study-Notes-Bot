from app.services.transcribe import get_transcriber


def test_mock_transcriber_returns_chunk():
    adapter = get_transcriber()
    chunks = adapter.transcribe("/tmp/audio.mp3")
    assert len(chunks) == 1
    assert "text" in chunks[0]
