from ktrain import text
INDEXDIR = './index/myindex'

qa = text.SimpleQA(INDEXDIR)
answers = qa.ask('My shoulders are killing me from hitting in hockey. What can I do to recover quickly?')
print(answers[:1])
# qa.display_answers(answers[:5])