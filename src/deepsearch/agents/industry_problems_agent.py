"""
Industry Problems Research Agent

This agent specializes in identifying potential industry problems, challenges,
and pain points that leads may face in their respective business sectors.
"""

import os
from typing import List, Dict, Any
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

@dataclass
class IndustryProblem:
    """Data structure for industry problems."""
    problem_title: str
    problem_description: str
    impact_level: str  # "High", "Medium", "Low"
    affected_stakeholders: List[str]
    market_size: str
    urgency: str  # "Critical", "High", "Medium", "Low"
    related_industries: List[str]
    potential_solutions: List[str]
    business_impact: str

class IndustryProblemsAgent:
    """Agent specialized in identifying potential industry problems and challenges."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.agent_type = "Industry Problems Specialist"
        
    def identify_lead_problems(self, 
                              company_industry: str,
                              company_size: str = "Unknown",
                              company_location: str = "Unknown",
                              person_role: str = "Unknown") -> List[IndustryProblem]:
        """
        Identify potential problems the lead may face in their industry.
        
        Args:
            company_industry: The industry sector (e.g., "Environmental Services")
            company_size: Company size category
            company_location: Geographic location
            person_role: Role of the contact person
            
        Returns:
            List of identified industry problems
        """
        
        # Define industry-specific problem frameworks
        industry_problems = self._get_industry_problem_framework(company_industry)
        
        # Enhance with AI-generated insights
        enhanced_problems = self._enhance_problems_with_ai(
            industry_problems, company_industry, company_size, company_location, person_role
        )
        
        return enhanced_problems
    
    def _get_industry_problem_framework(self, industry: str) -> List[IndustryProblem]:
        """Get base industry problem framework."""
        
        # Environmental Services Framework
        if "environmental" in industry.lower() or "waste" in industry.lower():
            return [
                IndustryProblem(
                    problem_title="Regulatory Compliance Complexity",
                    problem_description="Increasing environmental regulations requiring complex compliance strategies and documentation",
                    impact_level="High",
                    affected_stakeholders=["Companies", "Regulators", "Communities"],
                    market_size="$50B+ annually",
                    urgency="Critical",
                    related_industries=["Manufacturing", "Construction", "Energy"],
                    potential_solutions=["Compliance software", "Expert consulting", "Automated monitoring"],
                    business_impact="Fines, legal risks, operational delays"
                ),
                IndustryProblem(
                    problem_title="Waste Management Costs",
                    problem_description="Rising costs of waste disposal and treatment affecting profit margins",
                    impact_level="High",
                    affected_stakeholders=["Businesses", "Municipalities", "Consumers"],
                    market_size="$100B+ annually",
                    urgency="High",
                    related_industries=["Manufacturing", "Healthcare", "Retail"],
                    potential_solutions=["Waste reduction strategies", "Recycling programs", "Cost optimization"],
                    business_impact="Reduced profitability, competitive disadvantage"
                ),
                IndustryProblem(
                    problem_title="Sustainability Pressures",
                    problem_description="Growing demand for sustainable business practices from customers and investors",
                    impact_level="Medium",
                    affected_stakeholders=["Businesses", "Investors", "Customers"],
                    market_size="$30B+ annually",
                    urgency="High",
                    related_industries=["All sectors"],
                    potential_solutions=["Green certifications", "Sustainability reporting", "Eco-friendly alternatives"],
                    business_impact="Market share loss, investor pressure"
                )
            ]
        
        # Technology Framework
        elif "technology" in industry.lower() or "software" in industry.lower():
            return [
                IndustryProblem(
                    problem_title="Cybersecurity Threats",
                    problem_description="Increasing sophisticated cyber attacks and data breaches",
                    impact_level="Critical",
                    affected_stakeholders=["All businesses", "Government", "Individuals"],
                    market_size="$200B+ annually",
                    urgency="Critical",
                    related_industries=["Finance", "Healthcare", "Retail"],
                    potential_solutions=["Advanced security tools", "Employee training", "Incident response"],
                    business_impact="Data loss, reputation damage, legal liability"
                ),
                IndustryProblem(
                    problem_title="Digital Transformation",
                    problem_description="Pressure to modernize legacy systems and processes",
                    impact_level="High",
                    affected_stakeholders=["Enterprises", "SMBs", "Government"],
                    market_size="$500B+ annually",
                    urgency="High",
                    related_industries=["All sectors"],
                    potential_solutions=["Cloud migration", "Process automation", "Digital consulting"],
                    business_impact="Competitive disadvantage, operational inefficiency"
                )
            ]
        
        # Manufacturing Framework
        elif "manufacturing" in industry.lower():
            return [
                IndustryProblem(
                    problem_title="Supply Chain Disruption",
                    problem_description="Global supply chain challenges and material shortages",
                    impact_level="Critical",
                    affected_stakeholders=["Manufacturers", "Retailers", "Consumers"],
                    market_size="$100B+ annually",
                    urgency="Critical",
                    related_industries=["Automotive", "Electronics", "Construction"],
                    potential_solutions=["Supply chain optimization", "Local sourcing", "Inventory management"],
                    business_impact="Production delays, increased costs, customer dissatisfaction"
                ),
                IndustryProblem(
                    problem_title="Labor Shortages",
                    problem_description="Difficulty finding skilled manufacturing workers",
                    impact_level="High",
                    affected_stakeholders=["Manufacturers", "Workers", "Economy"],
                    market_size="$50B+ annually",
                    urgency="High",
                    related_industries=["All manufacturing"],
                    potential_solutions=["Automation", "Training programs", "Competitive compensation"],
                    business_impact="Reduced production capacity, quality issues"
                )
            ]
        
        # Default Framework
        else:
            return [
                IndustryProblem(
                    problem_title="Market Competition",
                    problem_description="Intense competition requiring differentiation strategies",
                    impact_level="High",
                    affected_stakeholders=["Businesses", "Customers", "Investors"],
                    market_size="Varies by industry",
                    urgency="Medium",
                    related_industries=["All sectors"],
                    potential_solutions=["Unique value propositions", "Customer experience", "Innovation"],
                    business_impact="Market share loss, price pressure"
                ),
                IndustryProblem(
                    problem_title="Cost Management",
                    problem_description="Rising operational costs affecting profitability",
                    impact_level="Medium",
                    affected_stakeholders=["Businesses", "Shareholders", "Employees"],
                    market_size="Varies by industry",
                    urgency="Medium",
                    related_industries=["All sectors"],
                    potential_solutions=["Process optimization", "Technology adoption", "Strategic partnerships"],
                    business_impact="Reduced margins, investment limitations"
                )
            ]
    
    def _enhance_problems_with_ai(self, 
                                 base_problems: List[IndustryProblem],
                                 industry: str,
                                 company_size: str,
                                 company_location: str,
                                 person_role: str) -> List[IndustryProblem]:
        """Enhance problems with AI-generated insights."""
        
        try:
            # Create context for AI enhancement
            context = f"""
            Industry: {industry}
            Company Size: {company_size}
            Location: {company_location}
            Contact Role: {person_role}
            
            Base Problems Identified:
            {chr(10).join([f"- {p.problem_title}: {p.problem_description}" for p in base_problems])}
            
            Please enhance these problems with:
            1. Additional industry-specific challenges relevant to this role
            2. Current market trends affecting these problems
            3. Emerging issues in this sector
            4. Regional variations based on location
            5. Role-specific challenges for {person_role}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an industry analyst specializing in identifying business challenges and market problems that executives and decision-makers face."},
                    {"role": "user", "content": context}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse AI response and enhance problems
            ai_insights = response.choices[0].message.content
            
            # Add AI-enhanced problems
            enhanced_problems = base_problems.copy()
            
            # Create additional problem from AI insights
            if "emerging" in ai_insights.lower() or "trend" in ai_insights.lower():
                enhanced_problems.append(
                    IndustryProblem(
                        problem_title="AI-Enhanced Industry Challenge",
                        problem_description=f"AI-identified challenge: {ai_insights[:200]}...",
                        impact_level="Medium",
                        affected_stakeholders=["Industry participants"],
                        market_size="Varies",
                        urgency="Medium",
                        related_industries=[industry],
                        potential_solutions=["AI-powered solutions", "Industry collaboration", "Innovation"],
                        business_impact="Competitive pressure, market disruption"
                    )
                )
            
            return enhanced_problems
            
        except Exception as e:
            print(f"AI enhancement failed: {e}")
            return base_problems
    
    def get_problem_summary(self, problems: List[IndustryProblem]) -> str:
        """Generate a summary of identified problems."""
        
        if not problems:
            return "No industry problems identified."
        
        summary = f"**Potential Industry Problems Analysis**\n\n"
        summary += f"**Total Problems Identified:** {len(problems)}\n\n"
        
        for i, problem in enumerate(problems, 1):
            summary += f"**{i}. {problem.problem_title}**\n"
            summary += f"   - Impact: {problem.impact_level}\n"
            summary += f"   - Urgency: {problem.urgency}\n"
            summary += f"   - Market Size: {problem.market_size}\n"
            summary += f"   - Description: {problem.problem_description}\n"
            summary += f"   - Business Impact: {problem.business_impact}\n"
            summary += f"   - Stakeholders: {', '.join(problem.affected_stakeholders)}\n"
            summary += f"   - Potential Solutions: {', '.join(problem.potential_solutions[:3])}\n\n"
        
        return summary

# Direct callable function for integration
def identify_lead_problems_direct(company_industry: str, 
                                 company_size: str = "Unknown",
                                 company_location: str = "Unknown",
                                 person_role: str = "Unknown") -> str:
    """Direct callable function for identifying lead problems."""
    try:
        agent = IndustryProblemsAgent()
        problems = agent.identify_lead_problems(company_industry, company_size, company_location, person_role)
        return agent.get_problem_summary(problems)
    except Exception as e:
        return f"Failed to identify lead problems: {str(e)}"

if __name__ == "__main__":
    # Example usage
    agent = IndustryProblemsAgent()
    
    # Test with environmental services
    problems = agent.identify_lead_problems("Environmental Services", "Mid-market", "United States", "CEO")
    
    print("Industry Problems Analysis:")
    print("=" * 50)
    print(agent.get_problem_summary(problems))
