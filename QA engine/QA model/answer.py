import ktrain
from ktrain import text
INDEXDIR = './index'

qa = text.SimpleQA(INDEXDIR)
answers = qa.ask('i cant sleep well')
print(answers[:1])
# qa.display_answers(answers[:5])