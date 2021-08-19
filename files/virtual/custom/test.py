import unittest
from unittest.mock import MagicMock
from .files_manager import VirtualManager

class MockIndexManager:
    def get_indexed_files(self):
        pass

class TestVirtualManager(unittest.TestCase):
    def setUp(self):
        self.vm=VirtualManager()
        self.vm.index_manager=MockIndexManager()
        self.items=[
            ['F:\\BA\\C\\D',15,"filesystem"],
            ['A:\\B\\E\\D',15,"filesystem"],
            ['A:\\B\\C\\D',15,"filesystem"],
            ['A:\\B',15,"filesystem"],
            ['A:\\C',15,"filesystem"]
        ]
        
        self.vm.index_manager.get_indexed_files=MagicMock(return_value=self.items)
        
    def tearDown(self):
        pass

    def test_get_root_items(self):
        result=self.vm.get_root_items()
        self.assertEqual(result,['F:','A:'],'Incorect root items.')

    def test_get_all_items(self):
        result=self.vm.get_all_items()
        self.assertEqual([[i.path,i.value,i.other[0]] for i in result],self.items,"Incorect fetch of all items.")

    def test_get_item_existing(self):
        result=self.vm.get_item("A:\\B\\C\\D")
        self.assertNotEqual(result,None,'Failed to find existing item.')

    def test_get_item_non_existing(self):
        result=self.vm.get_item("A:\\A\\C\\D")
        self.assertCountEqual(result,[],'Found a non existing item.')


    def test_get_children(self):
        result=self.vm.get_children('A:\\B\\C')
        self.assertEqual(result[0].name,'D',"Could not fetch children for path.")

    def test_get_parent(self):
        result=self.vm.get_parent("A:\\B\\C")
        self.assertEqual(result[0].name,'B','Wrong parent for path.')
        
    def test_is_traversable_True(self):
        result=self.vm.is_traversable('A:\\B')
        self.assertEqual(result,True,"Failed to detect traversible route.")

    def test_is_traversable_False(self):
        result=self.vm.is_traversable('A:\\B\\C\\D')
        self.assertEqual(result,False,"Flagged un-traversable route as traversible.")

    def test_buildNodeFromLine_Success(self):
        result=self.vm.buildNodeFromLine("A:\\B\\C\\D;15;filesystem")
        self.assertEqual(result.path,'A:\\B\\C\\D',"VNode build has assigned wrong path.")
        self.assertEqual(result.name,'D',"VNode build has assigned wrong name.")
        self.assertEqual(result.value,'15',"VNode build has assigned wrong value.")

    def test_buildNodeFromLine_Fail(self):
        with self.assertRaises(IndexError):
            result=self.vm.buildNodeFromLine("")
        