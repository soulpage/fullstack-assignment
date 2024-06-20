## Still in progress
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the pre-trained SentenceTransformer model
sentence_transformer_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the pre-trained GPT-2 model and tokenizer
gpt_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
gpt_model = GPT2LMHeadModel.from_pretrained('gpt2')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
sentence_transformer_model = sentence_transformer_model.to(device)
gpt_model = gpt_model.to(device)

def get_relevant_context(user_input, vault_embeddings, vault_context, top_k=3):
    input_embedding = sentence_transformer_model.encode([user_input])
    input_embedding = torch.tensor(input_embedding).to(device)
    cos_scores = util.cos_sim(input_embedding, vault_embeddings)[0]
    top_k = min(top_k, len(cos_scores))
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    relevant_context = [vault_context[i].strip() for i in top_indices]
    return relevant_context

def generate_rag_response(user_input, relevant_context, max_length=100):
    context = "\n".join(relevant_context) + "\n\n" + user_input
    input_ids = gpt_tokenizer.encode(context, return_tensors='pt').to(device)
    output_ids = gpt_model.generate(input_ids, max_length=max_length, num_beams=5, early_stopping=True)
    response = gpt_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response