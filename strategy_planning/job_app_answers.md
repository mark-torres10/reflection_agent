# Application questions

1. Can you describe a project where you tuned, fine-tuned, or architected an LLM system to achieve a very specific tone, personality, or behavioral style? What approach did you take, and how did you evaluate the quality of outputs?

I built an AI agent that drafts blog posts in a specific person’s voice (https://www.loom.com/share/f9bf8a4491c7465bb780e58fbb0104d7). The approach starts with the human: we collected a small set of their best posts, interview them on what “sounds like me” vs. what feels off, and turn that into a short style guide (tone, pacing, phrases they use or avoid, how they open and close pieces). That guide, plus a few real examples embedded in the prompts, becomes the core of the system. We set this up in steps so that the model learns over time what "sounds like" the person. Along the way, we ask for human feedback to make sure that the AI exactly matches criteria from the human facilitators, even developing our own models to grade outputs like the human experts would.

Quality is judged by the person whose voice it is, not by the model. We used a simple rubric: does this sound like them, is it specific rather than filler, and is it factually acceptable? We compared drafts side-by-side with real posts, captured specific failure modes ("they'd never say those words", "sounds too much like AI", "the AI made up facts"), and revised prompts and examples until those patterns disappeared.

## Question 2

Your facilitators would define what “remembered” means for this product: what’s worth carrying forward, what’s too private to store, and what continuity should feel like, and we'll design an intelligent AI memory layer so the technology follows their judgment and is not just a generic AI chatbot. Across days and journeys, we keep only a handful of lasting details, enough to make it feel personalized. Your facilitators’ way of working stays in charge: pacing, when to go deeper vs. hold space, and what good reflection sounds like. Those rules shape every reply; the notes support them, they do not replace them. For the MVP we start simple—short end-of-session notes plus real examples your team marks as strong vs. generic—and improve together using a short checklist (specific, calm, emotionally on-target) until people reliably feel understood. We only add more advanced customization (RAG, tuning, etc.) once we know exactly what still feels off.


## Question 3

Have you already collaborated with non-technical experts to turn their knowledge or methodology into AI prompts, workflows, or training data? Please share a relevant example.

Yes. I actively work with non-technical experts to convert their expertise into AI workflows. I am leading an initiative at Northwestern University to consolidate prompts (make this sound more impressive). In addition, I've run workshops with (multiple companies on how to adopt AI, see https://markptorres.com/ai_workflows/2025-12-17-is-this-worth-automating-with-ai) and I actively write about practical strategies for integrating AI workflows (https://markptorres.com/ai_workflows/)

Other automations I've built:

- AI agent for automating campaign analysis: https://www.loom.com/share/ac0835733d7a4dfa82ebdcfabe5940c8?sid=9928698f-e0b1-407d-804f-71ebca137ea8
- AI agent for automated content generation: https://www.loom.com/share/f9bf8a4491c7465bb780e58fbb0104d7
- AI agent for sales pipeline automation: https://www.loom.com/share/e392b1d9eb504a9bb2c06e09bfc66c87

- Example repo of prompts: ai_tools/agents at main · mark-torres10/ai_tools

I also run workshops advising experts on how to adopt AI workflows (need to spice this up to make it sound more impressive): https://docs.google.com/presentation/d/1ZhlBhpnedV5G7KTgcV0T9MW8jeWxplXMWzflRIw5kfE/edit?usp=sharing

I've also developed AI agent apps (... something something to automate their workflows, ...)

Yes, translating expert judgment into AI is core to how I work. At Northwestern I lead an initiative to turn scattered, researcher-built prompts into a shared library and repeatable workflows (https://github.com/mark-torres10/ai_tools/tree/main/agents). I run the same playbook with companies through live courses (https://docs.google.com/presentation/d/1ZhlBhpnedV5G7KTgcV0T9MW8jeWxplXMWzflRIw5kfE/edit?usp=sharing), workshops (https://markptorres.com/ai_workflows/2025-12-17-is-this-worth-automating-with-ai), and ongoing writing(https://markptorres.com/ai_workflows/): help experts decide what’s worth automating, capture their methodology, and iterate until they recognize their own standards in the output. I've developed many similar "turn expert insights into AI workflows" for clients (e.g., https://www.loom.com/share/ac0835733d7a4dfa82ebdcfabe5940c8?sid=9928698f-e0b1-407d-804f-71ebca137ea8 and https://www.loom.com/share/e392b1d9eb504a9bb2c06e09bfc66c87). Additionally, I'm quite familiar with AI in psychology, as I've published multiple papers on the subject (https://scholar.google.com/citations?user=d7CzCRMAAAAJ&hl=en) and my work on AI in psychology has been cited in avenues such as CNN and BBC. For your MVP I’d sit with your facilitators the same way: train the model to reflect the expertise of humans into a high quality, emotionally-aware AI experience.
