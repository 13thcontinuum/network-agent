import os
import tempfile
import unittest
from unittest.mock import patch

import analyzer
import database


class DatabaseMemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = os.path.join(self.temp_dir.name, "test.db")
        self.database_name = database.DB_NAME
        database.DB_NAME = self.database_path
        database.init_db()

    def tearDown(self):
        database.DB_NAME = self.database_name
        self.temp_dir.cleanup()

    def test_saves_incidents_and_selects_matching_context(self):
        database.save_incident(
            "2026-10-28",
            "Router interface GigabitEthernet1 is down",
            "The interface lost carrier.",
        )
        database.save_incident(
            "2026-10-28",
            "Switch VLAN 20 is unreachable",
            "Check the access port configuration.",
        )

        memory = database.get_relevant_incidents(
            "GigabitEthernet1 router down"
        )

        self.assertIn("Router interface GigabitEthernet1 is down", memory)
        self.assertNotIn("Switch VLAN 20", memory)

    def test_caps_context_length(self):
        database.save_incident(
            "2026-10-28",
            "Router interface GigabitEthernet1 is down",
            "interface " + ("detail " * 100),
        )

        memory = database.get_relevant_incidents(
            "GigabitEthernet1 router",
            max_chars=100,
        )

        self.assertLessEqual(len(memory), 100)

    def test_returns_message_when_no_incidents_match(self):
        self.assertEqual(
            database.get_relevant_incidents("unknown router issue"),
            "No relevant previous incidents.",
        )


class AnalysisTests(unittest.TestCase):
    @patch.dict(os.environ, {"OLLAMA_MODEL": "test-model"})
    @patch("analyzer.chat")
    def test_uses_shared_model_call_and_returns_analysis(self, mock_chat):
        mock_chat.return_value = {"message": {"content": "Analysis result"}}

        result = analyzer.analyze_network_output(
            "Router output",
            "Previous incident context",
        )

        self.assertEqual(result, "Analysis result")
        mock_chat.assert_called_once()
        call = mock_chat.call_args.kwargs
        self.assertEqual(call["model"], "test-model")
        self.assertIn(
            "Previous incident context",
            call["messages"][0]["content"],
        )
        self.assertEqual(call["messages"][1]["content"], "Router output")


if __name__ == "__main__":
    unittest.main()
