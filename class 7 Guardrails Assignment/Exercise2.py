from agents import(Agent, OutputGuardrailTripwireTriggered, InputGuardrailTripwireTriggered, 
    input_guardrail, 
    output_guardrail, 
    GuardrailFunctionOutput, Runner, trace)
                   
from dotenv import load_dotenv
from connection import config
import rich
from pydantic import BaseModel
import asyncio

class ChildOutput(BaseModel):
    response: str
    istempExceed: bool


Father_agent = Agent(
    name = "Father Agent",
    instructions = """
    You are a Father agent.Your task is to check the child do not run AC temperature below 26C.
    If temperature is lower than 26C,father stopping his child to run below 26C.
    """,
    output_type= ChildOutput

)

@input_guardrail
async def Father_guardrail(ctx, agent, input):
    result = await Runner.run(Father_agent,
                              input,
                              run_config= config)
    rich.print(result.final_output)

    return GuardrailFunctionOutput(
    output_info= result.final_output.response,
    tripwire_triggered= result.final_output.istempExceed
)

#main agent
Child_agent = Agent(
    name= "Child Agent",
    instructions= "You are a Child Agent",
    input_guardrails=[Father_guardrail]
)

async def main():
    try:
        result = await Runner.run(Child_agent, 'My AC temperature is 28C', run_config= config)
        print("run the AC")

    except InputGuardrailTripwireTriggered:
        print("Off the AC")

if __name__ == "__main__":
    asyncio.run(main())
