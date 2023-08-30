import random

import torch
from transformers import BertTokenizerFast, ErnieForCausalLM


def load_model(repo: str, revision: str = "main"):
    tokenizer = BertTokenizerFast.from_pretrained("wybxc/new-yiri")
    assert isinstance(tokenizer, BertTokenizerFast)
    model = ErnieForCausalLM.from_pretrained(repo, revision=revision)
    assert isinstance(model, ErnieForCausalLM)

    return tokenizer, model


def generate(tokenizer: BertTokenizerFast, model: ErnieForCausalLM, input_str: str):
    input_ids = tokenizer.encode(input_str, return_tensors="pt")
    outputs = model.generate(
        input_ids,
        max_new_tokens=100,
        penalty_alpha=0.4 + 0.2 * random.random(),
        top_k=5,
        early_stopping=True,
        decoder_start_token_id=tokenizer.sep_token_id,
        eos_token_id=tokenizer.sep_token_id,
        return_dict_in_generate=True,
        output_scores=True,
    )
    outputs, scores = outputs.sequences, outputs.scores
    i, j = torch.nonzero(outputs[0] == tokenizer.sep_token_id)
    output = tokenizer.decode(
        outputs[0, i:j],
        skip_special_tokens=True,
    ).replace(" ", "")
    score = float(
        torch.stack(scores).squeeze(1).log_softmax(axis=1).max(axis=1)[0].mean()
    )
    return output, score
