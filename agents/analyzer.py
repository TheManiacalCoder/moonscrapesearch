import os
import json
import aiohttp
import asyncio
from config.manager import ConfigManager
from pathlib import Path
from colorama import Fore, Style

class OpenRouterAnalyzer:
    def __init__(self, db):
        self.config = ConfigManager()
        self.db = db
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.config.openrouter_api_key}",
            "Content-Type": "application/json"
        }
        self.analysis_folder = Path("analysis")
        self.analysis_folder.mkdir(exist_ok=True)

    async def analyze_urls(self, filtered_content: dict):
        try:
            print(f"{Fore.CYAN}Performing comprehensive SEO analysis...{Style.RESET_ALL}")
            
            if "final_summary" not in filtered_content:
                raise ValueError("Expected final summary data")
                
            summary = filtered_content["final_summary"]
            
            prompt = f"""
            Perform a comprehensive SEO analysis of this content:
            {summary}
            
            Include:
            1. Key SEO opportunities
            2. Content structure improvements
            3. Keyword optimization suggestions
            4. Engagement strategies
            5. Technical SEO considerations
            6. Content gap analysis
            7. Backlink opportunities
            """
            
            payload = {
                "model": self.config.ai_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "max_tokens": 3000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, headers=self.headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        error = await response.text()
                        raise Exception(f"OpenRouter API error: {error}")
                        
        except Exception as e:
            print(f"{Fore.RED}Error during analysis: {e}{Style.RESET_ALL}")
            return None

    def _get_content_for_url(self, url):
        # Implement content retrieval from your database or storage
        pass

    async def save_report(self, report):
        report_path = self.analysis_folder / "aggregated_analysis.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"{Fore.GREEN}Aggregated report saved to {report_path}{Style.RESET_ALL}")

async def main(urls):
    analyzer = OpenRouterAnalyzer()
    report = await analyzer.analyze_urls(urls)
    if report:
        await analyzer.save_report(report)

# Example usage
if __name__ == "__main__":
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3",
        "https://example.com/page4",
        "https://example.com/page5"
    ]
    asyncio.run(main(urls)) 