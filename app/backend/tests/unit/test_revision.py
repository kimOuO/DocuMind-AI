"""D69: conditional verification-guided revision — the pure parts.

A draft that the deterministic checks fault may be revised once. What faults it
(triggers, by severity), what the second prompt holds, and how the final answer is
chosen are tested here without a model or a database.
"""

import uuid

from app.chat.citation_check import DoubtfulCitation
from app.chat.revision import (
    Candidate,
    build_revision_prompt,
    choose_final,
    find_triggers,
    invalid_citations,
    missing_coverage,
)
from app.chat.verification import (
    MislabelledNumber,
    NumberCheck,
    OverstatedClaim,
    UnresolvedNumber,
)
from app.llm.tokenizer import Qwen3TokenCounter
from tests.unit.test_number_verification import TABLE1_PAGE, TABLE_PAGE

DOC = uuid.uuid4()
CLEAN = NumberCheck([], [], [], [], [])
MISLABELLED = MislabelledNumber(
    "59.6%",
    ["Overall", "Mix", "-High"],
    [["Comprehensiveness", "Mix", "-High", "vs NaiveRAG"]],
    "In Mix, the Overall score falls to 59.6% (-High).",
)
OVERSTATED = OverstatedClaim(
    "LightRAG consistently outperforms the ablated versions across all datasets and metrics.",
    "LightRAG",
    [],
    53,
    8,
    ["Comprehensiveness / Agriculture: LightRAG 67.6% vs -Origin 75.2% (p. 8)"],
    "contradicted",
    None,
)
UNRESOLVED_CLAIM = OverstatedClaim(
    "LightRAG beats -Low in all cases.",
    "LightRAG",
    ["-Low"],
    0,
    0,
    [],
    "unresolved",
    "no shared cells",
)
DOUBT = DoubtfulCitation("GraphRAG must dismantle its community structure.", [3], [5], 0.0, 0.93)


# --- invalid citations ----------------------------------------------------------------


def test_citations_of_sources_that_were_not_given_are_invalid() -> None:
    assert invalid_citations("A claim [2]. Another [10]. A third [2, 12].", available=9) == [10, 12]
    assert invalid_citations("All fine [1][9].", available=9) == []


# --- triggers -------------------------------------------------------------------------


def test_a_mislabelled_number_an_overstated_claim_and_an_invalid_citation_are_hard() -> None:
    check = NumberCheck([], [], [MISLABELLED], [], [OVERSTATED])

    triggers = find_triggers(check, [], invalid=[10])

    assert [(t.kind, t.severity) for t in triggers] == [
        ("mislabelled_number", "hard"),
        ("overstated_claim", "hard"),
        ("invalid_citation", "hard"),
    ]
    assert "59.6%" in triggers[0].feedback and "Comprehensiveness" in triggers[0].feedback
    assert "-Origin 75.2%" in triggers[1].feedback
    assert "[10]" in triggers[2].feedback


def test_a_doubtful_citation_is_soft_and_can_be_switched_off() -> None:
    assert [(t.kind, t.severity) for t in find_triggers(CLEAN, [DOUBT], invalid=[])] == [
        ("doubtful_citation", "soft")
    ]
    assert find_triggers(CLEAN, [DOUBT], invalid=[], soft=False) == []


def test_unresolved_numbers_and_unresolved_claims_do_not_trigger() -> None:
    check = NumberCheck(
        [],
        [],
        [],
        [
            UnresolvedNumber(
                "57.6%", ["Overall", "Mix"], [["Overall", "Mix", "-High"]], "s", "missing"
            )
        ],
        [UNRESOLVED_CLAIM],
    )

    assert find_triggers(check, [], invalid=[]) == []


def test_missing_coverage_is_a_soft_trigger_naming_what_is_missing() -> None:
    [trigger] = find_triggers(CLEAN, [], invalid=[], missing=["-Origin"])

    assert (trigger.kind, trigger.severity) == ("incomplete", "soft")
    assert "-Origin" in trigger.feedback


# --- completeness (conservative) ------------------------------------------------------


def test_a_method_the_question_names_must_appear_in_the_answer() -> None:
    pages = [TABLE1_PAGE]
    question = "compare LightRAG with GraphRAG"

    assert missing_coverage(question, "LightRAG wins in most cases [1].", pages) == ["GraphRAG"]
    assert missing_coverage(question, "LightRAG beats GraphRAG in Legal [1].", pages) == []


