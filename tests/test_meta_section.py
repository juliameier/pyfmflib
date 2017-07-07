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
        entry = Meta_section_entry('key', 'value')

        assert entry is not None

        self.meta_section.entries.append(entry)

        assert len(self.meta_section.entries) > 0


