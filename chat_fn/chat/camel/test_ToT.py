import unittest
from unittest.mock import Mock, patch
from ToT import EvaluationChain, EvaluationScore, process_task, validate_task

class TestToT(unittest.TestCase):
    
    def test_score_in_range(self):
        es = EvaluationScore(score=5)
        self.assertEqual(es.score, 5)

    def test_score_out_of_range(self):
        with self.assertRaises(ValueError):
            es = EvaluationScore(score=11)
            
    def test_score_negative(self):
        with self.assertRaises(ValueError):
            es = EvaluationScore(score=-1)

    def test_valid_task(self):
        self.assertTrue(validate_task("This is a task."))
        
    def test_empty_task(self):
        self.assertFalse(validate_task(""))
        
    def test_none_task(self):
        self.assertFalse(validate_task(None))

    @patch('ToT.LLMChain')
    @patch('ToT.PydanticOutputParser')
    def test_evaluation_chain_call(self, MockParser, MockChain):
        mock_parser_instance = MockParser.return_value
        mock_parser_instance.parse.return_value = EvaluationScore(score=5)
        mock_chain_instance = MockChain.return_value
        mock_chain_instance.__call__.return_value = "test"
        
        ec = EvaluationChain(llm=None, prompt=None, output_parser=mock_parser_instance)
        result = ec("test")
        
        self.assertEqual(result, EvaluationScore(score=5))
        mock_parser_instance.parse.assert_called_once_with("test")

    @patch('ToT.Queue')
    @patch('ToT.decomposition_chain')
    @patch('ToT.generation_chain')
    @patch('ToT.evaluation_chain')
    @patch('ToT.search_chain')
    def test_process_task(self, mock_search, mock_evaluation, mock_generation, mock_decomposition, mock_queue):
        process_task("test", mock_queue, [], "", 0)
        # add your assertions here

if __name__ == '__main__':
    unittest.main()