def test_ablation_variants_are_required_only_for_an_ablation_question_on_a_variant_table() -> None:
    # TABLE_PAGE pairs NaiveRAG with -High, -Low and -Origin: a variant structure.
    question = "Performance of ablated versions of LightRAG"
    answer = (
        "Against LightRAG, -High drops to 65.2% and -Low to 64.0% in Agriculture "
        "Comprehensiveness [1]."
    )

    assert missing_coverage(question, answer, [TABLE_PAGE]) == ["-Origin"]
    # The same answer to a question that is not about the ablation: nothing required.
    assert missing_coverage("How does LightRAG retrieve?", answer, [TABLE_PAGE]) == []
    # A table without a variant structure (Table 1 pairs baselines with LightRAG): nothing.
    assert missing_coverage(question, answer, [TABLE1_PAGE]) == []


# --- the second prompt ----------------------------------------------------------------

SOURCES = [
    {
        "index": 1,
        "filename": "paper.pdf",
        "page_start": 8,
        "page_end": 8,
        "snippet": TABLE_PAGE.text,
    },
    {
        "index": 2,
        "filename": "paper.pdf",
        "page_start": 8,
        "page_end": 8,
        "snippet": "The -High variant removes high-order retrieval.",
    },
]


def test_the_revision_prompt_holds_question_sources_draft_and_feedback() -> None:
    counter = Qwen3TokenCounter()
    triggers = find_triggers(NumberCheck([], [], [MISLABELLED], [], []), [], invalid=[10])

    built = build_revision_prompt(
        "Performance of ablated versions of LightRAG",
        SOURCES,
        "Draft text [1][10].",
        triggers,
        counter,
        10_000,
    )

    assert built is not None
    prompt, max_output = built
    assert "Question: Performance of ablated versions of LightRAG" in prompt
    assert "[1] paper.pdf, page 8\n" in prompt and "[2] paper.pdf, page 8\n" in prompt
    assert "Draft answer:\nDraft text [1][10]." in prompt
    assert "59.6%" in prompt and "[10]" in prompt
    assert "only the revised answer" in prompt.lower()
    assert prompt.endswith("Revised answer:")
    assert max_output == 2_500
    assert counter.count(prompt) + max_output <= 10_000


def test_the_revision_is_skipped_when_the_budget_leaves_too_little_for_the_answer() -> None:
    counter = Qwen3TokenCounter()
    triggers = find_triggers(NumberCheck([], [], [MISLABELLED], [], []), [], invalid=[])
    long_draft = "A long draft. " * 400

    built = build_revision_prompt("q", SOURCES, long_draft, triggers, counter, 3_000)

    assert built is None


# --- choosing the final answer ---------------------------------------------------------


def hard(key: str):  # type: ignore[no-untyped-def]
    return find_triggers(
        NumberCheck(
            [], [], [MislabelledNumber(key, ["Overall"], [["Comprehensiveness"]], "s")], [], []
        ),
        [],
        invalid=[],
    )[0]


def soft():  # type: ignore[no-untyped-def]
    return find_triggers(CLEAN, [DOUBT], invalid=[])[0]


def test_without_a_revision_the_draft_is_final_and_its_status_follows_its_triggers() -> None:
    assert choose_final(Candidate("d", []), None).chosen == "draft"
    assert choose_final(Candidate("d", []), None).status == "verified"
    assert choose_final(Candidate("d", [soft()]), None).status == "unverified"


def test_a_revision_that_clears_the_hard_faults_is_chosen() -> None:
    choice = choose_final(Candidate("d", [hard("59.6%")]), Candidate("r", []))

    assert (choice.chosen, choice.status) == ("revision", "verified")


def test_a_revision_with_a_new_hard_fault_is_rejected_even_if_it_fixed_the_old_one() -> None:
    choice = choose_final(Candidate("d", [hard("59.6%"), soft()]), Candidate("r", [hard("83.6%")]))

    assert (choice.chosen, choice.status) == ("draft", "unverified")
    assert "new" in choice.reason


def test_a_revision_that_only_removes_doubts_is_chosen_but_equal_results_keep_the_draft() -> None:
    better = choose_final(Candidate("d", [hard("59.6%"), soft()]), Candidate("r", [hard("59.6%")]))
    same = choose_final(Candidate("d", [hard("59.6%")]), Candidate("r", [hard("59.6%")]))

    assert (better.chosen, better.status) == ("revision", "unverified")
    assert (same.chosen, same.status) == ("draft", "unverified")
