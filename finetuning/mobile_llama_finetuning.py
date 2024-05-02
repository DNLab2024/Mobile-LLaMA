import os
import transformers
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoConfig, AutoTokenizer, TrainingArguments
from trl import SFTTrainer
from torch import cuda
from peft import LoraConfig
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Fine-tuning Mobile LLaMA for specific tasks")
    parser.add_argument('--output_dir', type=str, default="../mobile_llama_5kEpoch",
                        help='Directory to save model and logs')
    parser.add_argument('--batch_size', type=int, default=4,
                        help='Training batch size per device')
    parser.add_argument('--gradient_accumulation_steps', type=int, default=1,
                        help='Number of updates steps to accumulate before performing a backward/update pass.')
    parser.add_argument('--optim', type=str, default="paged_adamw_32bit",
                        help='Optimizer type')
    parser.add_argument('--logging_steps', type=int, default=200,
                        help='Logging interval')
    parser.add_argument('--learning_rate', type=float, default=1e-4,
                        help='Learning rate')
    parser.add_argument('--max_grad_norm', type=float, default=0.3,
                        help='Max gradient norm')
    parser.add_argument('--max_steps', type=int, default=5000,
                        help='Maximum number of training steps')
    parser.add_argument('--warmup_ratio', type=float, default=0.05,
                        help='Warmup ratio for learning rate scheduler')
    parser.add_argument('--lora_alpha', type=int, default=16,
                        help='LoRA alpha parameter')
    parser.add_argument('--lora_dropout', type=float, default=0.1,
                        help='LoRA dropout rate')
    parser.add_argument('--lora_r', type=int, default=64,
                        help='LoRA r parameter')
    parser.add_argument('--num_train_epochs', type=float, default=3.0,
                        help='Number of training epochs')

    return parser.parse_args()

def main():
    args = get_args()
    hf_token = os.environ.get('HF_TOKEN')  # Make sure to export HF_TOKEN in your terminal or set it in your environment variables
    model_id = 'meta-llama/Llama-2-13b-chat-hf'
    data = load_dataset("json", data_files="../training_data/Mobile_LLaMA_main.json")

    model = load_model(model_id, hf_token)
    tokenizer = load_tokenizer(model_id, hf_token)
    trainer = setup_training(data, tokenizer, model, args)
    trainer.train()

def load_model(model_id, hf_auth):
    model_config = AutoConfig.from_pretrained(model_id, use_auth_token=hf_auth)
    bnb_config = transformers.BitsAndBytesConfig(load_in_8bit=True)

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        trust_remote_code=True,
        config=model_config,
        quantization_config=bnb_config,
        device_map='auto',
        use_auth_token=hf_auth
    )
    model.eval()
    device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
    print(f"Model loaded on {device}")
    return model

def load_tokenizer(model_id, hf_auth):
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=hf_auth)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    return tokenizer

def setup_training(data, tokenizer, model, args):
    
    train_val = data["train"].train_test_split(test_size=1300, shuffle=True, seed=42)

    def generate_and_tokenize_prompt(data_point):
        prompt = f"""Below is an instruction that describes a task, paired with an output that provides the completion of the task.
        ### Instruction:
        {data_point["instruction"]}
        ### Response:
        {data_point["output"]}"""
        
        result = tokenizer(prompt, truncation=True, max_length=2048, padding=False, return_tensors=None)
        if (result["input_ids"][-1] != tokenizer.eos_token_id and len(result["input_ids"]) < 2048):
            result["input_ids"].append(tokenizer.eos_token_id)
            result["attention_mask"].append(1)
        result["labels"] = result["input_ids"].copy()
        return result
    
    train_data = train_val["train"].map(generate_and_tokenize_prompt, batched=True)
    val_data = train_val["test"].map(generate_and_tokenize_prompt, batched=True)

    training_arguments = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        optim=args.optim,
        logging_steps=args.logging_steps,
        learning_rate=args.learning_rate,
        fp16=args.fp16,
        max_grad_norm=args.max_grad_norm,
        max_steps=args.max_steps,
        warmup_ratio=args.warmup_ratio,
        num_train_epochs=args.num_train_epochs,
        lr_scheduler_type=args.lr_scheduler_type,
        group_by_length=True
    )

    peft_config = LoraConfig(
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        r=args.lora_r,
        bias="none",
        task_type="CAUSAL_LM"
    )

    data_collator = transformers.DataCollatorForSeq2Seq(
        tokenizer, return_tensors="pt", padding=True
    )

    trainer = SFTTrainer(
        model=model,
        args=training_arguments,
        train_dataset=train_data,
        eval_dataset=val_data,
        tokenizer=tokenizer,
        peft_config=peft_config,
        data_collator=data_collator,
    )

    return trainer

if __name__ == '__main__':
    main()
