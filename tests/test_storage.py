import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

import storage


class StorageTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"
        self.path_patcher = patch.object(
            storage, "get_db_path", return_value=self.db_path
        )
        self.path_patcher.start()

    def tearDown(self):
        self.path_patcher.stop()
        self.temp_dir.cleanup()

    def test_database_initializes_automatically(self):
        self.assertFalse(self.db_path.exists())
        projects = storage.list_projects()
        self.assertEqual(projects, [])
        self.assertTrue(self.db_path.exists())

    def test_add_and_list_project(self):
        project_id = storage.add_project("Test Project", "Testing")
        projects = storage.list_projects()

        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]["id"], project_id)
        self.assertEqual(projects[0]["name"], "Test Project")

    def test_add_task(self):
        project_id = storage.add_project("Test Project")
        task_id = storage.add_task(project_id, "Write tests")

        tasks = storage.list_tasks(project_id)

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], task_id)

    def test_update_task(self):
        project_id = storage.add_project("Test Project")
        task_id = storage.add_task(project_id, "Write tests")

        storage.update_task(task_id, "completed")

        self.assertEqual(
            storage.list_tasks(project_id)[0]["status"],
            "completed"
        )

    def test_add_checkpoint(self):
        project_id = storage.add_project("Test Project")
        storage.add_checkpoint(project_id, "First milestone completed")

        checkpoint = storage.latest_checkpoint(project_id)

        self.assertEqual(
            checkpoint["summary"],
            "First milestone completed"
        )

    def test_get_project_context(self):
        project_id = storage.add_project(
            "BuildPilot Test",
            "Testing retrieval"
        )

        storage.add_task(project_id, "Build retrieval feature")
        storage.add_checkpoint(
            project_id,
            "Retrieval feature implemented"
        )

        context = storage.get_project_context(project_id)

        self.assertEqual(context["project"]["name"], "BuildPilot Test")
        self.assertEqual(len(context["tasks"]), 1)
        self.assertEqual(
            context["latest_checkpoint"]["summary"],
            "Retrieval feature implemented"
        )

    def test_get_missing_project_context(self):
        with self.assertRaises(ValueError):
            storage.get_project_context(9999)

    def test_reject_invalid_task_status(self):
        with self.assertRaises(ValueError):
            storage.update_task(1, "invalid")

    def test_reject_empty_project_name(self):
        with self.assertRaises(ValueError):
            storage.add_project("")


if __name__ == "__main__":
    unittest.main()
