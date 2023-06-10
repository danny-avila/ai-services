# services\ai_services.py
from .ask_question import ask_question
from .tree_of_thoughts import tree_of_thoughts
from .api_chain import api_chain

AI_SERVICES = {
    "q&a": ask_question,
    "api_chain": api_chain,
    "tree_of_thoughts": tree_of_thoughts
}