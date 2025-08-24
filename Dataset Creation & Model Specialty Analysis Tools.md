# Sahil's Complete Guide to Dataset Creation & Model Specialty Analysis

## 🎯 Your Mission
As **Sahil**, you're responsible for building comprehensive training datasets that capture each chatbot's strengths and weaknesses across different domains.

## 📊 Current Status
- **Overall Progress**: 3.5% (105/3000 prompts)
- **Target**: 500 prompts per domain × 6 domains = 3000 total prompts
- **Priority Domains**: Mathematical reasoning and language translation need immediate attention

## 🛠️ Tools You Have Created

### 1. **simple_data_collector.py** - ✅ COMPLETED
- Creates initial dataset structure
- Generates sample prompts for all domains
- **Usage**: `python simple_data_collector.py`

### 2. **expansion_guide.py** - ✅ COMPLETED  
- Creates detailed expansion plans for each domain
- Provides categories, difficulty levels, and data sources
- **Usage**: `python expansion_guide.py`

### 3. **prompt_adder.py** - ✅ COMPLETED
- Adds new prompts to existing datasets
- Includes sample prompt collections
- **Usage**: `python prompt_adder.py`

### 4. **progress_tracker.py** - ✅ COMPLETED
- Tracks progress across all domains
- Provides recommendations and action plans
- **Usage**: `python progress_tracker.py`

## 📋 Step-by-Step Roadmap

### **PHASE 1: BASIC LEVEL (Week 1-2)**
✅ **DONE**: Set up initial dataset structure with 10 prompts per domain

**NEXT IMMEDIATE TASKS:**
1. **Focus on Mathematical Reasoning** (currently 10/500 prompts)
   - Add prompts for: basic arithmetic, algebra, geometry, word problems
   - Use categories from expansion plan
   - Target: 100 prompts this week

2. **Focus on Language Translation** (currently 10/500 prompts) 
   - Add prompts for: Spanish, French, German, Chinese translations
   - Include formal/informal text, business phrases
   - Target: 100 prompts this week

**How to add prompts:**
```bash
cd c:\Users\91903\OrchestrateX\dataset\scripts
python prompt_adder.py
# Choose option 2 to see examples, then modify the script to add your own
```

### **PHASE 2: INTERMEDIATE LEVEL (Week 3-4)**
1. **Expand All Domains to 100+ prompts each**
   - Coding: Add web development, algorithms, debugging prompts
   - Creative Writing: Add different genres, poetry, dialogue
   - Factual Q&A: Add science, history, technology questions
   - Sentiment Analysis: Add product reviews, social media posts

2. **Add Difficulty Levels**
   - Easy, Medium, Hard for each domain
   - Ensure good distribution across difficulty levels

3. **Research Data Sources**
   - Check expansion plans for recommended sources
   - LeetCode, HackerRank for coding
   - r/WritingPrompts for creative writing
   - Wikipedia, textbooks for factual Q&A

### **PHASE 3: ADVANCED LEVEL (Week 5-8)**
1. **Reach Target of 500 prompts per domain**
   - Focus on variety and quality
   - Multiple categories per domain
   - Different question types and formats

2. **Start Model Response Collection**
   - Set up API connections to AI models:
     - GLM4.5
     - GPT-OSS
     - LLaMa 3
     - Gemini2.5
     - Claude 3.5
     - Falcon
   - Collect responses for identical prompts

3. **Human Evaluation Setup**
   - Create evaluation criteria (accuracy, relevance, clarity, creativity)
   - Set up rating system (1-5 Likert scale)
   - Plan for multiple human evaluators

### **PHASE 4: EXPERT LEVEL (Week 9-12)**
1. **Quality Assurance**
   - Remove duplicate prompts
   - Ensure prompt quality and clarity
   - Validate domain classifications

2. **Dataset Structuring**
   - Format final dataset as specified in `response_evaluation.md`
   - Create train/validation/test splits (70/15/15)
   - Generate metadata and documentation

3. **Handoff Preparation**
   - Prepare dataset for Avinash (Part 3 - ML Algorithm)
   - Document evaluation methodology
   - Create usage guidelines

## 📁 File Structure You've Created
```
dataset/
├── raw_data/               # Your prompt collections
│   ├── coding_prompts.json
│   ├── creative_writing_prompts.json
│   ├── factual_qa_prompts.json
│   ├── mathematical_reasoning_prompts.json
│   ├── language_translation_prompts.json
│   └── sentiment_analysis_prompts.json
├── processed_data/         # Analysis and planning files
│   ├── *_expansion_plan.json
│   └── progress_report_*.json
└── scripts/               # Your tools
    ├── simple_data_collector.py
    ├── expansion_guide.py
    ├── prompt_adder.py
    └── progress_tracker.py
```

## 🎯 Daily Workflow
1. **Start each day**: Run `python progress_tracker.py`
2. **Add prompts**: Use `python prompt_adder.py` or modify it
3. **Track progress**: Check how close you are to daily/weekly targets
4. **Focus**: Work on the domain that needs the most attention

## 📊 Key Metrics to Track
- **Total prompts**: Current 105/3000 (3.5%)
- **Domain balance**: Keep all domains roughly equal
- **Category diversity**: 5+ categories per domain
- **Difficulty spread**: Mix of easy, medium, hard prompts
- **Quality**: Clear, specific, testable prompts

## 🚨 Priority Actions This Week
1. **Mathematical Reasoning**: Add 90 more prompts (target: 100 total)
2. **Language Translation**: Add 90 more prompts (target: 100 total)  
3. **Sentiment Analysis**: Add 40 more prompts (target: 50 total)

## 💡 Pro Tips
- **Start small**: Add 10-20 prompts at a time
- **Use templates**: Modify existing prompts rather than starting from scratch
- **Check quality**: Each prompt should be clear and testable
- **Think variety**: Different formats, difficulties, and styles
- **Document everything**: Keep track of sources and methodology

## 🤝 Collaboration Points
- **With Zayed (Part 1)**: Understand API requirements for model testing
- **With Avinash (Part 3)**: Prepare dataset format for ML algorithm
- **With Jinu (Part 4)**: Plan integration with orchestration engine
- **With Atul (Part 5)**: Prepare for testing and validation

## 🎉 Success Criteria
By the end of your work, you should have:
- ✅ 3000+ high-quality prompts across 6 domains
- ✅ Responses from all 6 AI models for each prompt
- ✅ Human evaluation ratings for response quality
- ✅ Structured dataset ready for ML training
- ✅ Documentation of methodology and evaluation criteria

---

**You're doing great! Keep the momentum going and focus on one domain at a time. The tools you've built will help you track progress and stay organized.**

*Next run: `python progress_tracker.py` to see your current status and get updated recommendations.*
