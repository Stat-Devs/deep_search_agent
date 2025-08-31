from openai import AsyncOpenAI
import chainlit as cl
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional
import json
from datetime import datetime

# Import our research system components
from deep_research_system_handoffs import (
    ResearchContext, 
    AgentType, 
    determine_handoff_strategy_direct,
    analyze_company_website_direct,
    research_linkedin_profile_direct,
    generate_email_pitch_direct,
    compile_research_report_direct
)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Instrument the OpenAI client for Chainlit
cl.instrument_openai()

# Sales team assistant settings
settings = {
    "model": "gpt-4",
    "temperature": 0.1,
    "max_tokens": 2000
}

# Sales team context and capabilities
SALES_SYSTEM_PROMPT = """You are an AI Sales Intelligence Assistant for a data analytics services company. 

Your capabilities include:
1. **Lead Research & Analysis** - Research companies, contacts, and market opportunities
2. **Intelligent Handoff Routing** - Determine the best approach for different contact types
3. **Sales Strategy Development** - Create personalized outreach strategies
4. **Market Intelligence** - Provide industry insights and competitive analysis
5. **Email Pitch Generation** - Create compelling, personalized email pitches

Contact Types & Approaches:
- **Executive Contacts** (CEO/CTO/CFO): Strategic, ROI-focused, high priority (2-3 days)
- **Technical Contacts** (Engineers/Analysts): Technical integration + business outcomes (3-5 days)
- **General Contacts** (Managers/Coordinators): Professional, value-focused (5-7 days)

Always provide actionable insights and next steps for the sales team."""

