"""
Tavily Research Agent - Enhanced Lead Research with Web Search

This agent uses Tavily API to perform comprehensive web research on leads
based on the handoff system's analysis. It provides enhanced intelligence
by searching for recent news, company updates, and market information.
"""

import os
from dotenv import load_dotenv, find_dotenv
from typing import Dict, List, Any, Optional, Union
from tavily import TavilyClient
import json
from datetime import datetime, timedelta

# Load environment variables
load_dotenv(find_dotenv())

# Get Tavily API key
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found in environment variables")

# Initialize Tavily client
tavily_client = TavilyClient(api_key=tavily_api_key)

class TavilyResearchAgent:
    """
    Enhanced research agent using Tavily API for comprehensive lead intelligence.
    Integrates with the handoff system to provide specialized research based on contact type.
    """
    
    def __init__(self):
        self.client = tavily_client
        self.search_depth = "advanced"  # Options: basic, advanced
        self.max_results = 10
        
    def research_lead_with_tavily(
        self,
        company_name: str,
        person_name: str,
        person_role: Optional[str] = None,
        company_industry: Optional[str] = None,
        contact_type: str = "general",
        research_focus: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive lead research using Tavily API based on handoff analysis.
        
        Args:
            company_name: Name of the company
            person_name: Name of the contact person
            person_role: Role of the contact person
            company_industry: Industry of the company
            contact_type: Type of contact (executive, technical, general)
            research_focus: Specific focus area for research
            
        Returns:
            Dictionary containing comprehensive research results
        """
        
        research_results = {
            "company_name": company_name,
            "person_name": person_name,
            "research_timestamp": datetime.now().isoformat(),
            "contact_type": contact_type,
            "company_research": {},
            "person_research": {},
            "market_research": {},
            "opportunity_analysis": {},
            "research_summary": ""
        }
        
        try:
            # Company research based on contact type
            company_research = self._research_company(company_name, contact_type, company_industry)
            research_results["company_research"] = company_research
            
            # Person research based on role and contact type
            person_research = self._research_person(person_name, company_name, person_role, contact_type)
            research_results["person_research"] = person_research
            
            # Market and industry research
            market_research = self._research_market(company_name, company_industry, contact_type)
            research_results["market_research"] = market_research
            
            # Opportunity analysis based on handoff type
            opportunity_analysis = self._analyze_opportunities(
                company_research, person_research, market_research, contact_type
            )
            research_results["opportunity_analysis"] = opportunity_analysis
            
            # Generate comprehensive research summary
            research_summary = self._generate_research_summary(
                company_research, person_research, market_research, opportunity_analysis, contact_type
            )
            research_results["research_summary"] = research_summary
            
        except Exception as e:
            research_results["error"] = f"Research failed: {str(e)}"
            research_results["research_summary"] = f"Research encountered an error: {str(e)}"
        
        return research_results
    
    def _research_company(
        self, 
        company_name: str, 
        contact_type: str, 
        company_industry: Optional[str] = None
    ) -> Dict[str, Any]:
        """Research company information based on contact type."""
        
        company_research = {
            "company_name": company_name,
            "recent_news": [],
            "company_updates": [],
            "financial_info": [],
            "growth_indicators": [],
            "challenges": [],
            "opportunities": []
        }
        
        # Company news and updates
        news_query = f"{company_name} company news updates 2024"
        if company_industry:
            news_query += f" {company_industry}"
        
        try:
            news_results = self.client.search(
                query=news_query,
                search_depth=self.search_depth,
                max_results=5
            )
            
            if news_results.get("results"):
                company_research["recent_news"] = [
                    {
                        "title": result.get("title", ""),
                        "content": result.get("content", ""),
                        "url": result.get("url", ""),
                        "published_date": result.get("published_date", "")
                    }
                    for result in news_results["results"][:5]
                ]
        except Exception as e:
            company_research["recent_news"] = [{"error": f"News search failed: {str(e)}"}]
        
        # Company challenges and pain points
        challenges_query = f"{company_name} business challenges problems scaling growth"
        try:
            challenges_results = self.client.search(
                query=challenges_query,
                search_depth=self.search_depth,
                max_results=3
            )
            
            if challenges_results.get("results"):
                company_research["challenges"] = [
                    {
                        "content": result.get("content", ""),
                        "url": result.get("url", "")
                    }
                    for result in challenges_results["results"][:3]
                ]
        except Exception as e:
            company_research["challenges"] = [{"error": f"Challenges search failed: {str(e)}"}]
        
        # Growth indicators and opportunities
        growth_query = f"{company_name} growth expansion funding investment"
        try:
            growth_results = self.client.search(
                query=growth_query,
                search_depth=self.search_depth,
                max_results=3
            )
            
            if growth_results.get("results"):
                company_research["growth_indicators"] = [
                    {
                        "content": result.get("content", ""),
                        "url": result.get("url", "")
                    }
                    for result in growth_results["results"][:3]
                ]
        except Exception as e:
            company_research["growth_indicators"] = [{"error": f"Growth search failed: {str(e)}"}]
        
        return company_research
    
    def _research_person(
        self, 
        person_name: str, 
        company_name: str, 
        person_role: Optional[str], 
        contact_type: str
    ) -> Dict[str, Any]:
        """Research person information based on role and contact type."""
        
        person_research = {
            "person_name": person_name,
            "company": company_name,
            "recent_activity": [],
            "professional_background": [],
            "thought_leadership": [],
            "contact_preferences": [],
            "decision_influence": []
        }
        
        # Recent professional activity
        activity_query = f"{person_name} {company_name} recent professional activity speaking events"
        try:
            activity_results = self.client.search(
                query=activity_query,
                search_depth=self.search_depth,
                max_results=3
            )
            
            if activity_results.get("results"):
                person_research["recent_activity"] = [
                    {
                        "content": result.get("content", ""),
                        "url": result.get("url", ""),
                        "title": result.get("title", "")
                    }
                    for result in activity_results["results"][:3]
                ]
        except Exception as e:
            person_research["recent_activity"] = [{"error": f"Activity search failed: {str(e)}"}]
        
        # Thought leadership and expertise
        expertise_query = f"{person_name} {company_name} thought leadership expertise articles"
        try:
            expertise_results = self.client.search(
                query=expertise_query,
                search_depth=self.search_depth,
                max_results=3
            )
            
            if expertise_results.get("results"):
                person_research["thought_leadership"] = [
                    {
                        "content": result.get("content", ""),
                        "url": result.get("url", ""),
                        "title": result.get("title", "")
                    }
                    for result in expertise_results["results"][:3]
                ]
        except Exception as e:
            person_research["thought_leadership"] = [{"error": f"Expertise search failed: {str(e)}"}]
        
        # Decision influence based on contact type
        if contact_type == "executive":
            influence_query = f"{person_name} {company_name} executive decision making strategic"
        elif contact_type == "technical":
            influence_query = f"{person_name} {company_name} technical leadership implementation"
        else:
            influence_query = f"{person_name} {company_name} professional background role"
        
        try:
            influence_results = self.client.search(
                query=influence_query,
                search_depth=self.search_depth,
                max_results=3
            )
            
            if influence_results.get("results"):
                person_research["decision_influence"] = [
                    {
                        "content": result.get("content", ""),
                        "url": result.get("url", ""),
                        "title": result.get("title", "")
                    }
                    for result in influence_results["results"][:3]
                ]
        except Exception as e:
            person_research["decision_influence"] = [{"error": f"Influence search failed: {str(e)}"}]
        
        return person_research
    
    def _research_market(
        self, 
        company_name: str, 
        company_industry: Optional[str], 
        contact_type: str
    ) -> Dict[str, Any]:
        """Research market and industry information."""
        
        market_research = {
            "industry_trends": [],
            "competitive_landscape": [],
            "market_opportunities": [],
            "regulatory_environment": []
        }
        
        # Industry trends
        industry = company_industry or "business technology"
        trends_query = f"{industry} industry trends 2024 market analysis"
        try:
            trends_results = self.client.search(
                query=trends_query,
                search_depth=self.search_depth,
                max_results=3
            )
            
            if trends_results.get("results"):
                market_research["industry_trends"] = [
                    {
                        "content": result.get("content", ""),
                        "url": result.get("url", ""),
                        "title": result.get("title", "")
                    }
                    for result in trends_results["results"][:3]
                ]
        except Exception as e:
            market_research["industry_trends"] = [{"error": f"Trends search failed: {str(e)}"}]
        
        # Competitive landscape
        competitive_query = f"{company_name} competitors market position competitive analysis"
        try:
            competitive_results = self.client.search(
                query=competitive_query,
                search_depth=self.search_depth,
                max_results=3
            )
            
            if competitive_results.get("results"):
                market_research["competitive_landscape"] = [
                    {
                        "content": result.get("content", ""),
                        "url": result.get("url", ""),
                        "title": result.get("title", "")
                    }
                    for result in competitive_results["results"][:3]
                ]
        except Exception as e:
            market_research["competitive_landscape"] = [{"error": f"Competitive search failed: {str(e)}"}]
        
        return market_research
    
    def _analyze_opportunities(
        self, 
        company_research: Dict, 
        person_research: Dict, 
        market_research: Dict, 
        contact_type: str
    ) -> Dict[str, Any]:
        """Analyze opportunities based on research findings and contact type."""
        
        opportunities = {
            "immediate_opportunities": [],
            "strategic_opportunities": [],
            "timing_recommendations": [],
            "approach_strategy": []
        }
        
        # Analyze company challenges for immediate opportunities
        if company_research.get("challenges"):
            for challenge in company_research["challenges"]:
                if "content" in challenge and not challenge.get("error"):
                    opportunities["immediate_opportunities"].append({
                        "type": "challenge_based",
                        "description": challenge["content"][:200] + "...",
                        "priority": "high" if contact_type == "executive" else "medium"
                    })
        
        # Analyze growth indicators for strategic opportunities
        if company_research.get("growth_indicators"):
            for growth in company_research["growth_indicators"]:
                if "content" in growth and not growth.get("error"):
                    opportunities["strategic_opportunities"].append({
                        "type": "growth_based",
                        "description": growth["content"][:200] + "...",
                        "priority": "high" if contact_type == "executive" else "medium"
                    })
        
        # Timing recommendations based on contact type
        if contact_type == "executive":
            opportunities["timing_recommendations"] = [
                "Immediate outreach due to executive decision-making power",
                "Follow up within 2-3 business days",
                "Schedule executive briefing within 1 week"
            ]
        elif contact_type == "technical":
            opportunities["timing_recommendations"] = [
                "Technical discussion within 3-5 business days",
                "Follow up with technical specifications",
                "Schedule technical review within 2 weeks"
            ]
        else:
            opportunities["timing_recommendations"] = [
                "Professional outreach within 5-7 business days",
                "Follow up with value proposition",
                "Schedule consultation within 2-3 weeks"
            ]
        
        # Approach strategy based on contact type
        if contact_type == "executive":
            opportunities["approach_strategy"] = [
                "Focus on strategic business outcomes and ROI",
                "Emphasize competitive advantages and market positioning",
                "Present executive-level value propositions"
            ]
        elif contact_type == "technical":
            opportunities["approach_strategy"] = [
                "Balance technical depth with business outcomes",
                "Highlight implementation benefits and integration advantages",
                "Provide technical ROI and timeline estimates"
            ]
        else:
            opportunities["approach_strategy"] = [
                "Professional value-focused approach",
                "Emphasize practical benefits and solutions",
                "Provide case studies and references"
            ]
        
        return opportunities
    
    def _generate_research_summary(
        self, 
        company_research: Dict, 
        person_research: Dict, 
        market_research: Dict, 
        opportunity_analysis: Dict, 
        contact_type: str
    ) -> str:
        """Generate comprehensive research summary based on all findings."""
        
        summary_parts = []
        
        # Company overview
        if company_research.get("recent_news"):
            summary_parts.append(f"Company Research: {len(company_research['recent_news'])} recent news items found")
        
        if company_research.get("challenges"):
            summary_parts.append(f"Challenges Identified: {len(company_research['challenges'])} business challenges detected")
        
        if company_research.get("growth_indicators"):
            summary_parts.append(f"Growth Indicators: {len(company_research['growth_indicators'])} positive growth signals")
        
        # Person analysis
        if person_research.get("recent_activity"):
            summary_parts.append(f"Person Activity: {len(person_research['recent_activity'])} recent professional activities")
        
        if person_research.get("thought_leadership"):
            summary_parts.append(f"Expertise: {len(person_research['thought_leadership'])} thought leadership indicators")
        
        # Market context
        if market_research.get("industry_trends"):
            summary_parts.append(f"Market Trends: {len(market_research['industry_trends'])} industry trend insights")
        
        # Opportunities
        if opportunity_analysis.get("immediate_opportunities"):
            summary_parts.append(f"Immediate Opportunities: {len(opportunity_analysis['immediate_opportunities'])} high-priority opportunities")
        
        if opportunity_analysis.get("strategic_opportunities"):
            summary_parts.append(f"Strategic Opportunities: {len(opportunity_analysis['strategic_opportunities'])} long-term opportunities")
        
        # Contact type specific insights
        if contact_type == "executive":
            summary_parts.append("Executive Contact: High-priority outreach recommended with strategic focus")
        elif contact_type == "technical":
            summary_parts.append("Technical Contact: Technical integration focus with business outcomes")
        else:
            summary_parts.append("General Contact: Professional approach with value proposition focus")
        
        return " | ".join(summary_parts)
    
    def quick_research(
        self, 
        company_name: str, 
        person_name: str, 
        contact_type: str = "general"
    ) -> str:
        """
        Quick research function for basic lead intelligence.
        
        Args:
            company_name: Name of the company
            person_name: Name of the contact person
            contact_type: Type of contact (executive, technical, general)
            
        Returns:
            String summary of research findings
        """
        
        try:
            # Perform focused research
            company_query = f"{company_name} company overview business model"
            person_query = f"{person_name} {company_name} professional background"
            
            company_results = self.client.search(
                query=company_query,
                search_depth="basic",
                max_results=3
            )
            
            person_results = self.client.search(
                query=person_query,
                search_depth="basic",
                max_results=2
            )
            
            # Extract key information
            company_info = ""
            if company_results.get("results"):
                company_info = company_results["results"][0].get("content", "")[:300] + "..."
            
            person_info = ""
            if person_results.get("results"):
                person_info = person_results["results"][0].get("content", "")[:200] + "..."
            
            # Generate summary based on contact type
            if contact_type == "executive":
                summary = f"Executive Research Summary:\nCompany: {company_info}\nContact: {person_info}\nPriority: High - Executive contact requires strategic approach"
            elif contact_type == "technical":
                summary = f"Technical Research Summary:\nCompany: {company_info}\nContact: {person_info}\nPriority: Medium-High - Technical contact needs integration focus"
            else:
                summary = f"General Research Summary:\nCompany: {company_info}\nContact: {person_info}\nPriority: Medium - Standard professional approach"
            
            return summary
            
        except Exception as e:
            return f"Quick research failed: {str(e)}"
