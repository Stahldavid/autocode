import unittest
from unittest.mock import MagicMock
from final import create_dataframe, unir_textos_documentos, chat, build_the_bot, clear_chat_history

class TestPesquisaFinal(unittest.TestCase):

    def test_create_dataframe(self):
        source_documents = [
            MagicMock(metadata={'page': 1, 'source': 'doc1'}),
            MagicMock(metadata={'page': 2, 'source': 'doc2'})
        ]
        expected_df_string = '   Page Number Document Name\n0            1          doc1\n1            2          doc2'
        self.assertEqual(create_dataframe(source_documents), expected_df_string)

    def test_unir_textos_documentos(self):
        source_documents = [
            MagicMock(page_content='This is the first document.'),
            MagicMock(page_content='This is the second document.')
        ]
        expected_texto_unido = 'This is the first document. This is the second document.'
        self.assertEqual(unir_textos_documentos(source_documents), expected_texto_unido)

    def test_chat(self):
        chat_history = []
        message = 'What is the capital of France?'
        expected_chat_history = [(message, 'Paris is the capital of France.')]
        expected_source_documents_text = 'The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower. Constructed from 1887 to 1889 as the entrance to the 1889 World\'s Fair, it was initially criticized by some of France\'s leading artists and intellectuals for its design, but it has become a global cultural icon of France and one of the most recognizable structures in the world. The tower is the tallest structure in Paris and the most-visited paid monument in the world. The tower has three levels for visitors, with restaurants on the first and second levels. The top level's upper platform is 276 m (906 ft) above the ground – the highest observation deck accessible to the public in the European Union. Tickets can be purchased to ascend by stairs or lift to the first and second levels. The climb from ground level to the first level is over 300 steps, as is the climb from the first to the second level. Although there is a staircase to the top level, it is usually only accessible by lift.'
        expected_df_string = '   Page Number Document Name\n0            1          doc1\n1            2          doc2'
        result = chat(chat_history, message)
        self.assertEqual(result[0], expected_chat_history)
        self.assertEqual(result[1], expected_source_documents_text)
        self.assertEqual(result[2], expected_df_string)

    def test_build_the_bot(self):
        upload_arquivos = MagicMock(name='upload_arquivos')
        upload_arquivos.name = 'test.zip'
        expected_chat_history = [('Bot', 'Index saved successfully!!!')]
        self.assertEqual(build_the_bot(upload_arquivos), expected_chat_history)

    def test_clear_chat_history(self):
        chatbot = MagicMock(name='chatbot')
        expected_chat_history = []
        self.assertEqual(clear_chat_history(chatbot), expected_chat_history)

if __name__ == '__main__':
    unittest.main()



    """You can run the unit tests for your code in Visual Studio Code by using the built-in test runner. Here are the steps:

Open the file containing your unit tests in Visual Studio Code.
Click on the "Run" button in the left-hand menu (or press Ctrl+Shift+D).
Click on the "Create a launch.json file" button.
Select "Python" as the environment.
Select "Discover tests" as the test type.
Choose the test framework you are using (e.g. unittest).
Choose the folder containing your tests.
Save the launch.json file.
Click on the "Run" button again.
Select the test you want to run from the dropdown menu.
Click on the "Run" button next to the test.
This will run the selected test and display the results in the "Test Explorer" pane. You can also run all tests in the folder by selecting "Run All Tests" from the dropdown menu."""