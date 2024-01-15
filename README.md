# Mobile-LLaMA: instruction fine-tuning open-source LLM for network analysis in 5G NWDAF

**Abstract**: In the evolving landscape of 5G networks, the Network Data Analytics Function (NWDAF) emerges as a key component, interacting with core network elements to enhance data collection, model training, and analytical outcomes.  
Language Models (LLMs), with their state-of-the-art capabilities in natural language processing, have been successful in numerous fields. In particular, LLMs enhanced through instruction fine-tuning have demonstrated their effectiveness by employing sets of instructions to precisely tailor the model's responses and behavior. However, it requires collecting a large pool of high-quality training data regarding the precise domain knowledge and the corresponding programming codes. 
We present an open-source mobile network-specialized LLM - Mobile-LLaMA, instruction-finetuned LLaMA-13B model. We built Mobile-LLaMA by instruction fine-tuning LLaMA with our own network analysis data that we collect from publicly available, real-world 5G network datasets and expanded by the self-instruct framework utilizing OpenAI’s pretrained models (PMs). Mobile-LLaMA has three main functions: Packet Analysis Function, IP Routing Analysis, and Performance Analysis Function, enabling it to provide network analysis and contribute to the automation and artificial intelligence (AI) required for 5G network management and data analysis. 
Our evaluation demonstrates Mobile-LLaMA's proficiency in network analysis code generation, achieving a score of 247 out of 300, surpassing Chat-GPT’s score of 209.

## Figures and Tables
### The Architecture of NWDAF featuring Mobile-LLaMA for 5G network analytics
<!-- ![The Architecture of NWDAF featuring Mobile-LLaMA for 5G network analytics](images/architecture.png) -->
<figure>
  <img src="images/architecture.png" alt="Manual seed task example" style="width: auto; max-width: 100%; height: auto; max-height: 60%;">
  <!-- <figcaption>Manual seed task example</figcaption> -->
</figure>

### Manual seed task example
<figure>
  <img src="images/instruction_example.png" alt="Manual seed task example" style="width: auto; max-width: 40%; height: auto; max-height: 50%;">
  <!-- <figcaption>Manual seed task example</figcaption> -->
</figure>

### Analysis Tasks in NWDAF of 5G Network with Mobile-LLaMA and Training Data Summary
| Function of Mobile-LLaMA     | Analysis Tasks                                      | Library           | Manual Instruction Tasks | Self-Instruct Generated Instructions |
|--------------------------|-----------------------------------------|-------------------|------------------------|-------------------------------------|
| Packet analysis          | Parsing IP packets<br>Data structuring<br>RTT calculation<br>Packet size examination<br>Performance assessment<br>QoS assessment | `Scapy`           | 20                     | 2000                                |
| IP routing analysis      | BGP route anomalies<br>BGP path changes       | `PyBGPStream`     | 100                    | 10000                               |
| Performance analysis     | Per-user capacity Enhancement<br>5G investment cost analysis<br>Network quality evaluation<br>UE traffic anomaly detection<br>jitter & CQI benchmarking | `Pandas`, `Matplotlib` | 30 | 3000                                |


### Overview of Performance Evaluation Analysis Tasks

### Evaluation workflow
<figure>
  <img src="images/eval_workflow.png" alt="" style="width: auto; max-width: 80%; height: auto; max-height: 60%;">
  <!-- <figcaption>Performance evaluation score: LLaMA 7B, 13B, 70, Mobile-LLaMA, Chat-GPT 3.5</figcaption> -->
</figure>


### Performance evaluation score: LLaMA 7B, 13B, 70, Mobile-LLaMA, Chat-GPT 3.5
<figure>
  <img src="images/eval_score.png" alt="Performance evaluation score: LLaMA 7B, 13B, 70, Mobile-LLaMA, Chat-GPT 3.5" style="width: auto; max-width: 80%; height: auto; max-height: 60%;">
  <!-- <figcaption>Performance evaluation score: LLaMA 7B, 13B, 70, Mobile-LLaMA, Chat-GPT 3.5</figcaption> -->
</figure>
