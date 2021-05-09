from ktrain import text
INDEXDIR = './index/myindex'

qa = text.SimpleQA(INDEXDIR)
answers = qa.ask('What accopmanies pneumonia?')
print(answers[:1])
# qa.display_answers(answers[:5])