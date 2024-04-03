# Mobile-LLaMA: instruction fine-tuning open-source LLM for network analysis in 5G NWDAF

**Abstract**: In the evolving landscape of 5G networks, the Network Data Analytics Function (NWDAF) emerges as a key component, interacting with core network elements to enhance data collection, model training, and analytical outcomes.  
Language Models (LLMs), with their state-of-the-art capabilities in natural language processing, have been successful in numerous fields. In particular, LLMs enhanced through instruction fine-tuning have demonstrated their effectiveness by employing sets of instructions to precisely tailor the model's responses and behavior. However, it requires collecting a large pool of high-quality training data regarding the precise domain knowledge and the corresponding programming codes. 
We present an open-source mobile network-specialized LLM - Mobile-LLaMA, instruction-finetuned LLaMA-13B model. We built Mobile-LLaMA by instruction fine-tuning LLaMA with our own network analysis data that we collect from publicly available, real-world 5G network datasets and expanded by the self-instruct framework utilizing OpenAI’s pretrained models (PMs). Mobile-LLaMA has three main functions: Packet Analysis Function, IP Routing Analysis, and Performance Analysis Function, enabling it to provide network analysis and contribute to the automation and artificial intelligence (AI) required for 5G network management and data analysis. 
Our evaluation demonstrates Mobile-LLaMA's proficiency in network analysis code generation, achieving a score of 247 out of 300, surpassing Chat-GPT’s score of 209.

## Directory Structure

- **self_instruct_data**: Three separate subdirectories, each containing instructions generated via the self-instruct framework for one of Mobile-LLaMA's main functions: Packet Analysis, IP Routing Analysis, and Performance Analysis.

- **training_data**: The main training data for Mobile-LLaMA. We've combined all the instructions used in training, totaling 15,111 instruction sets.

- **evaluation**: Three JSON files containing specific instructions used for "Performance Evaluation" in each respective function.

## Jupyter Notebook Scripts

- **Mobile-LLaMA_finetune.ipynb**: Jupyter Notebook script is designed for instruction fine-tuning of Mobile-LLaMA 13B. You can use this script to fine-tune the model with specific instructions tailored to your needs.

- **Mobile-LLaMA_demo.ipynb**: Jupyter Notebook script allows you to load Mobile-LLaMA from HuggingFace and use it for demonstration and evaluation purposes. You can use this script to generate and evaluate code for various network analysis tasks.

## Getting Started
### Install
Clone this repository and navigate to the ToolBench folder.
```bash
git clone github.com/DNLab2024/Mobile-LLaMA.git
cd Mobile-LLaMA
```
Install Package (python>=3.9)
```bash
pip install -r requirements.txt
```

## Figures and Tables
### The Architecture of NWDAF featuring Mobile-LLaMA for 5G network analytics
<figure>
  <img src="images/architecture.png" alt="Architecture" style="width: auto; max-width: 100%; height: auto; max-height: 60%;">

</figure>

<div style="display: flex; flex-direction: row; justify-content: center; overflow-x: auto;">
    <div style="flex: 0 0 auto; margin-right: 10px;"> 
        <p align="center">Prompt example</p>
        <p align="center">
            <img src="images/prompt_example.png" alt="Prompt example" style="width: 400px; height: auto;">
        </p>
    </div>
    <div style="flex: 0 0 auto; margin-right: 10px;">
        <p align="center">Manual seed task example</p>
        <p align="center">
            <img src="images/instruction_example.png" alt="Manual seed task example" style="width: 400px; height: auto;">
        </p>
    </div>
    <div style="flex: 0 0 auto; margin-left: 10px;">
        <p align="center">Self-instruct generated example</p>
        <p align="center">
            <img src="images/self_instruct_example.png" alt="Self-instruct generated example" style="width: 400px; height: auto;">
        </p>
    </div>
</div>


### Analysis Tasks in NWDAF of 5G Network with Mobile-LLaMA and Training Data Summary
| Function of Mobile-LLaMA     | Analysis Tasks                                      | Library           | Manual Instruction Tasks | Self-Instruct Generated Instructions |
|--------------------------|-----------------------------------------|-------------------|------------------------|-------------------------------------|
| Packet analysis          | Parsing IP packets<br>Data structuring<br>RTT calculation<br>Packet size examination<br>Performance assessment<br>QoS assessment | `Scapy`           | 20                     | 2000                                |
| IP routing analysis      | BGP route anomalies<br>BGP path changes       | `PyBGPStream`     | 100                    | 10000                               |
| Performance analysis     | Per-user capacity Enhancement<br>5G investment cost analysis<br>Network quality evaluation<br>UE traffic anomaly detection<br>jitter & CQI benchmarking | `Pandas`, `Matplotlib` | 30 | 3000                                |


### Overview of Performance Evaluation Analysis Tasks

### Evaluation workflow
<div style="display: flex; flex-direction: row; justify-content: center;">
    <div style="flex: 1; margin-right: 10px;">
        <p align="center">Performance evaluation workflow</p>
        <p align="center">
            <img src="images/eval_workflow.png" alt="Performance evaluation workflow" style="width: 600px; height: auto;">
        </p>
    </div>
    <div style="flex: 1; margin-left: 10px;">
        <p align="center">Error type examples</p>
        <p align="center">
            <img src="images/raw_results.png" alt="Error type examples" style="width: 600px; height: auto;">
        </p>
    </div>
</div>

### Performance evaluation score: LLaMA 7B, 13B, 70, Mobile-LLaMA, Chat-GPT 3.5
<figure>
  <img src="images/eval_score.png" alt="Performance evaluation score: LLaMA 7B, 13B, 70, Mobile-LLaMA, Chat-GPT 3.5" style="width: auto; max-width: 80%; height: auto; max-height: 60%;">
  <!-- <figcaption>Performance evaluation score: LLaMA 7B, 13B, 70, Mobile-LLaMA, Chat-GPT 3.5</figcaption> -->
</figure>
