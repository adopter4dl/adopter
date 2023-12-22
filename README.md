# Adopter: Automated Deep Learning Optimization via DSL-based Source Code Transformation

```
├── dsl.py              Domain Specific Langiage definition 
|                       and model structure abstraction 
├── pattern_matcher.py  Pattern matching
├── refactor.py         Synthesis-based code transformation
├── ...
├── benchmarks.ipynb    Benchmarking Optimization Rules  
├── results/            Generated patches and statistic results
└── models              Hugging Face models used for evaluation

```

## Reproduce experiment results

```
cd results
python3 compare.py
```