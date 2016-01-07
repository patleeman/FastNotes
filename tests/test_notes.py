import unittest
import note
from tests import UnitTestTools
import unittest.mock as mock

class TestNotePy(unittest.TestCase):
    def setUp(self):
        pass

    @mock.patch('note.note_tag_find')
    @mock.patch('note.note_tags')
    @mock.patch('note.note_help')
    @mock.patch('note.helper_space_print')
    @mock.patch('note.note_search')
    @mock.patch('note.note_tag_all')
    @mock.patch('note.note_last')
    @mock.patch('note.note_create')
    def test_Main(self, create, last, tag_all, search, space_print, help, tags, tag_find):
        test_dict = {
            create: ['create', 'new'],
            last: ['last'],
            tag_all: ['list', 'all', ['tag', 'all'], ['tag', 'list']],
            search: ['search', 'find'],
            space_print: ['push', 'pull'],
            help: ['help'],
            tags: ['tags', 'tag'],
            tag_find: [['tag', 'find'], ['tag', 'peek']],

        }

        for obj in test_dict.keys():
            for call in test_dict[obj]:
                commands = ['note']
                if isinstance(call, str):
                    commands.append(call)
                elif isinstance(call, list):
                    commands.extend(call)

                with mock.patch('sys.argv', commands):
                    note.main()

                self.assertTrue(obj.called)

    def test_note_search(self):
        args = ['/foo/bar.py', 'search', 'test1', 'test2']
        def helper_grep_notes_search(low):
            return [[1, 'test'], [2, 'test']]
        def helper_display_matches(display_list, other):
            return
        self.assertTrue(note.note_search(args))

    def test_note_last(self):
        pass

    def test_note_tags(self):
        pass

    def test_note_tag_all(self):
        pass

    def test_note_tag_find(self):
        pass

    def test_helper_display_matches(self):
        pass

    def test_helper_get_modified_date(self):
        pass

    def test_helper_get_created_date(self):
        pass

    def test_helper_colorify(self):
        pass

    def test_helper_stringify_list(self):
        pass

    def test_helper_grepper(self):
        pass

    def test_helper_grep_notes_search(self):
        pass

    def test_helper_grep_notes_tag(self):
        pass

    def test_note_help(self):
        with UnitTestTools.captured_output() as (out, err):
            note.note_help()
        output = out.getvalue().strip()
        self.assertIsInstance(output, str)

    def test_note_create(self):
        pass

    def test_helper_open_editor(self):
        pass

    def test_helper_generate_file_name(self):
        pass

    def test_helper_create_base_file(self):
        pass

    def test_helper_space_sprint(self):
        pass

    def test_helper_verify_notes_directory(self):
        pass

