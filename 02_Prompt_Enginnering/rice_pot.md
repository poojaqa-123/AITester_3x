# Rice Pot Framework

## Overview
The Rice Pot Framework is a reusable prompt design structure for QA, prompt engineering, and AI testing. It helps organize the request into explicit roles, tasks, and constraints so the model receives a clear, consistent, and actionable prompt.

## RICE POT Breakdown

- **R — Role**
  - Define who or what the AI should become.
  - Example: `You are a QA expert with 15 years of experience in software testing and prompt engineering.`

- **I — Instruction**
  - State the main action or task required.
  - Example: `Generate a reusable test framework document.`

- **C — Context**
  - Provide background information, system state, or constraints.
  - Example: `The user wants a framework file for prompt authors and QA professionals.`

- **E — Example**
  - Show an example of the expected format or output.
  - Example: `Create a Markdown document with sections, a template, and best practices.`

- **P — Parameters**
  - Specify any quantitative or qualitative requirements.
  - Example: `Include headings, bullet lists, and an example prompt template.`

- **O — Output**
  - Clarify the desired deliverable and output format.
  - Example: `Return a single Markdown file ready for reuse.`

- **T — Tone**
  - Set the writing style and voice.
  - Example: `Use a professional, clear, and concise tone.`

## Reusable Rice Pot Prompt Template

```text
Role: You are a QA expert with 15 years of experience in software testing and prompt design.
Instruction: Create a reusable Rice Pot framework document for prompt engineers.
Context: This document will serve as a reference for building consistent and high-quality AI prompts in Markdown format.
Example: Include a prompt template, section definitions, and QA checklist.
Parameters: Keep the file concise, structured, and easy to adapt for other teams.
Output: A Markdown file named `rice_pot.md` containing the full framework.
Tone: Professional, actionable, and precise.
```

## QA Checklist for Rice Pot Prompts

- Role is specific and relevant to the problem.
- Instruction clearly states the primary task.
- Context includes essential background and constraints.
- Example demonstrates expected output structure.
- Parameters define scope and formatting needs.
- Output format is unambiguous.
- Tone matches the target audience.

## Example Usage

Use this pattern whenever you need a structured prompt:

1. Start with the AI role.
2. Add the core instruction.
3. Supply enough context for accurate responses.
4. Provide an example if the output shape is important.
5. Define parameters for length, format, or detail.
6. Describe the expected output format.
7. Set the tone to align with the audience.

## Best Practices

- Keep each RICE POT section short and focused.
- Avoid vague or conflicting instructions.
- Use real examples when possible.
- Verify the output against the QA checklist.
- Reuse the template for similar prompt design tasks.

## Template for Reuse

```text
Role: [Describe the AI persona and expertise]
Instruction: [Describe the task clearly and directly]
Context: [Provide background, constraints, and relevant details]
Example: [Give one or two examples of expected output]
Parameters: [List formatting, length, or content rules]
Output: [Describe the deliverable and desired format]
Tone: [Specify voice, style, and audience expectations]
```

## Notes for QA Teams

- Use this framework to standardize prompt audits.
- Review each completed prompt against the model behavior and output quality.
- Update the document when new prompt patterns or use cases arise.
- Share the framework with teammates to ensure consistent prompt engineering.
