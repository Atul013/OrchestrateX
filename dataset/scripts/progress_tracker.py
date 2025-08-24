"""
Dataset Progress Tracker for OrchestrateX
Author: Sahil (Part 2 - Dataset Creation & Model Specialty Analysis)

This script helps you track your progress and plan your next steps.
"""

import json
import os
from datetime import datetime

class ProgressTracker:
    """Track dataset progress and provide next steps"""
    
    def __init__(self):
        self.domains = [
            "coding", "creative_writing", "factual_qa", 
            "mathematical_reasoning", "language_translation", "sentiment_analysis"
        ]
        self.target_per_domain = 500
        self.total_target = self.target_per_domain * len(self.domains)
    
    def get_domain_stats(self, domain):
        """Get detailed stats for a domain"""
        filename = f"../raw_data/{domain}_prompts.json"
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
                
            count = len(prompts)
            categories = {}
            difficulties = {}
            
            for prompt in prompts:
                cat = prompt.get("category", "general")
                diff = prompt.get("difficulty", "unknown")
                categories[cat] = categories.get(cat, 0) + 1
                difficulties[diff] = difficulties.get(diff, 0) + 1
            
            return {
                "count": count,
                "progress": (count / self.target_per_domain) * 100,
                "remaining": self.target_per_domain - count,
                "categories": categories,
                "difficulties": difficulties
            }
        
        return {
            "count": 0,
            "progress": 0,
            "remaining": self.target_per_domain,
            "categories": {},
            "difficulties": {}
        }
    
    def show_overall_progress(self):
        """Show overall progress across all domains"""
        print("📊 ORCHESTRATEX DATASET PROGRESS REPORT")
        print("=" * 60)
        print(f"Target: {self.total_target} total prompts ({self.target_per_domain} per domain)")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        total_current = 0
        domain_stats = {}
        
        for domain in self.domains:
            stats = self.get_domain_stats(domain)
            domain_stats[domain] = stats
            total_current += stats["count"]
        
        overall_progress = (total_current / self.total_target) * 100
        
        print(f"\n🎯 OVERALL: {total_current}/{self.total_target} prompts ({overall_progress:.1f}%)")
        
        # Progress bar
        progress_chars = int(overall_progress / 2)  # Scale to 50 chars
        progress_bar = "█" * progress_chars + "░" * (50 - progress_chars)
        print(f"[{progress_bar}] {overall_progress:.1f}%")
        
        return domain_stats, total_current, overall_progress
    
    def show_domain_details(self, domain_stats):
        """Show detailed breakdown by domain"""
        print(f"\n📁 DOMAIN BREAKDOWN:")
        print("-" * 60)
        
        for domain, stats in domain_stats.items():
            status_emoji = "🟢" if stats["progress"] >= 100 else "🟡" if stats["progress"] >= 50 else "🔴"
            
            print(f"\n{status_emoji} {domain.upper().replace('_', ' ')}")
            print(f"   Progress: {stats['count']}/{self.target_per_domain} ({stats['progress']:.1f}%)")
            print(f"   Remaining: {stats['remaining']} prompts needed")
            print(f"   Categories: {len(stats['categories'])}")
            print(f"   Difficulties: {len(stats['difficulties'])}")
            
            if stats['categories']:
                top_categories = sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True)[:3]
                print(f"   Top categories: {', '.join([f'{cat}({count})' for cat, count in top_categories])}")
    
    def get_recommendations(self, domain_stats, overall_progress):
        """Get personalized recommendations"""
        recommendations = []
        
        # Find domains that need the most work
        sorted_domains = sorted(domain_stats.items(), key=lambda x: x[1]["count"])
        lowest_domain = sorted_domains[0]
        highest_domain = sorted_domains[-1]
        
        if overall_progress < 10:
            recommendations.append("🚀 You're just getting started! Focus on one domain at a time.")
            recommendations.append(f"📝 Start with {lowest_domain[0]} - add 50-100 prompts to build momentum.")
            recommendations.append("💡 Use the expansion plans in processed_data/ as your guide.")
        
        elif overall_progress < 25:
            recommendations.append("📈 Good progress! Keep the momentum going.")
            recommendations.append(f"🎯 Focus on {lowest_domain[0]} to catch up with other domains.")
            recommendations.append("🔄 Add variety: different difficulties and categories.")
        
        elif overall_progress < 50:
            recommendations.append("💪 You're making solid progress!")
            recommendations.append("🤖 Consider starting to test prompts with AI models.")
            recommendations.append("📊 Review prompt quality and remove duplicates.")
        
        elif overall_progress < 75:
            recommendations.append("🌟 Excellent progress! You're in the home stretch.")
            recommendations.append("🧪 Start collecting responses from AI models.")
            recommendations.append("👥 Begin planning human evaluation process.")
        
        else:
            recommendations.append("🎉 Amazing! You're almost done with data collection!")
            recommendations.append("🤖 Focus on collecting AI model responses.")
            recommendations.append("📋 Set up human evaluation and rating system.")
        
        # Domain-specific recommendations
        for domain, stats in domain_stats.items():
            if stats["count"] == 0:
                recommendations.append(f"❗ {domain} needs immediate attention - zero prompts!")
            elif stats["count"] < 50:
                recommendations.append(f"📝 {domain} needs more prompts ({stats['count']}/500)")
            elif len(stats["categories"]) < 5:
                recommendations.append(f"🎨 {domain} needs more variety in categories")
        
        return recommendations
    
    def generate_action_plan(self, domain_stats):
        """Generate specific action plan"""
        action_plan = []
        
        # Immediate tasks (next 7 days)
        action_plan.append("📅 THIS WEEK:")
        sorted_domains = sorted(domain_stats.items(), key=lambda x: x[1]["count"])
        for domain, stats in sorted_domains[:2]:  # Focus on 2 lowest domains
            needed = min(100, stats["remaining"])  # Add up to 100 prompts
            action_plan.append(f"   • Add {needed} prompts to {domain}")
        
        # Medium-term tasks (next 2-4 weeks)
        action_plan.append("\n📅 NEXT 2-4 WEEKS:")
        action_plan.append("   • Research more data sources for each domain")
        action_plan.append("   • Set up API connections to AI models")
        action_plan.append("   • Create response collection system")
        action_plan.append("   • Plan human evaluation process")
        
        # Long-term tasks (next month+)
        action_plan.append("\n📅 NEXT MONTH:")
        action_plan.append("   • Collect responses from all 5 AI models")
        action_plan.append("   • Conduct human evaluations")
        action_plan.append("   • Create final structured dataset")
        action_plan.append("   • Prepare dataset for ML algorithm training")
        
        return action_plan
    
    def save_progress_report(self, domain_stats, total_current, overall_progress):
        """Save progress report to file"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "overall_progress": {
                "current_prompts": total_current,
                "target_prompts": self.total_target,
                "progress_percentage": overall_progress
            },
            "domain_stats": domain_stats,
            "recommendations": self.get_recommendations(domain_stats, overall_progress),
            "action_plan": self.generate_action_plan(domain_stats)
        }
        
        # Ensure directory exists
        os.makedirs("../processed_data", exist_ok=True)
        
        filename = f"../processed_data/progress_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Progress report saved: {filename}")
        return report

def main():
    """Main function"""
    tracker = ProgressTracker()
    
    # Show overall progress
    domain_stats, total_current, overall_progress = tracker.show_overall_progress()
    
    # Show domain details
    tracker.show_domain_details(domain_stats)
    
    # Get recommendations
    recommendations = tracker.get_recommendations(domain_stats, overall_progress)
    print(f"\n💡 RECOMMENDATIONS FOR SAHIL:")
    print("-" * 40)
    for rec in recommendations:
        print(f"   {rec}")
    
    # Show action plan
    action_plan = tracker.generate_action_plan(domain_stats)
    print(f"\n📋 ACTION PLAN:")
    print("-" * 40)
    for item in action_plan:
        print(item)
    
    # Save report
    report = tracker.save_progress_report(domain_stats, total_current, overall_progress)
    
    print(f"\n🎯 NEXT STEPS:")
    print("1. Use prompt_adder.py to add more prompts")
    print("2. Follow the action plan above")
    print("3. Run this tracker daily to monitor progress")
    print("4. Move to model response collection when ready")

if __name__ == "__main__":
    main()
