"""
Solutions Research Agent

This agent specializes in researching and identifying data analytics and AI solutions
that can be provided to clients based on their industry problems and business needs.
"""

import os
from typing import List, Dict, Any
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Solution:
    """Data structure for AI and data analytics solutions."""
    solution_name: str
    solution_description: str
    problem_solved: str
    technology_stack: List[str]
    implementation_time: str
    cost_range: str
    roi_estimate: str
    use_cases: List[str]
    success_metrics: List[str]
    industry_applicability: List[str]

class SolutionsAgent:
    """Agent specialized in researching AI and data analytics solutions."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.agent_type = "Solutions Research Specialist"
        
    def research_solutions_for_problems(self, 
                                      industry_problems: List[str],
                                      company_industry: str,
                                      company_size: str = "Unknown") -> List[Solution]:
        """
        Research AI and data analytics solutions for identified industry problems.
        
        Args:
            industry_problems: List of identified industry problems
            company_industry: The industry sector
            company_size: Company size category
            
        Returns:
            List of relevant solutions
        """
        
        # Define solution frameworks based on problems
        base_solutions = self._get_solution_framework(industry_problems, company_industry)
        
        # Enhance with AI-generated insights
        enhanced_solutions = self._enhance_solutions_with_ai(
            base_solutions, industry_problems, company_industry, company_size
        )
        
        return enhanced_solutions
    
    def _get_solution_framework(self, problems: List[str], industry: str) -> List[Solution]:
        """Get base solution framework based on problems and industry."""
        
        solutions = []
        
        # Regulatory Compliance Solutions
        if any("compliance" in p.lower() or "regulatory" in p.lower() for p in problems):
            solutions.append(
                Solution(
                    solution_name="AI-Powered Compliance Monitoring",
                    solution_description="Automated monitoring and reporting system for regulatory compliance",
                    problem_solved="Regulatory compliance complexity and documentation",
                    technology_stack=["Machine Learning", "Natural Language Processing", "Automation", "Cloud Computing"],
                    implementation_time="3-6 months",
                    cost_range="$50K - $200K",
                    roi_estimate="200-400% within 18 months",
                    use_cases=["Environmental compliance", "Financial regulations", "Healthcare standards"],
                    success_metrics=["Reduced compliance violations", "Faster reporting", "Cost savings"],
                    industry_applicability=["Environmental Services", "Finance", "Healthcare", "Manufacturing"]
                )
            )
        
        # Cost Management Solutions
        if any("cost" in p.lower() or "management" in p.lower() for p in problems):
            solutions.append(
                Solution(
                    solution_name="Predictive Cost Analytics",
                    solution_description="AI-driven cost prediction and optimization platform",
                    problem_solved="Rising operational costs and cost management",
                    technology_stack=["Predictive Analytics", "Machine Learning", "Data Visualization", "Real-time Monitoring"],
                    implementation_time="2-4 months",
                    cost_range="$30K - $150K",
                    roi_estimate="150-300% within 12 months",
                    use_cases=["Budget forecasting", "Cost optimization", "Resource allocation"],
                    success_metrics=["Reduced operational costs", "Improved budget accuracy", "Better resource utilization"],
                    industry_applicability=["All sectors"]
                )
            )
        
        # Supply Chain Solutions
        if any("supply chain" in p.lower() or "disruption" in p.lower() for p in problems):
            solutions.append(
                Solution(
                    solution_name="Supply Chain Intelligence Platform",
                    solution_description="Real-time supply chain monitoring and optimization system",
                    problem_solved="Supply chain disruption and material shortages",
                    technology_stack=["IoT", "Machine Learning", "Predictive Analytics", "Blockchain"],
                    implementation_time="4-8 months",
                    cost_range="$100K - $500K",
                    roi_estimate="300-500% within 24 months",
                    use_cases=["Inventory optimization", "Supplier risk assessment", "Demand forecasting"],
                    success_metrics=["Reduced supply chain delays", "Lower inventory costs", "Improved supplier relationships"],
                    industry_applicability=["Manufacturing", "Retail", "Logistics", "Construction"]
                )
            )
        
        # Cybersecurity Solutions
        if any("cybersecurity" in p.lower() or "security" in p.lower() for p in problems):
            solutions.append(
                Solution(
                    solution_name="AI-Powered Threat Detection",
                    solution_description="Advanced cybersecurity monitoring and response system",
                    problem_solved="Cybersecurity threats and data breaches",
                    technology_stack=["Machine Learning", "Behavioral Analytics", "Threat Intelligence", "Automation"],
                    implementation_time="2-5 months",
                    cost_range="$75K - $300K",
                    roi_estimate="400-600% within 12 months",
                    use_cases=["Threat detection", "Incident response", "Vulnerability assessment"],
                    success_metrics=["Reduced security incidents", "Faster threat response", "Lower breach costs"],
                    industry_applicability=["Finance", "Healthcare", "Technology", "All sectors"]
                )
            )
        
        # Sustainability Solutions
        if any("sustainability" in p.lower() or "environmental" in p.lower() for p in problems):
            solutions.append(
                Solution(
                    solution_name="Sustainability Analytics Platform",
                    solution_description="Comprehensive sustainability monitoring and reporting system",
                    problem_solved="Sustainability pressures and environmental compliance",
                    technology_stack=["IoT Sensors", "Data Analytics", "Machine Learning", "Reporting Tools"],
                    implementation_time="3-6 months",
                    cost_range="$40K - $180K",
                    roi_estimate="180-350% within 18 months",
                    use_cases=["Carbon footprint tracking", "Resource optimization", "Sustainability reporting"],
                    success_metrics=["Reduced environmental impact", "Cost savings", "Improved compliance"],
                    industry_applicability=["Environmental Services", "Manufacturing", "Energy", "All sectors"]
                )
            )
        
        # Digital Transformation Solutions
        if any("digital" in p.lower() or "transformation" in p.lower() for p in problems):
            solutions.append(
                Solution(
                    solution_name="Digital Transformation Accelerator",
                    solution_description="Comprehensive digital transformation platform",
                    problem_solved="Digital transformation and legacy system modernization",
                    technology_stack=["Cloud Computing", "API Integration", "Process Automation", "Data Migration"],
                    implementation_time="6-12 months",
                    cost_range="$200K - $1M+",
                    roi_estimate="250-400% within 36 months",
                    use_cases=["Legacy system modernization", "Process automation", "Cloud migration"],
                    success_metrics=["Improved operational efficiency", "Reduced costs", "Enhanced customer experience"],
                    industry_applicability=["All sectors"]
                )
            )
        
        # If no specific problems match, provide general solutions
        if not solutions:
            solutions.extend([
                Solution(
                    solution_name="Business Intelligence Dashboard",
                    solution_description="Comprehensive business analytics and reporting platform",
                    problem_solved="General business intelligence and decision making",
                    technology_stack=["Data Analytics", "Visualization", "Real-time Monitoring", "Cloud Computing"],
                    implementation_time="2-4 months",
                    cost_range="$25K - $100K",
                    roi_estimate="120-250% within 12 months",
                    use_cases=["Performance monitoring", "KPI tracking", "Decision support"],
                    success_metrics=["Improved decision making", "Better performance visibility", "Increased efficiency"],
                    industry_applicability=["All sectors"]
                ),
                Solution(
                    solution_name="Customer Analytics Platform",
                    solution_description="AI-powered customer behavior analysis and insights",
                    problem_solved="Customer understanding and market competition",
                    technology_stack=["Machine Learning", "Predictive Analytics", "Customer Segmentation", "Behavioral Analysis"],
                    implementation_time="3-5 months",
                    cost_range="$35K - $150K",
                    roi_estimate="180-320% within 15 months",
                    use_cases=["Customer segmentation", "Churn prediction", "Personalization"],
                    success_metrics=["Improved customer retention", "Increased sales", "Better customer experience"],
                    industry_applicability=["Retail", "E-commerce", "Services", "All sectors"]
                )
            ])
        
        return solutions
    
    def _enhance_solutions_with_ai(self, 
                                  base_solutions: List[Solution],
                                  problems: List[str],
                                  industry: str,
                                  company_size: str) -> List[Solution]:
        """Enhance solutions with AI-generated insights."""
        
        try:
            # Create context for AI enhancement
            context = f"""
            Industry: {industry}
            Company Size: {company_size}
            
            Identified Problems:
            {chr(10).join([f"- {p}" for p in problems])}
            
            Base Solutions:
            {chr(10).join([f"- {s.solution_name}: {s.solution_description}" for s in base_solutions])}
            
            Please enhance these solutions with:
            1. Additional industry-specific solutions
            2. Emerging technologies relevant to this industry
            3. Customization options for {company_size} companies
            4. Integration possibilities with existing systems
            5. Competitive advantages and differentiators
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a technology consultant specializing in AI and data analytics solutions for business problems."},
                    {"role": "user", "content": context}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse AI response and enhance solutions
            ai_insights = response.choices[0].message.content
            
            # Add AI-enhanced solutions
            enhanced_solutions = base_solutions.copy()
            
            # Create additional solution from AI insights
            if "emerging" in ai_insights.lower() or "technology" in ai_insights.lower():
                enhanced_solutions.append(
                    Solution(
                        solution_name="AI-Enhanced Custom Solution",
                        solution_description=f"AI-recommended solution: {ai_insights[:200]}...",
                        problem_solved="Custom industry-specific challenges",
                        technology_stack=["AI/ML", "Custom Development", "Industry APIs"],
                        implementation_time="4-8 months",
                        cost_range="$80K - $300K",
                        roi_estimate="200-400% within 18 months",
                        use_cases=["Industry-specific automation", "Custom analytics", "Process optimization"],
                        success_metrics=["Customized solutions", "Industry fit", "Competitive advantage"],
                        industry_applicability=[industry]
                    )
                )
            
            return enhanced_solutions
            
        except Exception as e:
            print(f"AI enhancement failed: {e}")
            return base_solutions
    
    def get_solutions_summary(self, solutions: List[Solution]) -> str:
        """Generate a summary of identified solutions."""
        
        if not solutions:
            return "No solutions identified."
        
        summary = f"**AI & Data Analytics Solutions Analysis**\n\n"
        summary += f"**Total Solutions Identified:** {len(solutions)}\n\n"
        
        for i, solution in enumerate(solutions, 1):
            summary += f"**{i}. {solution.solution_name}**\n"
            summary += f"   - **Problem Solved:** {solution.problem_solved}\n"
            summary += f"   - **Description:** {solution.solution_description}\n"
            summary += f"   - **Technology Stack:** {', '.join(solution.technology_stack)}\n"
            summary += f"   - **Implementation Time:** {solution.implementation_time}\n"
            summary += f"   - **Cost Range:** {solution.cost_range}\n"
            summary += f"   - **ROI Estimate:** {solution.roi_estimate}\n"
            summary += f"   - **Use Cases:** {', '.join(solution.use_cases)}\n"
            summary += f"   - **Success Metrics:** {', '.join(solution.success_metrics)}\n"
            summary += f"   - **Industry Applicability:** {', '.join(solution.industry_applicability)}\n\n"
        
        return summary

# Direct callable function for integration
def research_solutions_for_problems_direct(industry_problems: List[str],
                                         company_industry: str,
                                         company_size: str = "Unknown") -> str:
    """Direct callable function for researching solutions."""
    try:
        agent = SolutionsAgent()
        solutions = agent.research_solutions_for_problems(industry_problems, company_industry, company_size)
        return agent.get_solutions_summary(solutions)
    except Exception as e:
        return f"Failed to research solutions: {str(e)}"

if __name__ == "__main__":
    # Example usage
    agent = SolutionsAgent()
    
    # Test with environmental services problems
    problems = [
        "Regulatory compliance complexity",
        "Waste management costs",
        "Sustainability pressures"
    ]
    
    solutions = agent.research_solutions_for_problems(problems, "Environmental Services", "Mid-market")
    
    print("Solutions Analysis:")
    print("=" * 50)
    print(agent.get_solutions_summary(solutions))
