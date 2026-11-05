"""Regression: medical symptoms must not automatically trigger self-harm text."""
from types import SimpleNamespace
from unittest.mock import patch
from fastapi.testclient import TestClient
import main
from safety_guardian import SafetyLevel


def test_german_medical_without_explicit_self_harm():
    with (patch('main.assess_message', return_value=SimpleNamespace(level=SafetyLevel.CRISIS, reason='AI uncertainty', requires_professional_help=True)),
          patch('main.assess_crisis_fallback', return_value=SimpleNamespace(explicit_crisis=False))):
        response = TestClient(main.app).post('/chat', json={
            'message':'Ich habe starke Brustschmerzen und bekomme schlecht Luft.',
            'language_mode':'manual','preferred_language':'de'})
    assert response.status_code == 200
    text=response.json()['response']
    assert 'medizinischen Notfall' in text
    assert 'Gegenständen' not in text
