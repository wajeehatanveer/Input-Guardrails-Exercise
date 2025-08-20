from agents import(Agent, Runner, trace,
    input_guardrail, output_guardrail, InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered, GuardrailFunctionOutput)
import rich
from connection import config
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio

class Adminoutput(BaseModel):
    response: str
    change_student_timing: bool


Admin = Agent(
    name= """You are a Admin agent.Your task is to change the student class timing.
    """,
    output_type=Adminoutput
)

@input_guardrail
async def Admin_guardrail(ctx, agent, input):
    result = await Runner.run(Admin,
                              input,
                              run_config= config)
    rich.print(result.final_output) 

    return GuardrailFunctionOutput(
    output_info= result.final_output.response,
    tripwire_triggered= result.final_output.change_student_timing
)

#Main agent
Student_agent = Agent(
    name="Student Agent",
    instructions="Your are a Student agent",
    input_guardrails=[Admin_guardrail]
)

async def main():
        try:
            result = await Runner.run(Student_agent, 'i want to change my class timing', run_config=config)
            print("Your class timing cannot change")

        except InputGuardrailTripwireTriggered:
             print('OK i will change your class timing')


if __name__ == "__main__":
    asyncio.run(main())
