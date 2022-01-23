import unittest
import os
from unittest import mock

import main
from main import (
    SimpleFindStrategy,
    BufferFindStrategy,
    TODOContext,
    SearchClient
)


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        tests_dir_path = os.path.dirname(os.path.realpath(__file__))
        proj_dir_path = os.path.dirname(tests_dir_path)
        self.test_resources = os.path.join(tests_dir_path, "test_resources")
        self.main_py_file = os.path.join(proj_dir_path, "main.py")

    def test_1_simple_find_strategy_found(self):
        test_file = os.path.join(self.test_resources, "test_dir_1", "test_file.js")
        strategy = SimpleFindStrategy()
        found = strategy.find_word(word="TODO", file_name=test_file)
        assert found is True

    def test_2_buffer_find_strategy_found(self):
        test_file = os.path.join(self.test_resources,
                                 "test_dir_2",
                                 "test_sub_dir_2",
                                 "test_file_2_2.js")
        strategy = BufferFindStrategy()
        found = strategy.find_word(word="TODO", file_name=test_file)
        assert found is True

    def test_3_buffer_find_strategy_not_found(self):
        test_file = os.path.join(self.test_resources,
                                 "test_dir_2",
                                 "test_file_2.js")
        strategy = BufferFindStrategy()
        found = strategy.find_word(word="TODO", file_name=test_file)
        assert found is False

    @mock.patch.dict(os.environ, {"WHITE_LIST_DIRS": "test_ignore_dir"}, clear=True)
    def test_4_search_context(self):
        mock_strategy = mock.Mock()
        mock_strategy.find_word.side_effect = [True, False, True]
        mock_strategy.find_word_concurrent.side_effect = [(True, 'test_file_1.js'),
                                                          (False, 'test_file_2.js'),
                                                          (True, 'test_file_3.js')]

        context = TODOContext(strategy=mock_strategy, start_dir=self.test_resources)
        todo_files = context.find_todo()
        assert len(todo_files) == 2

        todo_files.clear()
        assert len(todo_files) == 0

        todo_files = context.find_todo_concurrent()
        assert len(todo_files) == 2

    def test_5_search_client(self):
        with mock.patch.object(main.TODOContext,
                               'find_todo',
                               mock.MagicMock(side_effect=[
                                   ["test_file_1.js", self.main_py_file]
                               ])):
            client = SearchClient()
            files = client.run()
            assert len(files) == 1

    @mock.patch.dict(os.environ, {"SEARCH_STRATEGY": "random_monkey"}, clear=True)
    def test_err_1_unavailable_strategy(self):
        with self.assertRaises(RuntimeError):
            client = SearchClient()