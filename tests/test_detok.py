from lab import detok


def test_step_label_shows_split_characters():
    assert detok.step_label({"tok": "�", "text": ""}) == "·"
    assert detok.step_label({"tok": "�", "text": "📿"}) == "📿"
    assert detok.step_label({"tok": " ", "text": " "}) == "␣"
    assert detok.step_label({"tok": " cat"}) == "cat"


def test_pieces_without_tokenizer(monkeypatch):
    monkeypatch.setattr(detok, "_tokenizer", lambda model: None)
    assert detok.pieces("any", [1, 2]) is None
