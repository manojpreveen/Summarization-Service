import torch
from pydantic import BaseModel
from fastapi import FastAPI
from transformers import BartTokenizer, BartForConditionalGeneration

class Input(BaseModel):
    document: str
    summary: str = None

class Output(BaseModel):
    summary: str

readiness_flag = False

app = FastAPI()
model_name = 'manojpreveen/distilbart-cnn-v2'
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'
    print('Running on CUDA GPU')
    #model.cuda()
    model.half()
else:
    print('Running on CPU')

model.to(device)
model.eval()

readiness_flag = True

def preprocess(text):
  text = text.replace("\n"," ").replace("\\"," ")
  return text

def liveness_check():
    check_input = "This is to test for the liveness of this summarization routine."
    check_summary = summary(check_input)
    if check_summary in [" This is to test for the liveness of this summarization routine. This is the first time the summarization of this routine has been tested for the effectiveness of the routine. It's to test whether the routine is true and that it will be tested for its effectiveness in this routine."]:
        return True
    return False

def summary(text):
    batch = [preprocess(text)]
    inputs = tokenizer(batch, max_length=1024, truncation=True, return_tensors='pt')
    input_id = inputs['input_ids'].to(device)
    summary_ids = model.generate(input_id, num_beams=4, length_penalty=2.0, min_length=55, max_length=80, no_repeat_ngram_size=3, early_stopping=True)
    dec = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    dec[0]=dec[0].replace(" .",".")
    return dec[0]

@app.post('/summarize',response_model=Output)
def summarize(input:Input):
    input.summary = summary(input.document)
    return input

@app.get('/liveness')
def liveness():
    if readiness_flag and liveness_check():
        return {"Ok"}
    else:
        return {"Liveness Failed"}, 500

@app.get('/readiness')
def readiness():
    if readiness_flag:
        return {"Ok"}
    else:
        return {"Readiness Failed"}, 500
