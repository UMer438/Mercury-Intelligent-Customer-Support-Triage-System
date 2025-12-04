import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Auto-Triage AI Agent")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq Client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

llm = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile",
    groq_api_key=GROQ_API_KEY
)

# Define Pydantic models
class TicketInput(BaseModel):
    complaint: str

class TicketAnalysis(BaseModel):
    category: str = Field(description="The category of the ticket: Hardware_Defect, Software_Bug, Billing_Dispute, Shipping_Delay, User_Error")
    sentiment: str = Field(description="The sentiment of the ticket")
    urgency: str = Field(description="The urgency of the ticket: Low, Medium, High, Critical")
    suggested_action: str = Field(description="The suggested action: REFUND, REPLACE, TROUBLESHOOT, ESCALATE")
    draft_response: str = Field(description="A drafted response to the customer")

# Define the parser
parser = JsonOutputParser(pydantic_object=TicketAnalysis)

# Define the prompt template
system_prompt = """
You are a Senior Customer Support AI Agent.
STRICT INSTRUCTIONS:
1. Analyze the ticket for root cause and emotion.
2. Categorize into: [Hardware_Defect, Software_Bug, Billing_Dispute, Shipping_Delay, User_Error].
3. Determine urgency: [Low, Medium, High, Critical].
4. Suggest action: [REFUND, REPLACE, TROUBLESHOOT, ESCALATE].
5. Output STRICTLY valid JSON.

FEW-SHOT EXAMPLES:
User: "I was charged twice!" -> {{"category": "Billing_Dispute", "sentiment": "Frustrated", "urgency": "High", "suggested_action": "REFUND", "draft_response": "I apologize for the error. I have processed a refund."}}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{query}\n\n{format_instructions}")
])

# Create the chain
chain = prompt | llm | parser

@app.post("/analyze", response_model=TicketAnalysis)
async def analyze_ticket(ticket: TicketInput):
    try:
        response = chain.invoke({
            "query": ticket.complaint,
            "format_instructions": parser.get_format_instructions()
        })
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
