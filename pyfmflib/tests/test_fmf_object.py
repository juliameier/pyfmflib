#import nose
import pytest
import inspect
import numpy
import unittest

from pyfmflib.fmf import FMF

class Test_Fmf:

    def setup(self):
        self.fmf_object = FMF()

    def test_empty_fmf(self):
        assert self.fmf_object is not None

    def test_empty_fmf_instance(self):

        assert isinstance(self.fmf_object, FMF)

    def test_create_fmf_with_reference(self):

        self.fmf_object.reference_section = self.fmf_object.set_reference(self, 'title', 'Creator', 'Created', 'Place')

        self.fmf_object.meta_sections.append(self.fmf_object.reference_section)

        assert self.fmf_object.meta_sections is not None

        assert len(self.fmf_object.meta_sections) > 0
#        assert isinstance(self.fmf_object, Fmf.FMF)

    def test_create_fmf_meta_section(self):
        meta_section = FMF.add_meta_section(self.fmf_object, 'Name')
        self.fmf_object.meta_sections.append(meta_section)

        assert self.fmf_object.meta_sections is not None

        assert len(self.fmf_object.meta_sections) > 0

    def test_add_meta_section_invalid_name(self):
        FMF.add_meta_section(self.fmf_object, '*Name')

    def test_add_meta_section_existing_name(self):
        meta_section = FMF.add_meta_section(self.fmf_object, 'Name')
        self.fmf_object.meta_sections.append(meta_section)

        meta_section2 = FMF.add_meta_section(self.fmf_object, 'Name')
        self.fmf_object.meta_sections.append(meta_section2)

    def test_create_fmf_with_table(self):
        self.fmf_object.table_sections.append(FMF.add_table(self.fmf_object, 'Table Name', 'Table Symbol'))

        assert self.fmf_object.table_sections is not None

        assert len(self.fmf_object.table_sections) > 0

    def test_get_meta_section(self):
        meta_section = FMF.add_meta_section(self.fmf_object, 'Name')
        self.fmf_object.meta_sections.append(meta_section)

        meta_section_returned = FMF.get_meta_section(self.fmf_object, 'Name1')
        print meta_section_returned.name

        assert meta_section_returned is not None


