from Algorithm.prompt_analyzer import extract_prompt_features

# Test ambiguous 'write' usage
test_cases = [
    'Write a function to sort arrays',
    'Write an essay about climate change', 
    'Write me a summary of this article',
    'Can you write some code for me?',
    'Please write an explanation of quantum physics'
]

print("Testing context-aware 'write' handling:")
print("=" * 50)

for prompt in test_cases:
    result = extract_prompt_features(prompt)
    print(f'Prompt: "{prompt}"')
    print(f'Categories: {result["categories"]}')
    print(f'Intent: {result["intent_type"]}')
    print(f'Domain: {result["topic_domain"]}')
    print(f'Category scores: {result["_debug"]["category_scores"]}')
    print('---')
