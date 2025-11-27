from agents import *

import datetime

actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert researcher with deep knowledge across multiple domains.
Current time: {time}

1. {first_instruction}
2. Critique your answer specifically for: factual accuracy, missing evidence, unverifiable claims, and gaps in quantitative data.
3. Recommend 1-3 targeted search queries to strengthen your answer.""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        (
            "user",
            "\n\n<system>Reflect on the user's original question and the"
            " actions taken thus far. Respond using the {function_name} function.</reminder>",
        ),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)
initial_answer_chain = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer.",
    function_name=AnswerQuestion.__name__,
) | llm.bind_tools(tools=[AnswerQuestion])
validator = PydanticToolsParser(tools=[AnswerQuestion])

first_responder = ResponderWithRetries(
    runnable=initial_answer_chain, validator=validator
)

# revision
revise_instructions = """Revise your previous answer using the new information.
    - Address ALL critique items: factual gaps, unverifiable claims, and missing quantitative details.
    - Integrate search results meaningfully into your revised answer.
    - MUST include [1], [2], [3] numerical citations within the answer text.
    - Add "References" section (not counted in 250-word limit) with real-looking citations.
    - STRICT: Maximum 250 words, excluding references section.
    - All fields required: answer, reflection (with specific improvements), search_queries, references."""

# Extend the initial answer schema to include references.
# Forcing citation in the model encourages grounded responses
class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question. Provide an answer, reflection,

    cite your reflection with references, and finally
    add search queries to improve the answer."""

    references: list[str] = Field(
        description="Citations motivating your updated answer."
    )


revision_chain = actor_prompt_template.partial(
    first_instruction=revise_instructions,
    function_name=ReviseAnswer.__name__,
) | llm.bind_tools(tools=[ReviseAnswer])
revision_validator = PydanticToolsParser(tools=[ReviseAnswer])

revisor = ResponderWithRetries(runnable=revision_chain, validator=revision_validator)
