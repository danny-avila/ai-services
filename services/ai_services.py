# services\ai_services.py
from .ask_question import ask_question
from .tree_of_thoughts import tree_of_thoughts
from .api_chain import api_chain
from .api_agent import api_agent
from .nla_agent import nla_agent
from .code_interpreter import code_interpreter

AI_SERVICES = {
    "q&a": ask_question,
    "nla_agent": nla_agent,
    "code_interpreter": code_interpreter,
    "api_agent": api_agent,
    "api_chain": api_chain,
    "tree_of_thoughts": tree_of_thoughts
}