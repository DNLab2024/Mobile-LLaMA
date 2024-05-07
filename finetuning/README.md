## Fine-tuning LLaMA
Install Package (python>=3.9)
```bash
pip install -r ../requirements.txt
```

Below is a command that fine-tunes LLaMA-13B with our dataset. Run the training script with the following command, adjusting the parameters as necessary for your specific training needs:

```bash
python mobile_llama_finetuning.py \
    --output_dir "../mobile_llama" \
    --batch_size 4 \
    --gradient_accumulation_steps 1 \
    --optim "paged_adamw_32bit" \
    --logging_steps 200 \
    --learning_rate 0.0001 \
    --max_grad_norm 0.3 \
    --max_steps 5000 \
    --warmup_ratio 0.05 \
    --lora_alpha 16 \
    --lora_dropout 0.1 \
    --lora_r 64 \
    --num_train_epochs 3.0
```
