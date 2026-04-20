# Production User Analysis — ElectroCoach Bot
**Snapshot date:** 2026-04-17
**Bot live since:** 2026-04-13 (4 days)
**Data source:** PostgreSQL production DB on VPS (193.124.56.183)

---

## 1. General Stats

| Metric | Value |
|---|---|
| Total registered users | 7 |
| Users who sent at least 1 message | 6 (86%) |
| Users who never messaged | 1 (Insaf @tjins) |
| Total sessions | 10 |
| Sessions with messages | 9 |
| Completed sessions (user pressed /stop) | 2 (20%) |
| Active (unclosed) sessions | 8 (80%) |
| Total messages | 211 |
| User messages | 107 |
| Bot messages | 104 |
| Avg messages per session (excl. empty) | 23.4 |
| Avg session duration (active chat time) | ~13 min (median), ~6–46 min range |
| Ratings collected | 2 (rating 1 — test; rating 7 — Alexey) |

---

## 2. User Profiles

### Кирилл (@Milenkij) — founder, test user
- **Registered:** 2026-04-13
- **Sessions:** 2
- **Messages:** 52 (25 user + 25 bot + 2 early test)
- **Reg-to-first-message:** 11 sec (instant)
- **Session 1:** 2 messages, 7 min, completed, rating 1 (test/throwaway)
- **Session 2:** 50 messages, 46 min, active (longest session by time)
- **Avg user message length:** 35 chars
- **Avg bot response length:** 370 chars
- **Avg user reply time:** 98 sec
- **Avg bot reply time:** 15.6 sec (slowest bot, likely early version or load)
- **Topic:** money, monetization of ElectroCoach product, founder self-identity
- **Notable:** asked about data privacy at end ("Хранишь ли ты мои ответы для аналитики?")

### Alexey (@shapovalov_vsegda) — power user, 3 sessions
- **Registered:** 2026-04-13
- **Sessions:** 3 (most of any user)
- **Messages:** 82 (41 user + 41 bot)
- **Reg-to-first-message:** 21 sec (instant)
- **Session 1 (sleep):** 30 messages, 6.4 min, active
- **Session 2 (self-worth):** 46 messages, 11.6 min, completed, rating 7
- **Session 3 (short):** 6 messages, 1.3 min, active
- **Avg user message length:** 15–28 chars (very short answers)
- **Avg bot response length:** 156–441 chars
- **Avg user reply time:** 24 sec (fastest responder)
- **Avg bot reply time:** 6.1 sec
- **Retention:** came back next day for session 2, then again same day for session 3
- **Topics:** insomnia, self-worth/income, identity crisis
- **Key insight from session 2:** bot uncovered loop "low income -> low self-worth -> paralysis -> can't change income"
- **User confirmed accuracy:** "Да, класс"
- **Resistance to action:** said "Никакой, сложно оочень" and "Не уверен, что это поможет" to proposed steps
- **"Не знаю" count:** 6 across sessions (highest)

### Анастасия (@minaeva) — business user
- **Registered:** 2026-04-14
- **Sessions:** 1
- **Messages:** 23 (12 user + 11 bot)
- **Reg-to-first-message:** 21 hours (registered day before, came back next day)
- **Session duration (active):** spread across 2 days (2026-04-15 to 2026-04-16)
- **Avg user message length:** 42 chars (moderate)
- **Avg bot response length:** 895 chars (longest bot responses — business analysis mode)
- **Max user message length:** 169 chars
- **Avg user reply time:** 189 sec (slowest — thinking about business decisions)
- **Avg bot reply time:** 8.7 sec
- **Topic:** STM vs co-branding decision for probiotic manufacturing business
- **GROW stage reached:** Options (bot provided 7 business variants with pros/cons)
- **Unexpected use case:** pure business consulting, not coaching/therapy
- **Session unfinished:** asked a follow-up question about co-branding but didn't complete decision

### Glebch (@iGlebch) — dropped off
- **Registered:** 2026-04-14
- **Sessions:** 1
- **Messages:** 12 (6 user + 6 bot)
- **Reg-to-first-message:** 1.1 min
- **Session duration:** started evening, resumed next morning (12.5 hour gap between msg 1 and msg 3)
- **Avg user message length:** 48 chars
- **Avg bot response length:** 277 chars
- **Avg user reply time:** 83 sec
- **Avg bot reply time:** 3.0 sec (fastest)
- **Topic:** anxiety, chaos in tasks, cash gap in business, fear of uncertainty
- **GROW stage reached:** early Reality (identified "don't know where to start" as blocker)
- **Dropped off after:** bot asked "what one result today would reduce anxiety most?" — no answer
- **Risk signal:** combined business + personal crisis, mentioned "кассовый разрыв" (cash gap)

