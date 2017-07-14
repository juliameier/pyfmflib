import pytest


from API.Meta_section import Meta_section, Meta_section_entry
from API.Fmf import FMF

class Test_Meta_Section:

    def setup(self):
        self.meta_section = Meta_section('Meta Section Name')

    def test_create_meta_section(self):
        assert self.meta_section is not None

    def test_meta_section_object(self):
        assert isinstance(self.meta_section, Meta_section)

    def test_add_meta_section_to_fmf(self):
        fmf_object = FMF()

        fmf_object.meta_sections = [fmf_object.add_meta_section(self.meta_section.name)]

        assert fmf_object.meta_sections is not None

    def test_add_entry(self):
        entry = Meta_section.add_entry(self.meta_section,'key','value')

        assert entry is not None

        self.meta_section.entries.append(entry)

        assert len(self.meta_section.entries) > 0

    def test_add_entry_with_same_name(self):
#        entry1 = Meta_section.add_entry(self.meta_section,'key1','value1')
#        entry2 = Meta_section.add_entry(self.meta_section,'key1','value2')

        entry1 = Meta_section_entry('key1','value1')
        entry2 = Meta_section_entry('key2','value2')

        assert entry1.key != entry2.key


    def test_get_entry(self):

        key = 'key1'
        value = 'value1'
        entry1 = Meta_section.add_entry(self.meta_section, key, value)

        item = Meta_section.get_entry(self.meta_section, key)

        print (item.value)
        print (self.meta_section.name)

        assert item is not None

        assert item.key == key and item.value == value


    def test_get_entry_wrong_key(self):
        key = 'key1'
        value = 'value1'
        entry1 = Meta_section.add_entry(self.meta_section, key, value)

        self.meta_section.entries.append(entry1)

        key_to_get = 'key2'

        item_key = self.meta_section.entries.__getitem__(0).key

        assert key_to_get == item_key


    def test_get_entry_no_entries(self):
        item = Meta_section.get_entry(self.meta_section, None)






