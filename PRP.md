<thinking>
Now I have a clear picture. The task is:

1. **Remove "Karl Dietz" references** from ALL devotionals (not just January) - 232 mentions across the entire file
2. **Rewrite those passages in first person plural** ("nós/nossa" perspective)
3. **Expand January devotionals under 300 words** (23 devocionais, min 257 words, need to reach 300+)

Key observations about Day 14 (Dia 14 - "Arrependimento É Atualizar a Mente"):
- 7 paragraphs, total ~292 words
- NO Karl Dietz mentions (this is a good example of the style without Karl)
- The writing style is very good: conversational, first-person-adjacent, biblical examples
- Already close to 300 words, just needs a bit more

For the Karl Dietz rewrite patterns:
- "Karl Dietz nos lembra que" → "Somos lembrados de que" / "Lembramos que"
- "Karl Dietz ensina que" → "Aprendemos que" / "Sabemos que"
- "A verdade em Karl Dietz revela que" → "Descobrimos que" / "A Bíblia revela que"
- "Karl Dietz explica que" → "Entendemos que"
- "Karl Dietz nos mostrou que" → "Reconhecemos que" / "Temos descoberto que"
- "Karl Dietz resume a essência" → "A essência disso é"
- "A verdade em Karl Dietz nos mostra que" → "A Escritura nos mostra que"

**Implementation strategy:**

Since there are 11 unique patterns and 232 total mentions, I can write a Python script that:
1. Uses regex to find all Karl Dietz sentence patterns
2. Replaces them with appropriate first-person-plural equivalents
3. For January devotionals under 300 words, adds a new closing paragraph

But for January expansion specifically, I need to be careful - Day 14 shows that the writing is already good style-wise, just needs more content. The challenge is that I can't generate AI content in a Python script directly.

Wait - actually, looking at Day 14 example: 7 paragraphs at ~292 words total. Each paragraph is 35-49 words. To get to 300+ words, I just need 1 more paragraph or expand a couple of existing ones.

For January devotionals that are under 300 words, the strategy should be:
1. First remove Karl Dietz mentions (which might reduce word count a bit)
2. Then add a new paragraph if still under 300 words

But the expansion for January requires creative writing - I can't easily automate that. 

Let me think about this differently. The user wants:
1. Remove Karl Dietz mentions - rewrite to first person plural
2. Expand January devotionals to 300+ words

For #1, I can do this with a Python script using regex patterns.
For #2, I need to generate content. Since the devotionals.js is already very large, I think the approach should be:
- Write a Python script that identifies which January devotionals are under 300 words
- For those, generate a closing paragraph programmatically

OR... I could use Claude to generate the expansion. The challenge is that devotionals.js is 944KB and I can't pass that to Claude easily.

Actually, let me think about this more practically:

**Step 1: Karl Dietz removal (regex script)**
- This can be done with a Python script
- 11 patterns → 11 replacement rules
- Pure mechanical transformation

**Step 2: January expansion**
- I need to generate content for 23 devotionals
- Each needs ~50-100 more words
- I could write a Python script that adds a generic "call to action" paragraph based on the devotional's theme

OR, I could write a separate Python script that generates a specific extra paragraph for each of the 23 January devotionals that need expansion, using the existing title and theme as context.

Actually, looking at Day 14's example: the writing is conversational, direct, and doesn't need Karl Dietz at all. The expansion needed is just adding 1 more paragraph.

For the plan, I'll:

1. **Script 1** - Karl Dietz removal: regex-based Python script
2. **Script 2** - January expansion: Python script that adds themed paragraphs to under-300 devotionals

For Script 2, I'll need to embed the expansion paragraphs directly into the Python script. Since this is creative content, I'll need to write them as part of the plan.

Let me look at the scope:
- 23 January devotionals under 300 words
- Need to add ~50-100 words each
- Each devotional has a title and theme that guides the content

I'll include the expansion paragraphs as embedded data in the Python script.

Now, for the plan file:

**Plan:**

1. Create `scripts/patch_devotionals.py`:
   - Step 1: Load devotionals.js
   - Step 2: For each devotional, apply Karl Dietz regex replacements
   - Step 3: For January devotionals under 300 words, append an expansion paragraph
   - Step 4: Write back to devotionals.js

The Karl Dietz patterns (based on our analysis):
```python
REPLACEMENTS = [
    ("Karl Dietz nos lembra que", "Precisamos nos lembrar de que"),
    ("A verdade em Karl Dietz nos lembra que", "Precisamos nos lembrar de que"),
    ("Karl Dietz ensina que", "Aprendemos que"),
    ("A verdade em Karl Dietz ensina que", "Aprendemos que"),
    ("Karl Dietz explica que", "Entendemos que"),
    ("A verdade em Karl Dietz explica que", "Entendemos que"),
    ("A verdade em Karl Dietz revela que", "Descobrimos que"),
    ("Karl Dietz revela que", "Descobrimos que"),
    ("A verdade em Karl Dietz nos mostra que", "A Escritura nos mostra que"),
    ("Karl Dietz nos mostrou que", "Reconhecemos que"),
    ("A verdade em Karl Dietz resume a essência", "Resumindo: a essência"),
    ("Karl Dietz resume a essência", "Resumindo: a essência"),
]
```

For the January expansion - I need to provide specific paragraphs for each of the 23 under-300-word devotionals. This is the creative part.

Since I don't know which specific days are under 300 after Karl Dietz cleanup, I should:
1. Run the Karl Dietz cleanup first
2. Re-count words
3. Then expand those still under 300

Let me plan accordingly.

Actually, from the previous analysis:
- 23 January devotionals are under 300 words
- The minimum is 257 words (Day 14)
- The Karl Dietz paragraphs being removed might reduce word count slightly

So I need to:
1. Remove Karl Dietz references (may remove ~15-20 words per devotional where they appear)
2. Add expansion paragraphs to January devotionals that end up under 300 words

For the expansion paragraphs, I'll write them as part of the Python script - they need to be thematically relevant. Given that all January devotionals are about "A Natureza de Deus" (The Nature of God), I can write generic but thematically appropriate closing paragraphs.

Let me now write the plan. This is a significant task that involves:
1. A Python script for Karl Dietz removal (~50 lines)
2. A Python script for January expansion (~100 lines with embedded content)
3. Git commit and push

Let me write the final plan to the plan file.
</thinking>