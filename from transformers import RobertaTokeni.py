# from transformers import RobertaTokenizerFast, RobertaForSequenceClassification, TextClassificationPipeline

# # Load fine-tuned MRC model by HuggingFace Model Hub
# HUGGINGFACE_MODEL_PATH = "bespin-global/klue-roberta-small-3i4k-intent-classification"
# loaded_tokenizer = RobertaTokenizerFast.from_pretrained(HUGGINGFACE_MODEL_PATH )
# loaded_model = RobertaForSequenceClassification.from_pretrained(HUGGINGFACE_MODEL_PATH )

# # using Pipeline
# text_classifier = TextClassificationPipeline(
#     tokenizer=loaded_tokenizer, 
#     model=loaded_model, 
#     return_all_scores=True
# )

# # predict
# text = "your text"

# preds_list = text_classifier(text)
# best_pred = preds_list[0]
# print(f"Label of Best Intentatioin: {best_pred['label']}")
# print(f"Score of Best Intentatioin: {best_pred['score']}")





# import torchaudio
# from speechbrain.pretrained import EncoderClassifier
# classifier = EncoderClassifier.from_hparams(source="speechbrain/lang-id-commonlanguage_ecapa", savedir="pretrained_models/lang-id-commonlanguage_ecapa")
# # Italian Example
# out_prob, score, index, text_lab = classifier.classify_file('speechbrain/lang-id-commonlanguage_ecapa/example-it.wav')
# print(text_lab)

# # French Example
# out_prob, score, index, text_lab = classifier.classify_file('speechbrain/lang-id-commonlanguage_ecapa/example-fr.wav')
# print(text_lab)







# # Tip: By now, install transformers from source

# from transformers import AutoModelWithLMHead, AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-e2m-intent")
# model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-e2m-intent")

# def get_intent(event, max_length=16):
#   input_text = "%s </s>" % event
#   features = tokenizer([input_text], return_tensors='pt')

#   output = model.generate(input_ids=features['input_ids'], 
#                attention_mask=features['attention_mask'],
#                max_length=max_length)

#   return tokenizer.decode(output[0])

# event = "PersonX takes PersonY home"
# get_intent(event)

# # output: 'to be helpful'