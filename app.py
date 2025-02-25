import torch
from transformers import BertTokenizerFast, BertForTokenClassification
from flask import Flask, request, render_template_string
from UtilityFunctions.utilityFunctions2 import preprocess_data, predict, idx2tag

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

MAX_LEN = 500
NUM_LABELS = 12
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = 'bert-base-uncased'
STATE_DICT = torch.load("model-state.bin", map_location=DEVICE)
TOKENIZER = BertTokenizerFast("./vocab/vocab.txt", lowercase=True)

model = BertForTokenClassification.from_pretrained(
    'bert-base-uncased', state_dict=STATE_DICT['model_state_dict'], num_labels=NUM_LABELS)
model.to(DEVICE)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Resume Entity Extractor</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; background-color: #f8f9fa; }
        h2 { color: #343a40; }
        form { margin-bottom: 20px; }
        textarea { width: 80%; height: 120px; padding: 10px; border-radius: 5px; border: 1px solid #ccc; }
        button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .container { max-width: 700px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.1); }
        .entities-container { text-align: left; background: #fff; padding: 15px; border-radius: 5px; margin-top: 20px; }
        .entity { padding: 5px; margin: 5px 0; border-radius: 3px; font-weight: bold; }
        .Name { background-color: #d4edda; color: #155724; }
        .Degree { background-color: #cce5ff; color: #004085; }
        .Skills { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Enter Text to Extract Entities</h2>
        <form action="/" method="post">
            <textarea name="text" placeholder="Enter resume text here..." required></textarea><br>
            <button type="submit">Extract Entities</button>
        </form>
        {% if entities %}
            <h3>Extracted Entities:</h3>
            <div class="entities-container">
                {% for entity in entities %}
                    <div class="entity {{ entity['entity'] }}">
                        <strong>{{ entity['entity'] }}:</strong> {{ entity['text'] }}
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    entities = None
    if request.method == 'POST':
        text = request.form.get('text', '')
        if text:
            resume_text = preprocess_data(text)
            entities = predict(model, TOKENIZER, idx2tag, DEVICE, resume_text, MAX_LEN)
    return render_template_string(HTML_TEMPLATE, entities=entities)

if __name__ == '__main__':
    app.run(debug=True)