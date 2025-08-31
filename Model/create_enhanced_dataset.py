#!/usr/bin/env python3
"""
Enhanced Dataset Creator with 5000 realistic samples
"""

import pandas as pd
import numpy as np
from prompt_analyzer import extract_prompt_features

def create_enhanced_large_dataset(n_samples=5000):
    """Create a large, realistic dataset with clear model selection patterns."""
    
    print(f"🔥 Creating enhanced dataset with {n_samples} samples...")
    
    # Expanded and categorized prompts for realistic patterns
    coding_prompts = [
        "Write a Python function to implement binary search",
        "Create a REST API using Flask/Django",
        "Optimize this SQL query for better performance", 
        "Debug this JavaScript React component",
        "Implement a machine learning model in TensorFlow",
        "Set up a Docker container for microservices",
        "Build a web scraper using BeautifulSoup",
        "Create a database schema for e-commerce",
        "Write unit tests for this Python class",
        "Implement authentication with JWT tokens",
        "Build a GraphQL API with Node.js",
        "Create a CI/CD pipeline with GitHub Actions",
        "Optimize memory usage in this algorithm",
        "Write a regex pattern to validate emails",
        "Implement caching with Redis",
        "Create a responsive CSS layout",
        "Build a chatbot using NLP libraries",
        "Write async/await functions in JavaScript",
        "Implement data structures like linked lists",
        "Create API documentation with Swagger"
    ]
    
    reasoning_prompts = [
        "Analyze the pros and cons of remote work",
        "Evaluate the economic impact of AI automation",
        "Compare different investment strategies for retirement", 
        "Explain the root causes of climate change",
        "Argue for or against universal basic income",
        "Solve this complex logic puzzle step by step",
        "Analyze market trends in cryptocurrency",
        "Evaluate the ethics of genetic engineering",
        "Compare democratic vs authoritarian governance",
        "Assess the impact of social media on society",
        "Analyze the geopolitical implications of trade wars",
        "Evaluate different approaches to healthcare systems",
        "Compare renewable vs fossil fuel energy strategies",
        "Analyze the psychological effects of remote learning",
        "Evaluate the effectiveness of various marketing strategies",
        "Assess the long-term impacts of urbanization",
        "Compare different philosophical approaches to ethics",
        "Analyze the economic effects of immigration policies",
        "Evaluate the pros and cons of nuclear energy",
        "Assess the impact of automation on employment"
    ]
    
    creative_prompts = [
        "Write a short story about time travel",
        "Generate creative ideas for a marketing campaign",
        "Create an innovative meal plan for weight loss",
        "Design a user interface for a meditation app",
        "Compose a poem about technological progress",
        "Brainstorm solutions to reduce plastic waste",
        "Write a compelling product description",
        "Create a fictional world with unique rules",
        "Design a logo concept for a startup",
        "Write dialogue for a dramatic scene",
        "Create a brand story for eco-friendly products",
        "Design a game concept with unique mechanics",
        "Write a persuasive speech about climate action",
        "Create a social media content strategy",
        "Design an innovative workspace layout",
        "Write a children's book story outline",
        "Create a video script for product demonstration",
        "Design a mobile app user experience flow",
        "Write compelling email subject lines",
        "Create a podcast episode concept"
    ]
    
    technical_prompts = [
        "Explain how blockchain consensus mechanisms work",
        "Compare different cloud computing architectures",
        "Analyze network security vulnerabilities and mitigation",
        "Review quantum computing developments and applications",
        "Evaluate different database management systems",
        "Assess the performance of various sorting algorithms",
        "Compare microservices vs monolithic architectures",
        "Explain distributed systems design patterns",
        "Analyze cybersecurity threat landscapes",
        "Compare different machine learning frameworks",
        "Evaluate edge computing vs cloud computing",
        "Explain container orchestration with Kubernetes",
        "Analyze big data processing frameworks",
        "Compare different API design paradigms",
        "Evaluate serverless computing architectures",
        "Explain cryptocurrency mining mechanisms",
        "Analyze software testing methodologies",
        "Compare different version control strategies",
        "Evaluate data warehouse design approaches",
        "Explain neural network architectures"
    ]
    
    general_prompts = [
        "What's the best way to learn a new language?",
        "How do I improve my productivity at work?",
        "What are some healthy breakfast recipes?",
        "Help me plan a budget-friendly vacation",
        "Explain photosynthesis in simple terms",
        "What should I wear to a job interview?",
        "How do I start a small business?",
        "What are the benefits of regular exercise?",
        "How do I improve my public speaking skills?",
        "What are some good book recommendations?",
        "How do I manage stress effectively?",
        "What are the basics of personal finance?",
        "How do I maintain work-life balance?",
        "What are some effective study techniques?",
        "How do I build confidence and self-esteem?",
        "What are the signs of a healthy relationship?",
        "How do I choose the right career path?",
        "What are some tips for better sleep?",
        "How do I develop leadership skills?",
        "What are some sustainable living practices?"
    ]
    
    def enhanced_model_selection(features, prompt_text, category):
        """
        Realistic model selection based on actual model strengths.
        This creates clear, learnable patterns for the ML model.
        """
        
        prompt_lower = prompt_text.lower()
        
        # CODING TASKS - TNG DeepSeek excels at code
        if category == 'coding':
            # Python/ML coding -> TNG DeepSeek (70%)
            if any(word in prompt_lower for word in ['python', 'tensorflow', 'pytorch', 'pandas', 'numpy']):
                return np.random.choice(['TNG DeepSeek', 'GLM4.5', 'GPT-OSS'], p=[0.7, 0.2, 0.1])
            
            # Web development -> TNG DeepSeek (65%)  
            elif any(word in prompt_lower for word in ['javascript', 'react', 'node', 'api', 'web']):
                return np.random.choice(['TNG DeepSeek', 'GPT-OSS', 'GLM4.5'], p=[0.65, 0.25, 0.1])
            
            # Database/SQL -> GLM4.5 (60%)
            elif any(word in prompt_lower for word in ['sql', 'database', 'schema', 'query']):
                return np.random.choice(['GLM4.5', 'TNG DeepSeek', 'Qwen3'], p=[0.6, 0.3, 0.1])
            
            # General coding -> TNG DeepSeek (60%)
            else:
                return np.random.choice(['TNG DeepSeek', 'GLM4.5', 'GPT-OSS'], p=[0.6, 0.25, 0.15])
        
        # REASONING/ANALYSIS - GLM4.5 for complex analysis
        elif category == 'reasoning':
            # Economic/Financial analysis -> GLM4.5 (70%)
            if any(word in prompt_lower for word in ['economic', 'financial', 'investment', 'market']):
                return np.random.choice(['GLM4.5', 'Qwen3', 'GPT-OSS'], p=[0.7, 0.2, 0.1])
            
            # Logical reasoning -> Qwen3 (65%)
            elif any(word in prompt_lower for word in ['logic', 'puzzle', 'proof', 'theorem']):
                return np.random.choice(['Qwen3', 'GLM4.5', 'GPT-OSS'], p=[0.65, 0.25, 0.1])
            
            # Social analysis -> GLM4.5 (60%)
            elif any(word in prompt_lower for word in ['social', 'society', 'political', 'ethical']):
                return np.random.choice(['GLM4.5', 'GPT-OSS', 'MoonshotAI Kimi'], p=[0.6, 0.25, 0.15])
            
            # General reasoning -> GLM4.5 (55%)
            else:
                return np.random.choice(['GLM4.5', 'GPT-OSS', 'Qwen3'], p=[0.55, 0.3, 0.15])
        
        # CREATIVE TASKS - GPT-OSS for creativity
        elif category == 'creative':
            # Writing/Content -> GPT-OSS (75%)
            if any(word in prompt_lower for word in ['write', 'story', 'content', 'script', 'poem']):
                return np.random.choice(['GPT-OSS', 'MoonshotAI Kimi', 'GLM4.5'], p=[0.75, 0.15, 0.1])
            
            # Marketing/Branding -> GPT-OSS (70%)
            elif any(word in prompt_lower for word in ['marketing', 'brand', 'campaign', 'social media']):
                return np.random.choice(['GPT-OSS', 'MoonshotAI Kimi', 'GLM4.5'], p=[0.7, 0.2, 0.1])
            
            # Design concepts -> MoonshotAI Kimi (60%)
            elif any(word in prompt_lower for word in ['design', 'ui', 'ux', 'interface', 'layout']):
                return np.random.choice(['MoonshotAI Kimi', 'GPT-OSS', 'GLM4.5'], p=[0.6, 0.3, 0.1])
            
            # General creative -> GPT-OSS (65%)
            else:
                return np.random.choice(['GPT-OSS', 'MoonshotAI Kimi', 'GLM4.5'], p=[0.65, 0.25, 0.1])
        
        # TECHNICAL ANALYSIS - GLM4.5 for deep technical knowledge
        elif category == 'technical':
            # Architecture/Systems -> GLM4.5 (75%)
            if any(word in prompt_lower for word in ['architecture', 'system', 'distributed', 'microservices']):
                return np.random.choice(['GLM4.5', 'Qwen3', 'TNG DeepSeek'], p=[0.75, 0.15, 0.1])
            
            # Security -> Qwen3 (70%)
            elif any(word in prompt_lower for word in ['security', 'cybersecurity', 'encryption', 'vulnerability']):
                return np.random.choice(['Qwen3', 'GLM4.5', 'TNG DeepSeek'], p=[0.7, 0.2, 0.1])
            
            # Cloud/Infrastructure -> GLM4.5 (65%)
            elif any(word in prompt_lower for word in ['cloud', 'aws', 'azure', 'kubernetes', 'docker']):
                return np.random.choice(['GLM4.5', 'TNG DeepSeek', 'Qwen3'], p=[0.65, 0.25, 0.1])
            
            # General technical -> GLM4.5 (60%)
            else:
                return np.random.choice(['GLM4.5', 'Qwen3', 'TNG DeepSeek'], p=[0.6, 0.25, 0.15])
        
        # GENERAL QUESTIONS - GPT-OSS as the generalist
        else:
            # Lifestyle/Personal -> MoonshotAI Kimi (60%)
            if any(word in prompt_lower for word in ['lifestyle', 'health', 'fitness', 'relationship', 'personal']):
                return np.random.choice(['MoonshotAI Kimi', 'GPT-OSS', 'Llama 4 Maverick'], p=[0.6, 0.25, 0.15])
            
            # Business/Career -> GPT-OSS (65%)
            elif any(word in prompt_lower for word in ['business', 'career', 'job', 'interview', 'leadership']):
                return np.random.choice(['GPT-OSS', 'GLM4.5', 'MoonshotAI Kimi'], p=[0.65, 0.2, 0.15])
            
            # Educational -> Llama 4 Maverick (60%)
            elif any(word in prompt_lower for word in ['learn', 'study', 'education', 'explain', 'teach']):
                return np.random.choice(['Llama 4 Maverick', 'GPT-OSS', 'MoonshotAI Kimi'], p=[0.6, 0.25, 0.15])
            
            # General questions -> GPT-OSS (70%)
            else:
                return np.random.choice(['GPT-OSS', 'MoonshotAI Kimi', 'Llama 4 Maverick'], p=[0.7, 0.2, 0.1])
    
    # Create the dataset
    data = []
    np.random.seed(42)  # For reproducibility
    
    prompt_categories = [
        (coding_prompts, 'coding'),
        (reasoning_prompts, 'reasoning'), 
        (creative_prompts, 'creative'),
        (technical_prompts, 'technical'),
        (general_prompts, 'general')
    ]
    
    samples_per_category = n_samples // len(prompt_categories)
    
    for prompts, category in prompt_categories:
        for i in range(samples_per_category):
            # Select base prompt and add variation
            base_prompt = np.random.choice(prompts)
            variation = np.random.randint(1, 1000)
            prompt = f"{base_prompt} (variation {variation})"
            
            # Extract features using existing analyzer
            features = extract_prompt_features(prompt)
            
            # Use enhanced selection logic
            best_model = enhanced_model_selection(features, prompt, category)
            
            data.append({
                'prompt': prompt,
                'categories': features['categories'],
                'topic_domain': features['topic_domain'],
                'intent_type': features['intent_type'],
                'confidence': features['confidence'],
                'token_count': features['token_count'],
                'best_model': best_model,
                'true_category': category  # Add for analysis
            })
    
    # Fill remaining samples with mixed categories
    remaining = n_samples - len(data)
    for i in range(remaining):
        all_prompts = [p for prompts, _ in prompt_categories for p in prompts]
        base_prompt = np.random.choice(all_prompts)
        prompt = f"{base_prompt} (mixed {i})"
        
        features = extract_prompt_features(prompt)
        
        # Determine category from features
        if 'coding' in features['categories']:
            category = 'coding'
        elif 'reasoning' in features['categories']:
            category = 'reasoning'
        elif features['topic_domain'] == 'technical':
            category = 'technical'
        else:
            category = 'general'
        
        best_model = enhanced_model_selection(features, prompt, category)
        
        data.append({
            'prompt': prompt,
            'categories': features['categories'],
            'topic_domain': features['topic_domain'],
            'intent_type': features['intent_type'],
            'confidence': features['confidence'],
            'token_count': features['token_count'],
            'best_model': best_model,
            'true_category': category
        })
    
    df = pd.DataFrame(data)
    
    print(f"✅ Created {len(df)} samples")
    print(f"📊 Model distribution:")
    print(df['best_model'].value_counts())
    print(f"📊 Category distribution:")
    print(df['true_category'].value_counts())
    
    return df

if __name__ == "__main__":
    # Create the enhanced dataset
    df = create_enhanced_large_dataset(5000)
    
    # Save to CSV
    df.to_csv('enhanced_dataset_5000.csv', index=False)
    print(f"\n💾 Saved to enhanced_dataset_5000.csv")
    
    # Quick preview
    print(f"\n👀 Sample data:")
    print(df[['prompt', 'best_model', 'true_category']].head(10))
