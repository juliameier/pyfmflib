#import nose
import pytest
import inspect
import numpy
import unittest

from API.Fmf import FMF

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
        self.fmf_object.meta_sections.append(FMF.add_meta_section(self.fmf_object,'Name'))

        assert self.fmf_object.meta_sections is not None

        assert len(self.fmf_object.meta_sections) > 0


    def test_create_fmf_with_table(self):

        self.fmf_object.table_sections.append(FMF.add_table(self.fmf_object, 'Table Name', 'Table Symbol'))

        assert self.fmf_object.table_sections is not None

        assert len(self.fmf_object.table_sections) > 0