### Insaf (@tjins) — silent registration
- **Registered:** 2026-04-15
- **Sessions:** 1 (empty)
- **Messages:** 0
- **Reg-to-first-message:** never sent one
- **Hypothesis:** pressed /start, saw welcome message, left without engaging
- **Activation failure:** 100% — bot failed to convert registration to first message

### Лера (@mini_lerka) — quick session, didn't finish
- **Registered:** 2026-04-16
- **Sessions:** 1
- **Messages:** 18 (9 user + 9 bot)
- **Reg-to-first-message:** 16 sec
- **Session duration:** 3.1 min (shortest real session)
- **Avg user message length:** 31 chars
- **Avg bot response length:** 322 chars
- **Avg user reply time:** 19.8 sec (second fastest)
- **Avg bot reply time:** 3.0 sec
- **Topic:** loss of work motivation, doing bare minimum, self-disappointment
- **GROW stage reached:** mid-Reality (identified "attitude to self changed first, then motivation dropped")
- **Key discovery:** "отношение к себе" changed before work motivation dropped
- **Session unfinished:** stopped after bot asked what changed in self-attitude
- **Gender note:** bot used masculine forms ("ты не выпал") for a female user

### darik (@dbazurina) — deepest emotional session
- **Registered:** 2026-04-16
- **Sessions:** 1
- **Messages:** 24 (12 user + 12 bot)
- **Reg-to-first-message:** 6 min
- **Session duration:** 21.2 min
- **Avg user message length:** 276 chars (by far the longest — 7x average)
- **Max user message length:** 625 chars (paragraph-length answers)
- **Min user message length:** 62 chars (even shortest is substantial)
- **Avg bot response length:** 1012 chars (longest bot responses)
- **Avg user reply time:** 106 sec (thinking deeply)
- **Avg bot reply time:** 8.8 sec
- **Topic:** breakup, grief, belief system crisis ("if you love, you fight")
- **GROW stage reached:** Options (bot provided 9 variants by Dilts levels)
- **Key therapeutic moves by bot:**
  - Separated "he didn't stay" from "I don't matter to him"
  - Identified belief system collision: her model of love vs his behavior
  - Named the double grief: loss of person + loss of trust in love as concept
- **User pushed back:** "Я не пытаюсь доказать свою значимость через это" — corrected bot's hypothesis
- **Bot adapted well** after pushback, shifted frame
- **Session unfinished:** stopped at Options, didn't reach Will/commitment

---

## 3. Engagement Metrics

### Activation Funnel
| Step | Count | % |
|---|---|---|
| Registered (/start) | 7 | 100% |
| Sent first message | 6 | 86% |
| Had 10+ messages in a session | 6 | 86% |
| Completed a session (/stop) | 2 | 29% |
| Gave a rating | 2 | 29% |
| Returned for 2nd session | 2 | 29% (Кирилл, Alexey) |
| Returned for 3rd session | 1 | 14% (Alexey) |

### Session Completion Problem
**80% of sessions are never closed.** Users chat and then leave without /stop.
- Possible causes: don't know about /stop, don't feel session is "done", forget, or context switch
- Impact: no ratings collected, no clean session boundaries, can't measure satisfaction at scale

### User Acquisition Timeline
| Date | New users | Sessions started |
|---|---|---|
| Apr 13 (Sun) | 2 (Кирилл, Alexey) | 3 |
| Apr 14 (Mon) | 2 (Анастасия, Glebch) | 3 |
| Apr 15 (Tue) | 1 (Insaf) | 1 |
| Apr 16 (Wed) | 2 (Лера, darik) | 2 |

**Growth:** steady 1–2 users/day, no spikes, likely organic/word-of-mouth

### Time of Day (Moscow Time)
| Hour | Messages | Note |
|---|---|---|
| 23:00 | 55 | **Peak** — late evening, reflection time |
| 00:00 | 27 | Night owls |
| 16:00 | 31 | Afternoon |
| 15:00 | 18 | |
| 12:00 | 26 | Lunch break |
| 13:00 | 20 | |
| 17:00 | 16 | |
| 10:00 | 10 | Morning |
| 14:00 | 6 | |
| 21:00 | 2 | |

