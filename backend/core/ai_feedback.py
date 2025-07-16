from transformers import pipeline, AutoTokenizer
import warnings
import torch
# Suppress model loading warnings
warnings.filterwarnings("ignore")

tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
analyzer = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    tokenizer=tokenizer,
    device="cuda" if torch.cuda.is_available() else "cpu",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

# TinyLlama (1.1B parameters - runs on CPU)
def get_ai_feedback(title, description, content, mode=""):
    if mode == "code":
        SYSTEM_PROMPT = """You are a senior Python developer. Provide specific feedback on:
        1. Correctness - Does it solve the problem?
        2. Efficiency - Time/space complexity
        3. Best Practices - PEP 8, readability
        4. Improvements - Concrete suggestions"""
        
        prompt = f"""<|system|>
        {SYSTEM_PROMPT}</s>
        <|user|>
        Problem: {title}
        Description: {description}
        Code:
        ```python
        {content}
        ```</s>
        <|assistant|>"""
    
    elif mode == "behavior":
        SYSTEM_PROMPT = """You are a senior HR specialist. Analyze this interview response using:
        1. STAR Format: {Situation, Task, Action, Result} 
        2. Specificity: Concrete examples?
        3. Impact: Quantifiable results?
        4. Suggestions: Clear improvements"""
        
        prompt = f"""<|system|>
        {SYSTEM_PROMPT}
        Question: {description}
        </s>
        <|user|>
        Candidate Response:
        {content}</s>
        <|assistant|>
        Analysis:
        - STAR Compliance:"""
    
    try:
        output = analyzer(
            prompt,
            max_new_tokens=350,
            temperature=0.2,  # More focused for behavioral
            repetition_penalty=1.15
        )
        feedback = output[0]['generated_text'].split("<|assistant|>")[-1].strip()
        
        # Format behavioral feedback better
        if mode == "behavior":
            feedback = feedback.replace("- ", "• ").replace("1. ", "\n1. ")
        return feedback
        
    except Exception as e:
        return f"⚠️ Analysis Error: {str(e)}"


# Rule-based fallback
def get_basic_feedback(code):
    feedback = []
    if "for i in range(len(" in code:
        feedback.append("🔍 Use direct iteration (for x in list) instead of range(len())")
    if " = " in code and " == " not in code:
        feedback.append("🔍 Possible assignment (=) where comparison (==) intended")
    return "\n".join(feedback) if feedback else "✅ Basic checks passed"