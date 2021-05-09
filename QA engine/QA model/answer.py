from ktrain import text
INDEXDIR = './index/myindex'
# text.SimpleQA.initialize_index("./index/myindex")
qa = text.SimpleQA(INDEXDIR)
answers = qa.ask('what is my age when i get periods')
print(answers[:1])
# qa.display_answers(answers[:5])

# from flask import Flask, jsonify

# app = Flask(__name__

# @app.route('/query', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})

# if __name__ == '__main__':
#     app.run(debug=True)