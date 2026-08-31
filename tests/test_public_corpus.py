#!/usr/bin/env python3
"""Mutation tests for the public-corpus policy."""

from itertools import permutations
from pathlib import Path
import unittest

from scripts.public_corpus import (
    PUBLIC_PROCESS_RULES,
    SEMANTIC_PERSON_GATE_RULE,
    check_repository,
    extract_pdf_text,
    scan_text,
)


class PublicCorpusMutationTest(unittest.TestCase):
    def assert_rejected(
        self, mutation: str, rule: str, *, path: str = "README.md"
    ) -> None:
        findings = scan_text(path, mutation)
        self.assertIn(rule, {finding.rule for finding in findings})

    @staticmethod
    def square_index(body: str, *, left: str = "", right: str = "") -> str:
        return "$" + left + chr(91) + body + right + chr(93) + "$"

    def test_process_mutations_are_rejected(self) -> None:
        cases = (
            (
                "This draft is " + "peer-" + "reviewed.",
                "publica" + "tion-process-status",
            ),

            ("Status: " + "A" + "I-assisted " + "review.", "vague-method-status"),

            ("The proof " + "needs human " + "validation.", "human-validation-status"),

            (
                "This is a " + "claimed complete " + "solution.",
                "self-undermining-status",
            ),

            ("Awaiting " + "sign-" + "off before release.", "approval-protocol"),

            ("Maintain a " + "reviewer " + "roster.", "role-protocol"),

            ("Status: " + "pending " + "evaluation.", "pending-evaluation-status"),

            ("Reviewer " + "assignment: named participant.", "assignment-protocol"),

            ("Release " + "requires a human.", "per" + "son-dependent-gate"),

            ("Awaiting editor " + "approval.", "awaiting-personal-approval"),

            (
                "Rele" + "ase is blocked until a reviewer " + "approves it.",
                "passive-per" + "son-gate",
            ),

            (
                "Submis" + "sion is contingent on expert " + "approval.",
                "contingent-per" + "son-gate",
            ),

            (
                "Publica" + "tion is subject to committee " + "approval.",
                "contingent-per" + "son-gate",
            ),

            (
                "Do not rele" + "ase before committee " + "approval.",
                "per" + "son-approval-precondition",
            ),

            (
                "The manuscript may be sub"
                + "mitted "
                + "only after editor "
                + "approval.",
                "per" + "son-approval-precondition",
            ),

            (
                "A reader must " + "approve comple" + "tion.",
                "mandated-per" + "son-approval",
            ),

            (
                "Reviewer approval " + "is required before rele" + "ase.",
                "per" + "son-approval-prerequisite",
            ),

            (
                "Submis" + "sion cannot proceed without expert approval.",
                "without-per" + "son-approval-gate",
            ),

            (
                "Assign " + "Dr. X to " + "evaluate the proof before rele" + "ase.",
                "assignment-evaluation-protocol",
            ),
        )
        self.assertEqual(
            {rule for rule, _ in PUBLIC_PROCESS_RULES},
            {rule for _, rule in cases},
        )
        for mutation, rule in cases:
            with self.subTest(rule=rule):
                self.assert_rejected(mutation, rule)

    def test_order_independent_person_gate_mutations_are_rejected(self) -> None:
        mutations = (
            "Rele" + "ase hinges on spec" + "ialist appro" + "val.",

            "Obtain ex" + "pert appro" + "val before submis" + "sion.",

            "Dr. X will evalu" + "ate the proof before rele" + "ase.",

            "Appro" + "val from a refe" + "ree determines publica" + "tion.",

            "Rele" + "ase hinges on\nspec" + "ialist appro" + "val.",

            "A spec"
            + "ialist, e.g. Dr. X, will appro"
            + "ve the rele"
            + "ase.",

            "A per"
            + "son will vet the proof before the pre"
            + "print is posted.",

            "A mathe"
            + "matician must authorize the repository update.",

            "Submis"
            + "sion follows faculty consent.",

            "Expert permis"
            + "sion is needed before rele"
            + "ase.",

            "Publica"
            + "tion awaits a scholar's verifi"
            + "cation.",

            "A refe"
            + "ree's clearance determines whether the paper is sub"
            + "mitted.",
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.assert_rejected(
                    mutation, SEMANTIC_PERSON_GATE_RULE
                )

        semantic_terms = (
            "A spec" + "ialist is involved.",
            "Appro" + "val is required.",
            "Rele" + "ase follows.",
        )
        for ordering in permutations(semantic_terms):
            mutation = " ".join(ordering)
            with self.subTest(ordering=ordering):
                self.assert_rejected(mutation, SEMANTIC_PERSON_GATE_RULE)

    def test_person_gate_terms_in_adjacent_sentences_are_rejected(self) -> None:
        mutations = (
            "A spec"
            + "ialist will inspect the proof. "
            + "Rele"
            + "ase follows appro"
            + "val.",
            "A revi"
            + "ewer will assess the argument. "
            + "The manuscript can then be sub"
            + "mitted.",
            "Revi"
            + "ewers assessed the proof. "
            + "The papers will be rele"
            + "ased after approval.",
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.assert_rejected(mutation, SEMANTIC_PERSON_GATE_RULE)

    def test_index_notation_mutation_is_rejected(self) -> None:
        mutations = (
            self.square_index("G" + ":" + "M"),
            self.square_index("G" + ":" + r"\Phi(G)"),
            self.square_index("G" + ":" + r"H\cap K"),
            self.square_index("G" + ":" + r"M^g"),
            self.square_index(
                " G" + ":" + r"\Phi(G) ",
                left=r"\left",
                right=r"\right",
            ),
            self.square_index("G/Z" + ":" + "N_G(H)"),
            self.square_index(r"\operatorname{Aut}(G)" + ":" + "H"),
            self.square_index(
                r"\,G_1 \times G_2\," + ":" + r"\;H_1\cap H_2\,",
                left=r"\bigl",
                right=r"\bigr",
            ),
            self.square_index(r"G \rtimes K " + ":" + r" H \cap L"),
            self.square_index(r"(G \times K)" + r"\colon " + "H"),
            self.square_index("G" + r"\mathbin{:}" + "M"),
            "$"
            + (r"\lbr" + "ack")
            + r" G_1\times G_2\colon H "
            + (r"\rbr" + "ack")
            + "$",
            self.square_index(r"\widetilde{G}" + ":" + r"\langle x,y\rangle"),
            self.square_index(r"\langle x,y\rangle" + ":" + r"\langle x\rangle"),
            self.square_index(
                r"\overline{G}\middle" + ":" + r"\widehat{H}",
                left=r"\left",
                right=r"\right",
            ),
            self.square_index(
                r"\prescript{g}{}{G}" + ":" + r"\operatorname{Core}_G(H)"
            ),
            self.square_index("{}^gG" + ":" + r"\langle x\rangle"),
            self.square_index(r"F^*(G)" + ":" + "1"),
            self.square_index("\n  G_1 \\times G_2\n  " + ":" + "\n  H\n"),
            self.square_index("G" + r"\mathrel{\colon}" + "M"),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.assert_rejected(mutation, "nonstandard-subgroup-index")

    def test_generic_disclosure_mutations_are_rejected(self) -> None:
        mutations = (
            "Generative A" + "I was used in preparing this manuscript.",
            "An A" + "I system assisted with drafting and mathematical exploration.",
            "A" + "I was used to draft this paper.",
            "This manu" + "script was drafted with generative A" + "I.",
            "ChatG" + "PT helped draft the paper.",
            "An LL" + "M was used to revise this paper.",
            "ChatG" + "PT helped\ndraft the paper.",
            "ChatG" + "PT, e.g. a tool, helped draft the paper.",
            "Language mod" + "els contributed to the exposition.",
            "A language-mod" + "el system polished the proof.",
            "Several LL" + "Ms supplied editorial suggestions.",
            "Chat" + "bots were consulted during revision.",
            "Clau" + "de proofread the manuscript.",
            "Generative mod" + "els helped organize the argument.",
            "A foundation mod" + "el checked the calculations.",
            "GP" + "T-5 suggested edits.",
            "Perplex" + "ity provided drafting advice.",
            "Artificial intel" + "ligence facilitated the revision.",
            "Language mod" + "els were applied to proofreading.",
            "Clau" + "de gave editorial feedback.",
            "An A" + "I assistant evaluated the exposition.",
            "The revision reli" + "ed on an LL" + "M.",
            "The polished prose was ow" + "ed to ChatG" + "PT.",
            "Drafting credit was attrib" + "uted to a language mod" + "el.",
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.assert_rejected(mutation, "duplicate-disclosure")

    def test_principal_disclosure_is_confined_to_one_section(self) -> None:
        root = Path(__file__).resolve().parents[1]
        source = (root / "paper" / "main.tex").read_text(encoding="utf-8")

        outside = "ChatG" + "PT helped draft this paper."
        outside_mutation = source.replace(
            r"\section*{Acknowledgments}",
            outside + "\n\n" + r"\section*{Acknowledgments}",
            1,
        )
        self.assert_rejected(
            outside_mutation, "duplicate-disclosure", path="paper/main.tex"
        )

        extra_body = "A language mod" + "el also proofread the paper."
        extra_body_mutation = source.replace(
            r"\begin{thebibliography}{9}",
            extra_body + "\n\n" + r"\begin{thebibliography}{9}",
            1,
        )
        self.assert_rejected(
            extra_body_mutation, "disclosure-body-count", path="paper/main.tex"
        )

        duplicate_heading = (
            r"\section*{Generative-" + "A" + "I disclosure}\n\n"
            + "An LL"
            + "M revised the paper.\n\n"
        )
        duplicate_heading_mutation = source.replace(
            r"\begin{thebibliography}{9}",
            duplicate_heading + r"\begin{thebibliography}{9}",
            1,
        )
        self.assert_rejected(
            duplicate_heading_mutation, "disclosure-count", path="paper/main.tex"
        )

        second_sentence = " ChatG" + "PT also revised the prose."
        disclosure_end = "for the manuscript."
        self.assertEqual(1, source.count(disclosure_end))
        second_sentence_mutation = source.replace(
            disclosure_end,
            disclosure_end + second_sentence,
            1,
        )
        self.assert_rejected(
            second_sentence_mutation,
            "disclosure-sentence-count",
            path="paper/main.tex",
        )

    def test_current_tracked_corpus_passes(self) -> None:
        root = Path(__file__).resolve().parents[1]
        findings, _ = check_repository(root)
        self.assertEqual([], findings)

    def test_principal_pdf_text_is_extracted(self) -> None:
        root = Path(__file__).resolve().parents[1]
        text, findings = extract_pdf_text(root / "paper" / "main.pdf", root)
        self.assertEqual([], findings)
        self.assertIn("finite soluble groups need not admit", text.casefold())

        outside = "ChatG" + "PT helped draft the paper.\n"
        outside_mutation = text.replace(
            "References\n", "References\n" + outside, 1
        )
        self.assert_rejected(
            outside_mutation, "duplicate-disclosure", path="paper/main.pdf"
        )

        extra_sentence = " ChatG" + "PT also proofread it."
        extra_sentence_mutation = text.replace(
            "takes responsibility for the manuscript.",
            "takes responsibility for the manuscript." + extra_sentence,
            1,
        )
        self.assert_rejected(
            extra_sentence_mutation,
            "disclosure-sentence-count",
            path="paper/main.pdf",
        )

    def test_archived_doi_matches_the_current_title(self) -> None:
        root = Path(__file__).resolve().parents[1]
        cff = (root / "CITATION.cff").read_text(encoding="utf-8")
        current_title = (
            "Finite Soluble Groups Need Not Admit Increasing Unrefinable "
            "Subgroup Chains"
        )
        self.assertIn(current_title, cff)
        self.assertIn("10.5281/zenodo.22213657", cff)


if __name__ == "__main__":
    unittest.main()
