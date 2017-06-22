import pytest


from API import Meta_section

class test_meta_section():

    def __int__(self):
        self.meta_section = Meta_section.Meta_section.Tableinitialize()

    def test_create_meta_section(self):
        assert self.meta_section is not None

    def test_meta_section_object(self):
        assert isinstance(self.meta_section, Meta_section.Meta_section)

    def test_create_meta_section_with_name(self):
        meta_section = Meta_section.Meta_section.initialize('Meta_Section_Name')

        assert meta_section is not None


if __name__ == '__main__':
    pytest.main([__file__])