@cl.on_chat_start
async def on_chat_start():
    """Initialize the sales assistant when the chat starts."""
    await cl.Message(
        content="🚀 **Sales Intelligence Assistant - BETA VERSION** 🧪\n\n"
               "⚠️ **This is a beta version of the tool. Features may evolve and improve over time.**\n\n"
               "I'm here to help your sales team with:\n"
               "• 🔍 Lead research and analysis\n"
               "• 🎯 Intelligent handoff strategies\n"
               "• 📧 Personalized email pitches\n"
               "• 📊 Market intelligence and insights\n"
               "• 🚀 Sales strategy development\n\n"
               "**Example queries:**\n"
               "• 'Research TechCorp Inc. and their CTO John Smith'\n"
               "• 'Create a pitch for a data engineer at DataFlow Analytics'\n"
               "• 'What's the best approach for a CEO contact?'\n"
               "• 'Generate an email for a marketing manager'\n\n"
               "**Beta Feedback:** We'd love to hear your experience and suggestions!\n\n"
               "📝 **Have a Feature Request?** [Submit it here](https://forms.gle/D9uAUPtJR1gmoDCD7)\n\n"
               "How can I help you today?"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming messages from the sales team."""
    
    user_query = message.content.lower()
    
    # Check if this is a lead research request
    if any(keyword in user_query for keyword in ['research', 'analyze', 'investigate', 'look up']):
        await handle_lead_research(message)
        return
    
    # Check if this is a pitch generation request
    elif any(keyword in user_query for keyword in ['pitch', 'email', 'outreach', 'message']):
        await handle_pitch_generation(message)
        return
    
    # Check if this is a handoff strategy request
    elif any(keyword in user_query for keyword in ['handoff', 'strategy', 'approach', 'route']):
        await handle_handoff_strategy(message)
        return
    
    # Check if this is a market intelligence request
    elif any(keyword in user_query for keyword in ['market', 'industry', 'competitive', 'trends']):
        await handle_market_intelligence(message)
        return
    
    # Default: General sales assistance
    else:
        await handle_general_sales_assistance(message)

async def handle_lead_research(message: cl.Message):
    """Handle lead research requests."""
    
    # Send initial response
    await cl.Message(
        content="🔍 **Lead Research Initiated**\n\n"
               "I'm analyzing your lead. Please provide:\n"
               "• Company name\n"
               "• Contact person's name and role\n"
               "• Website URL (if available)\n"
               "• LinkedIn URL (if available)\n\n"
               "Or simply describe the lead you want me to research."
    ).send()
    
    # Use OpenAI to extract structured information
    extraction_prompt = f"""
    Extract company and contact information from this sales query:
    "{message.content}"
    
    Return a JSON object with:
    {{
        "company_name": "extracted company name",
        "person_name": "extracted person name", 
        "person_role": "extracted role or title",
        "website_url": "extracted website if mentioned",
        "linkedin_url": "extracted LinkedIn if mentioned",
        "additional_context": "any other relevant details"
    }}
    
    If information is missing, use "Unknown" or null.
    """
    
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts structured information from text. Always return valid JSON."},
                {"role": "user", "content": extraction_prompt}
            ],
            **settings
        )
        
        extracted_info = json.loads(response.choices[0].message.content)
        
        # Create research context
        context = ResearchContext(
            company_name=extracted_info.get("company_name", "Unknown Company"),
            person_name=extracted_info.get("person_name", "Unknown Contact"),
            website_url=extracted_info.get("website_url"),
            linkedin_url=extracted_info.get("linkedin_url"),
            person_role=extracted_info.get("person_role")
        )
        
        # Perform research
        await perform_comprehensive_research(context)
        
    except Exception as e:
        await cl.Message(
            content=f"❌ **Research Error**\n\n"
                   f"Sorry, I encountered an error while processing your request:\n"
                   f"`{str(e)}`\n\n"
                   f"Please try rephrasing your request or provide more specific details."
        ).send()

async def perform_comprehensive_research(context: ResearchContext):
    """Perform comprehensive lead research."""
    
    # Step 1: Website Analysis
    if context.website_url:
        await cl.Message(content="🌐 **Analyzing company website...**").send()
        try:
            context.website_research = analyze_company_website_direct(
                context.company_name, 
                context.website_url
            )
            await cl.Message(content="✅ Website analysis complete").send()
        except Exception as e:
            context.website_research = f"Website analysis failed: {str(e)}"
    
    # Step 2: LinkedIn Research
    if context.linkedin_url or context.person_name:
        await cl.Message(content="👔 **Researching contact profile...**").send()
        try:
            context.linkedin_research = research_linkedin_profile_direct(
                context.person_name, 
                context.company_name
            )
            await cl.Message(content="✅ LinkedIn research complete").send()
        except Exception as e:
            context.linkedin_research = f"LinkedIn research failed: {str(e)}"
    
    # Step 3: Handoff Strategy
    await cl.Message(content="🎯 **Determining best approach...**").send()
    try:
        handoff_strategy = determine_handoff_strategy_direct(context)
        # The function modifies the context directly, so we just need to get the result
        await cl.Message(content="✅ Handoff strategy determined").send()
    except Exception as e:
        await cl.Message(content=f"⚠️ Handoff strategy failed: {str(e)}").send()
    
    # Step 4: Generate Research Report
    await cl.Message(content="📊 **Compiling research report...**").send()
    try:
        research_report = compile_research_report_direct(
            context.company_name,
            context.person_name,
            context.website_research or "No website research available",
            context.linkedin_research or "No LinkedIn research available"
        )
        await cl.Message(content="✅ Research report compiled").send()
    except Exception as e:
        research_report = f"Report compilation failed: {str(e)}"
    
    # Step 5: Generate Email Pitch
    await cl.Message(content="📧 **Creating personalized email pitch...**").send()
    try:
        # Create a research summary for email generation
        research_summary = f"""
Company: {context.company_name}
Contact: {context.person_name}
Role: {context.person_role or 'Unknown'}
Website Research: {context.website_research or 'Not available'}
LinkedIn Research: {context.linkedin_research or 'Not available'}
Handoff Strategy: {context.handoff_reason or 'Standard approach'}
        """.strip()
        
        email_pitch = generate_email_pitch_direct(
            context.person_name,
            context.company_name,
            research_summary
        )
        await cl.Message(content="✅ Email pitch created").send()
    except Exception as e:
        email_pitch = f"Email generation failed: {str(e)}"
    
    # Step 6: Present Results
    await present_research_results(context, research_report, email_pitch)

async def present_research_results(context: ResearchContext, research_report: str, email_pitch: str):
    """Present comprehensive research results to the sales team."""
    
    # Create a comprehensive results message
    results_content = f"""
🎯 **LEAD RESEARCH COMPLETE**
================================

📋 **Lead Information**
Company: {context.company_name}
Contact: {context.person_name}
Role: {context.person_role or 'Unknown'}
Priority: {'⭐' * context.priority_level} ({context.priority_level}/5)

🔄 **Handoff Strategy**
Next Agent: {context.next_agent.value if context.next_agent else 'General'}
Reason: {context.handoff_reason or 'Standard processing'}
Approach: {context.communication_tone or 'Professional'}
Timeline: {context.follow_up_timeline or '5-7 business days'}

📊 **Research Summary**
{research_report[:500]}{'...' if len(research_report) > 500 else ''}

📧 **Email Pitch**
{email_pitch[:300]}{'...' if len(email_pitch) > 300 else ''}

🚀 **Next Steps**
1. Review the complete research report
2. Customize the email pitch for your style
3. Follow up within the recommended timeline
4. Track engagement and adjust approach

💡 **Sales Intelligence Tips**
• Contact type: {'Executive' if context.priority_level >= 4 else 'Technical' if context.priority_level >= 3 else 'General'}
• Focus on: {context.communication_tone or 'Value propositions and ROI'}
• Best timing: {context.follow_up_timeline or 'Within 5-7 business days'}

🧪 **Beta Note:** This is a beta version. Please provide feedback on the research quality and suggestions!

📝 **Feature Request?** [Submit new features here](https://forms.gle/D9uAUPtJR1gmoDCD7)
"""
    
    await cl.Message(content=results_content).send()
    
    # Send detailed reports as separate messages
    if len(research_report) > 500:
        await cl.Message(
            content=f"📊 **Complete Research Report**\n\n{research_report}"
        ).send()
    
    if len(email_pitch) > 300:
        await cl.Message(
            content=f"📧 **Complete Email Pitch**\n\n{email_pitch}"
        ).send()

async def handle_pitch_generation(message: cl.Message):
    """Handle email pitch generation requests."""
    
    await cl.Message(
        content="📧 **Email Pitch Generation**\n\n"
               "I'll help you create a personalized email pitch. Please provide:\n"
               "• Company name and contact person\n"
               "• Their role and any known pain points\n"
               "• What specific value proposition you want to highlight\n\n"
               "Or describe the prospect and I'll create a pitch for you."
    ).send()
    
    # Generate pitch using OpenAI
    pitch_prompt = f"""
    Create a compelling sales email pitch for this request:
    "{message.content}"
    
    The pitch should be:
    - Professional and personalized
    - Focused on value and ROI
    - Include a clear call-to-action
    - Appropriate length (150-200 words)
    - Written in a confident, consultative tone
    """
    
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert sales copywriter specializing in B2B data analytics services."},
                {"role": "user", "content": pitch_prompt}
            ],
            **settings
        )
        
        pitch = response.choices[0].message.content
        
        await cl.Message(
            content=f"📧 **Your Personalized Email Pitch**\n\n{pitch}\n\n"
                   f"💡 **Tips for Success:**\n"
                   f"• Customize the opening to reference recent company news\n"
                   f"• Add specific metrics or case studies if available\n"
                   f"• Follow up within 3-5 business days\n"
                   f"• Track open rates and engagement\n\n"
                   f"🧪 **Beta Feedback:** How was this pitch? Any suggestions for improvement?\n\n"
                   f"📝 **Feature Request?** [Submit new features here](https://forms.gle/D9uAUPtJR1gmoDCD7)"
        ).send()
        
    except Exception as e:
        await cl.Message(
            content=f"❌ **Pitch Generation Error**\n\n"
                   f"Sorry, I couldn't generate a pitch: {str(e)}\n\n"
                   f"Please try again or provide more specific details."
        ).send()

async def handle_handoff_strategy(message: cl.Message):
    """Handle handoff strategy requests."""
    
    await cl.Message(
        content="🎯 **Handoff Strategy Analysis**\n\n"
               "I'll help you determine the best approach for your contact. Please provide:\n"
               "• Contact person's name and role\n"
               "• Company name and industry\n"
               "• Any known technical skills or decision-making power\n"
               "• What you're trying to achieve\n\n"
               "I'll analyze and recommend the optimal handoff strategy."
    ).send()
    
    # Analyze handoff strategy using OpenAI
    strategy_prompt = f"""
    Analyze this contact for handoff strategy:
    "{message.content}"
    
    Provide recommendations for:
    1. Contact type classification (Executive/Technical/General)
    2. Priority level (1-5 scale)
    3. Best approach and communication tone
    4. Recommended timeline for follow-up
    5. Key value propositions to highlight
    """
    
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a sales strategy expert specializing in lead qualification and handoff optimization."},
                {"role": "user", "content": strategy_prompt}
            ],
            **settings
        )
        
        strategy = response.choices[0].message.content
        
        await cl.Message(
            content=f"🎯 **Handoff Strategy Analysis**\n\n{strategy}\n\n"
                   f"💡 **Implementation Tips:**\n"
                   f"• Use the recommended communication tone consistently\n"
                   f"• Follow the suggested timeline for optimal engagement\n"
                   f"• Focus on the highlighted value propositions\n"
                   f"• Track results and adjust strategy based on response\n\n"
                   f"🧪 **Beta Note:** How accurate was this strategy analysis? Any improvements needed?\n\n"
                   f"📝 **Feature Request?** [Submit new features here](https://forms.gle/D9uAUPtJR1gmoDCD7)"
        ).send()
        
    except Exception as e:
        await cl.Message(
            content=f"❌ **Strategy Analysis Error**\n\n"
                   f"Sorry, I couldn't analyze the strategy: {str(e)}\n\n"
                   f"Please try again or provide more specific details."
        ).send()

async def handle_market_intelligence(message: cl.Message):
    """Handle market intelligence requests."""
    
    await cl.Message(
        content="📊 **Market Intelligence Request**\n\n"
               "I'll help you with market insights. Please specify:\n"
               "• Industry or sector you're interested in\n"
               "• Specific market trends or competitive landscape\n"
               "• Geographic region or market size\n"
               "• What insights would be most valuable for your sales strategy\n\n"
               "I'll provide market intelligence to help you position your services effectively."
    ).send()
    
    # Generate market intelligence using OpenAI
    market_prompt = f"""
    Provide market intelligence for this sales team request:
    "{message.content}"
    
    Include:
    1. Current market trends and opportunities
    2. Competitive landscape analysis
    3. Key challenges and pain points in the market
    4. Sales positioning recommendations
    5. Market timing and seasonal factors
    """
    
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a market intelligence expert specializing in B2B data analytics and technology services."},
                {"role": "user", "content": market_prompt}
            ],
            **settings
        )
        
        intelligence = response.choices[0].message.content
        
        await cl.Message(
            content=f"📊 **Market Intelligence Report**\n\n{intelligence}\n\n"
                   f"💡 **Sales Strategy Recommendations:**\n"
                   f"• Use these insights to refine your value proposition\n"
                   f"• Position your services against current market challenges\n"
                   f"• Leverage timing and seasonal factors in your outreach\n"
                   f"• Monitor these trends for ongoing strategy adjustments\n\n"
                   f"🧪 **Beta Feedback:** How valuable were these market insights? Any specific areas you'd like me to focus on?\n\n"
                   f"📝 **Feature Request?** [Submit new features here](https://forms.gle/D9uAUPtJR1gmoDCD7)"
        ).send()
        
    except Exception as e:
        await cl.Message(
            content=f"❌ **Market Intelligence Error**\n\n"
                   f"Sorry, I couldn't generate market intelligence: {str(e)}\n\n"
                   f"Please try again or provide more specific details."
        ).send()

async def handle_general_sales_assistance(message: cl.Message):
    """Handle general sales assistance requests."""
    
    # Use OpenAI to provide general sales assistance
    assistance_prompt = f"""
    You are an AI Sales Intelligence Assistant. Help the sales team with this request:
    "{message.content}"
    
    Provide helpful, actionable advice for:
    - Sales strategy and tactics
    - Lead qualification and research
    - Communication and outreach
    - Market positioning and competitive analysis
    - Sales process optimization
    
    Keep responses practical and sales-focused.
    """
    
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert sales consultant and coach specializing in B2B technology sales."},
                {"role": "user", "content": assistance_prompt}
            ],
            **settings
        )
        
        assistance = response.choices[0].message.content
        
        await cl.Message(
            content=f"💡 **Sales Intelligence Assistant**\n\n{assistance}\n\n"
                   f"🔍 **Need More Specific Help?**\n"
                   f"• Lead research: 'Research [Company] and [Contact]'\n"
                   f"• Email pitches: 'Create a pitch for [Role] at [Company]'\n"
                   f"• Handoff strategy: 'What's the best approach for [Contact Type]?'\n"
                   f"• Market insights: 'Tell me about [Industry] market trends'\n\n"
                   f"🧪 **Beta Note:** How helpful was this assistance? Any specific areas you'd like me to improve?\n\n"
                   f"📝 **Feature Request?** [Submit new features here](https://forms.gle/D9uAUPtJR1gmoDCD7)"
        ).send()
        
    except Exception as e:
        await cl.Message(
            content=f"❌ **Assistance Error**\n\n"
                   f"Sorry, I couldn't provide assistance: {str(e)}\n\n"
                   f"Please try rephrasing your request or ask for specific help with lead research, pitch generation, or market intelligence."
        ).send()

@cl.on_chat_end
async def on_chat_end():
    """Handle chat session end."""
    await cl.Message(
        content="👋 **Sales Intelligence Session Ended**\n\n"
               "Thank you for using the Sales Intelligence Assistant!\n\n"
               "**Session Summary:**\n"
               "• Lead research and analysis completed\n"
               "• Handoff strategies determined\n"
               "• Email pitches generated\n"
               "• Market intelligence provided\n\n"
               "**Next Steps:**\n"
               "• Follow up on researched leads within recommended timelines\n"
               "• Customize generated pitches for your style\n"
               "• Implement suggested sales strategies\n"
               "• Track results and adjust approaches\n\n"
               "🧪 **Beta Feedback Request:**\n"
               "• How was your experience with the tool?\n"
               "• What features would you like to see improved?\n"
               "• Any bugs or issues you encountered?\n"
               "• Suggestions for new capabilities?\n\n"
               "📝 **Feature Request Form:** [Submit new features here](https://forms.gle/D9uAUPtJR1gmoDCD7)\n\n"
               "🚀 Happy selling! Come back anytime for more intelligence support."
    ).send()

if __name__ == "__main__":
    print("🚀 Sales Intelligence Assistant - BETA VERSION 🧪")
    print("⚠️  This is a beta version of the tool. Features may evolve and improve over time.")
    print("💡 This app provides conversational AI assistance to your sales team")
    print("🔍 Features: Lead research, handoff analysis, pitch generation, market intelligence")
    print("📱 Run with: chainlit run app.py -w")
    print("💬 Beta Feedback: We'd love to hear your experience and suggestions!")
