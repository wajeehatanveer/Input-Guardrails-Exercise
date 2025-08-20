from agents import(Agent, Runner, trace,
    input_guardrail, output_guardrail, InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered, GuardrailFunctionOutput)
import rich
from connection import config
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio

class Studentoutput(BaseModel):
    response: str
    is_school_student: bool


gate_keeper = Agent(
    name= """You are a gate keeper.Your task is to check the student uniform.Student uniform color is blue so cannot stop student to come in school.
    If student uniform is other,gatekeeper stopping student to come in school.
    """,
    output_type=Studentoutput
)


@input_guardrail
async def gate_keeper_guardrail(ctx, agent, input):
    result = await Runner.run(gate_keeper,
                              input,
                              run_config= config)
    rich.print(result.final_output) 

    return GuardrailFunctionOutput(
    output_info= result.final_output.response,
    tripwire_triggered= result.final_output.is_school_student
)

#Main agent
Student_agent = Agent(
    name="Student Agent",
    instructions="Your are a Student agent",
    input_guardrails=[gate_keeper_guardrail]
)

async def main():
        try:
            result = await Runner.run(Student_agent, 'what is age', run_config=config)
            print("come to school")

        except InputGuardrailTripwireTriggered:
             print('you are not come to school')


if __name__ == "__main__":
    asyncio.run(main())
