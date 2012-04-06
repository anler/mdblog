import os
import shutil
import argparse
import unittest

from mdblog.scripts import utils


class ValidDirTest(unittest.TestCase):
    def test_valid_dir(self):
        "Test that returns the path when given a valid path"
        valid_path = os.path.dirname(__file__)
        self.assertEqual(valid_path, utils.is_dir(valid_path))

    def test_invalid_dir(self):
        """Test that raises an argparse.ArgumentTypeError when given an invalid
        path"""
        invalid_path = os.path.join(os.path.dirname(__file__), "invalid-path")
        self.assertRaises(argparse.ArgumentTypeError, utils.is_dir,
                          invalid_path)


class BlogNameTest(unittest.TestCase):
    def test_dir_exists(self):
        """Test that raises and argparse.ArgumentTypeError if the given name
        is an existing directory
        """
        current = os.getcwd()
        valid_dir = os.path.dirname(__file__)
        os.chdir(os.path.abspath(os.path.join(valid_dir, "..")))
        name = os.path.basename(valid_dir)
        self.assertRaises(argparse.ArgumentTypeError, utils.valid_name, name)
        os.chdir(current)

    def test_valid_name(self):
        """Test that returns the name if the given name is not an existing
        directory and use only numbers, letters and underscores
        """
        for name in ("myblog", "1234", "myblog1234", "myblog_1234"):
            self.assertEqual(name, utils.valid_name(name))

    def test_invalid_name(self):
        """Test that raises an argparse.ArgumentTypeError if the given name
        is invalid
        """
        self.assertRaises(argparse.ArgumentTypeError, utils.valid_name, "a/b")
        self.assertRaises(argparse.ArgumentTypeError, utils.valid_name, "a b")


class MakeTreeTest(unittest.TestCase):
    def setUp(self):
        self.current = os.getcwd()
        self.path = "mktree_test"
        os.mkdir(self.path)
        os.chdir(self.path)

    def tearDown(self):
        os.chdir(self.current)
        shutil.rmtree(self.path)

    def test_mktree(self):
        "Test that recursively creates the given tree"
        utils.mktree("a/b/c")
        self.assertTrue(os.path.isdir("a"))
        self.assertTrue(os.path.isdir("a/b"))
        self.assertTrue(os.path.isdir("a/b/c"))

    def test_touch(self):
        "Test that creates empty files"
        utils.touch("a")
        self.assertTrue(os.path.isfile("a"))

    def test_touch_nested(self):
        "Test that creates directories if the don't exist and empty files"
        utils.touch("a/b/c")
        self.assertTrue(os.path.isfile("a/b/c"))


