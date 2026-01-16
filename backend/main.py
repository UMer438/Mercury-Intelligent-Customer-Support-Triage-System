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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# We will mount StaticFiles after defining the API routes so API takes precedence, 
# OR we mount it at specific path, but for SPA we usually catch all or mount root.
# Let's mount static first for distinct files, and catch-all for index.html


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

# Initialize Groq Client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    try:
        llm = ChatGroq(
            temperature=0,
            model_name="llama-3.3-70b-versatile",
            groq_api_key=GROQ_API_KEY
        )
        
        # Define the prompt template
        system_prompt = """
You are a Senior Customer Support AI Agent.
STRICT INSTRUCTIONS:
1. Analyze the ticket for root cause and emotion.
2. Categorize into: [Hardware_Defect, Software_Bug, Billing_Dispute, Shipping_Delay, User_Error].
3. Determine urgency: [Low, Medium, High, Critical].
4. Suggest action: [REFUND, REPLACE, TROUBLESHOOT, ESCALATE].
5. Output STRICTLY valid JSON.
6. Provide a professional, empathetic, and concise response.
FEW-SHOT EXAMPLES:
User: "I was charged twice!" -> {{"category": "Billing_Dispute", "sentiment": "Frustrated", "urgency": "High", "suggested_action": "REFUND", "draft_response": "I sincerely apologize for the billing error. I have processed a full refund for the duplicate charge, which should appear in your account shortly."}}
"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{query}\n\n{format_instructions}")
        ])

        # Create the chain
        chain = prompt | llm | parser
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        chain = None
else:
    print("WARNING: GROQ_API_KEY is not set. The API will return 500 errors.")
    chain = None

@app.post("/analyze", response_model=TicketAnalysis)
async def analyze_ticket(ticket: TicketInput):
    if not chain:
         raise HTTPException(status_code=500, detail="Server Configuration Error: GROQ_API_KEY is missing. Please verify the server settings.")
    
    try:
        response = chain.invoke({
            "query": ticket.complaint,
            "format_instructions": parser.get_format_instructions()
        })
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
app.mount("/_next", StaticFiles(directory="static/_next"), name="next")
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