**Insight:** People use the bot most at 23:00–00:00 MSK. This aligns with the "can't sleep / end-of-day reflection" pattern (Alexey's insomnia session was at 23:35 MSK).

### Day of Week
| Day | Messages |
|---|---|
| Mon | 55 |
| Tue | 81 (peak) |
| Wed | 18 |
| Thu | 57 |

**Note:** Bot has only been live since Sunday Apr 13, so this is not a full week. Tuesday peak may be coincidental.

---

## 4. Response Time Analysis

### Bot Response Time
| Metric | Value |
|---|---|
| Average | 8.5 sec |
| Median | 5.3 sec |
| Fastest (Glebch, Лера) | ~3.0 sec |
| Slowest (Кирилл) | 15.6 sec |

Bot responds fast enough for conversational flow. Under 10 sec median is good for a coaching context.

### User Response Time (excluding cross-day gaps)
| User | Avg reply time | Interpretation |
|---|---|---|
| Лера | 19.8 sec | Quick, short answers |
| Alexey | 23.9 sec | Fast responder, terse |
| Glebch | 82.7 sec | Thinking, or distracted |
| Кирилл | 98.1 sec | Multitasking (founder) |
| darik | 105.8 sec | Writing long, thoughtful answers |
| Анастасия | 189 sec | Business decision-making, long gaps |

**Insight:** User reply time correlates with message depth. darik takes longest but writes the most (276 chars avg). Alexey replies fastest but shortest (15 chars avg in session 2).

---

## 5. Bot Behavior Patterns

### "Я правильно понял?" frequency
| Session | Messages | Count | Ratio |
|---|---|---|---|
| Кирилл session 2 | 50 | 20 | **40%** of bot msgs |
| Alexey sleep | 30 | 9 | 60% |
| Alexey self-worth | 46 | 5 | 22% |
| Анастасия | 23 | 5 | 45% |
| Glebch | 12 | 4 | 67% |
| Лера | 18 | 4 | 44% |
| darik | 24 | 9 | 75% |

**Problem:** Bot says "Я правильно понял?" in 40–75% of its messages. This is excessive and can feel repetitive. The phrase appears 56 times across all sessions — nearly every other bot message. Good coaching uses varied reflection techniques, not a single catchphrase.

### "Не знаю" from users
| User | "Не знаю" count | Sessions |
|---|---|---|
| Alexey | 6 | across 3 sessions |
| darik | 2 | 1 session |
| All others | 0–1 | |

**Insight:** Alexey says "не знаю" most — correlates with his self-reported paralysis/indecision. The bot handles "не знаю" well by reframing or simplifying.

### GROW Stages Reached
| Session | Contract | Goal | Reality | Options | Will |
|---|---|---|---|---|---|
| Кирилл s2 | yes | yes | yes | yes | yes |
| Alexey sleep | yes | yes | yes | partial | no |
| Alexey self-worth | no | no | no | yes | yes |
| Alexey s3 | no | no | no | no | no |
| Анастасия | yes | no | no | yes | no |
| Glebch | no | no | no | no | no |
| Лера | no | no | no | no | partial |
| darik | no | no | no | yes | no |

**Insight:** Only Кирилл's test session went through full GROW. Most real users get stuck in Reality or jump to Options. The bot doesn't always label stages explicitly — it sometimes flows naturally without naming GROW/Dilts, which may actually be better for UX.

---

## 6. Message Length Analysis

### User Message Length (chars)
| User | Avg | Min | Max | Style |
|---|---|---|---|---|
| Alexey (s2) | 15 | 1 | 33 | Ultra-terse, one-word answers |
| Alexey (s1) | 28 | 6 | 75 | Short phrases |
| Лера | 31 | 8 | 60 | Brief but clear |
| Кирилл | 35 | 2 | 86 | Mixed |
| Анастасия | 42 | 3 | 169 | Business-style, moderate |
| Glebch | 48 | 6 | 87 | Moderate |
| darik | 276 | 62 | 625 | **Paragraph-length, deeply reflective** |

**Insight:** darik's average message is 7x the overall average. She writes like she's journaling — full thoughts, nuanced. This correlates with the depth of emotional processing. The bot adapts by writing longer responses (1012 chars avg) for her vs shorter for Alexey.

### Bot Message Length (chars)
| Session | Avg bot msg length | Note |
|---|---|---|
| Alexey s3 | 156 | Short exploratory |
| Alexey sleep | 240 | Practical, action-focused |
| Glebch | 277 | Moderate |
| Лера | 322 | Moderate |
| Кирилл | 370 | Detailed |
| Alexey self-worth | 441 | Deep reflection |
| Анастасия | 895 | Business analysis with lists |
| darik | 1012 | Longest — emotional + structural |

**Bot adapts length to context** — business and emotional depth sessions get longer responses.

---

## 7. Topic Clustering

### Primary Request Themes
| Theme | Users | % |
|---|---|---|
| Money / income / financial anxiety | 3 (Кирилл, Alexey, Glebch) | 50% |
| Self-worth / identity | 3 (Alexey, Лера, darik) | 50% |
| Anxiety / emotional state | 3 (Alexey, Glebch, Лера) | 50% |
| Relationships / grief | 1 (darik) | 17% |
| Business decision | 1 (Анастасия) | 17% |
| Insomnia | 1 (Alexey) | 17% |

### Underlying Patterns
Most users present a surface problem that unfolds into something deeper:
- "Хочу денег" -> "Хочу чувствовать что чего-то стою" (Alexey)
- "Нет мотивации на работу" -> "Изменилось отношение к себе" (Лера)
- "Как уснуть" -> "Есть рабочий способ, но не могу начать" (Alexey)
- "СТМ или кобрендинг?" -> "На каких условиях это вообще выгодно?" (Анастасия)

### B2C Segments That Showed Up Organically
| Segment from landing pages | Matched users |
|---|---|
| Founder in stagnation | Кирилл, Glebch |
| Existential crisis | Alexey |
| Life crisis | darik |
| Young professional in anxiety | Лера |
| Growth enthusiast | — |
| No budget for specialist | — |
| Serial entrepreneur | — |
| CEO/top manager | — |

**Missing segment:** Business decision-maker (Анастасия) — this use case has no landing page but came naturally.

---

## 8. Quality Assessment

### Helpfulness Score (subjective, based on dialogue analysis)
| User | Score | Evidence |
|---|---|---|
| Alexey (sleep) | 8/10 | Found concrete blocker, got to action, user said "Решает" |
| Alexey (self-worth) | 7/10 | Deep diagnosis, user confirmed "Да, класс", gave rating 7 |
| Анастасия | 9/10 | Structured business analysis, clear recommendation, actionable |
| Glebch | 5/10 | Right direction but session abandoned before value delivered |
| Лера | 6/10 | Good diagnosis but session too short, no action step |
| darik | 8/10 | Deep emotional work, separated key beliefs, 9 actionable options |

### Bot Strengths Observed
1. **Contracting works well** — asking for goal + time budget at start
2. **Dilts levels find real blockers** — especially Alexey's sleep session (environment -> behavior -> capability)
3. **Handles "не знаю" gracefully** — reframes, simplifies, offers alternatives
4. **Adapts depth to user** — terse for Alexey, expansive for darik, analytical for Анастасия
5. **Doesn't give advice** (mostly) — stays in question mode per coaching methodology
6. **Works for unexpected use cases** — business consulting, insomnia, grief

### Bot Weaknesses Observed
1. **"Я правильно понял?" overuse** — 56 times across 211 messages (27%). Needs variation: "Слышу это так:", "Если я правильно уловил:", just paraphrase without asking, etc.
2. **Gender misidentification** — addressed Лера as male ("ты не выпал"), Анастасия as male ("С чем пришёл")
3. **Options overload** — gave 7–9 options to darik and Анастасия. 3–4 would be more actionable.
4. **No session closure mechanism** — 80% of sessions stay open. No gentle nudge to close or rate.
5. **Breaks coaching mode for business queries** — with Анастасия, bot shifted into consultant/advisor mode. May need separate "advisor" vs "coach" modes.
6. **Кирилл session 1 had 0 bot messages** but message_count=2 — possible early bug where bot responses weren't stored.

---

## 9. Retention & Churn Signals

| Signal | Value |
|---|---|
| Return rate (2+ sessions) | 2/6 = 33% |
| Return rate (3+ sessions) | 1/6 = 17% |
| Time to return (Alexey) | 13 hours (session 1 -> 2), then 1.2 hours (session 2 -> 3) |
| Time to return (Кирилл) | 8 min (test -> real session) |
| Silent churn (registered, never messaged) | 1/7 = 14% |
| Abandoned sessions (< 6 user messages, no return) | 2 (Glebch, Alexey s3) |

### Churn Risk Assessment
| User | Risk | Why |
|---|---|---|
| Alexey | Low | 3 sessions, deep engagement, gave rating, likely returns |
| Анастасия | Medium | Got value but session spread over 2 days, may not have ongoing need |
| darik | Medium-Low | Deep session, unfinished, likely has more to process |
| Лера | Medium-High | Very short session, stopped mid-conversation |
| Glebch | High | Dropped off mid-session, complex crisis, may need more than bot |
| Insaf | Churned | Never sent a message |

---

## 10. Product Implications

### What the data suggests for next steps:

1. **Session completion UX:** Need auto-prompt to close/rate after inactivity (e.g., "Похоже, мы закончили. Хочешь оценить сессию от 1 до 10?")

2. **Gender detection:** Telegram provides first_name. Could use LLM or heuristic to infer gender for correct Russian grammatical forms.

3. **"Я правильно понял?" variation:** Add 5–8 alternative reflection patterns to the prompt.

4. **Follow-up for abandoned sessions:** After 24h of silence, send a gentle check-in ("Как дела после нашего разговора?")

5. **Business use case:** Анастасия showed demand for facilitated decision-making. Could be a separate product mode or landing page.

6. **Late-night usage peak (23:00+):** Marketing/positioning could lean into "когда не с кем поговорить в 3 ночи" angle.

7. **Onboarding for silent users:** Insaf registered but never wrote. The /start welcome message may need a stronger hook or first question.

8. **Options count:** Cap at 3–4 in GROW Options stage, not 7–9.
