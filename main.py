import os
import sys
import concurrent.futures

from abc import ABC, abstractmethod
from typing import List


class Constants:
    WORD = "TODO"
    UTF8 = "utf-8"
    DEFAULT_WHITE_LIST = ".git,.idea"
    SIMPLE_STRATEGY = "simple"
    BUFFER_STRATEGY = "buffer"
    BUFFER_SIZE = 4096
    MIN_WORKERS = 1


class EnvConfig:
    ENCODING = "ENCODING"
    CHUNK_SIZE = "CHUNK_SIZE"
    SEARCH_STRATEGY = "SEARCH_STRATEGY"
    WHITE_LIST_DIRS = "WHITE_LIST_DIRS"
    CONCURRENCY = "CONCURRENCY"


class SearchStrategy(ABC):  # pragma: no cover
    @abstractmethod
    def find_word(self, word: str, file_name: str) -> bool:
        raise NotImplemented

    def find_word_concurrent(self, word: str, file_name: str) -> (bool, str):
        return self.find_word(word=word, file_name=file_name), file_name


class SimpleFindStrategy(SearchStrategy):
    def __init__(self):
        self._encoding = os.getenv(EnvConfig.ENCODING, Constants.UTF8)

    def find_word(self, word: str, file_name: str) -> bool:
        try:
            with open(file_name, 'r', encoding=self._encoding) as f:
                found = f.read().find(word)
            return False if found < 0 else True
        except UnicodeDecodeError:  # pragma: no cover
            print(f"File [{file_name}] is not {self._encoding} supported.")


class BufferFindStrategy(SearchStrategy):
    def __init__(self):
        self._encoding = os.getenv(EnvConfig.ENCODING, Constants.UTF8)
        self._chunk_size = int(os.getenv(EnvConfig.CHUNK_SIZE, Constants.BUFFER_SIZE))

    def find_word(self, word: str, file_name: str) -> bool:
        found = False
        with open(file_name, 'r', encoding=self._encoding) as f:
            while True:
                content = f.read(self._chunk_size)
                if not content:
                    break
                index = content.find(word)
                if index >= 0:
                    found = True
                    break
        return found


class TODOContext:
    def __init__(self, strategy: SearchStrategy, start_dir: str):
        self._strategy = strategy
        self._white_list_dirs = self._get_white_list_dirs()
        self._list_of_files = self._get_list_of_files(start_dir=start_dir)

    @property
    def strategy(self) -> SearchStrategy:
        return self._strategy

    @staticmethod
    def _get_white_list_dirs():
        env_white_list = str(os.getenv(EnvConfig.WHITE_LIST_DIRS, Constants.DEFAULT_WHITE_LIST))
        if env_white_list:
            return [f.strip() for f in env_white_list.split(",")]

    def _get_list_of_files(self, start_dir: str) -> List[str]:
        file_list = list()
        for dir_path, dir_names, files in os.walk(start_dir):
            for white_list_dir in self._white_list_dirs:
                if white_list_dir in dir_names:
                    dir_names.remove(white_list_dir)
            for file_name in files:
                file_path = os.path.join(dir_path, file_name)
                file_list.append(file_path)
        return file_list

    def find_todo(self) -> List[str]:
        todo_files = []
        for file in self._list_of_files:
            found = self.strategy.find_word(word=Constants.WORD, file_name=file)
            if found:
                todo_files.append(file)
        return todo_files

    def find_todo_concurrent(self) -> List[str]:
        num_of_workers = int(os.getenv(EnvConfig.CONCURRENCY, Constants.MIN_WORKERS))
        todo_files = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_of_workers) as executor:
            futures = []
            for file in self._list_of_files:
                futures.append(executor.submit(self.strategy.find_word_concurrent, word=Constants.WORD, file_name=file))
            for future in concurrent.futures.as_completed(futures):
                found, file_name = future.result()
                if found:
                    todo_files.append(file_name)
        return todo_files


class SearchClient:
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        strategy_name = os.getenv(EnvConfig.SEARCH_STRATEGY, Constants.SIMPLE_STRATEGY)
        if strategy_name.lower() == Constants.BUFFER_STRATEGY:  # pragma: no cover
            strategy = BufferFindStrategy()
        elif strategy_name.lower() == Constants.SIMPLE_STRATEGY:
            strategy = SimpleFindStrategy()
        else:
            print(f"Search strategy {strategy_name} does not exist.")
            raise RuntimeError

        self.context = TODOContext(start_dir=dir_path, strategy=strategy)
        concurrency = os.getenv(EnvConfig.CONCURRENCY, None)
        self.concurrent_mode = True if concurrency else False

    def run(self) -> List[str]:
        if self.concurrent_mode: # pragma: no cover
            files = self.context.find_todo_concurrent()
        else:
            files = self.context.find_todo()

        if __file__ in files:
            files.remove(__file__)

        return files


if __name__ == "__main__":  # pragma: no cover
    client = SearchClient()
    todo_files = client.run()
    print("*" * 40)
    print(f"List of TODO files: {len(todo_files)}")
    for file_name in todo_files:
        print(file_name)
    print("*" * 40)
