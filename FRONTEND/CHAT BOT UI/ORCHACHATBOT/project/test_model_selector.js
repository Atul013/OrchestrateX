// Test the model selector algorithm
import { modelSelector } from './src/services/modelSelector.js';

console.log('🧠 Testing ModelSelector Algorithm');
console.log('=' * 50);

const testPrompts = [
    "Write a Python function to sort arrays",
    "Tell me a creative story about robots", 
    "Explain quantum physics in simple terms",
    "Help me debug this JavaScript code",
    "Analyze the economic implications of AI",
    "What's the best way to learn programming?"
];

testPrompts.forEach((prompt, index) => {
    console.log(`\n📝 Test ${index + 1}: "${prompt}"`);
    const result = modelSelector.selectBestModel(prompt);
    console.log(`🎯 Selected: ${result.selectedModel}`);
    console.log(`📊 Confidence: ${result.confidence.toFixed(3)}`);
    console.log(`💡 Reasoning: ${result.reasoning}`);
    console.log(`📈 Top 3 scores:`);
    
    const sortedScores = Object.entries(result.allScores)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 3);
    
    sortedScores.forEach(([model, score], i) => {
        console.log(`   ${i + 1}. ${model}: ${score.toFixed(3)}`);
    });
});