#!/usr/bin/env python3
"""Fail-closed checks for the repository's public corpus."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Iterable


TEXT_SUFFIXES = {
    ".cff",
    ".g",
    ".md",
    ".py",
    ".sh",
    ".tex",
    ".txt",
    ".yaml",
    ".yml",
}
TEXT_BASENAMES = {".gitignore", "AGENTS.md", "LICENSE", "Makefile"}
BINARY_SUFFIXES = {".pdf"}


@dataclass(frozen=True)
class Finding:
    path: str
    rule: str
    line: int
    excerpt: str


def _pattern(*parts: str) -> re.Pattern[str]:
    return re.compile("".join(parts), re.IGNORECASE)


PERSON_ROLE = (
    r"(?:humans?|persons?|people|individuals?|someone|somebody|experts?|"
    r"reviewers?|readers?|editors?|committees?|referees?|"
    r"specialists?|evaluators?|assessors?|auditors?|advisors?|advisers?|"
    r"consultants?|panels?|boards?|peers?|teams?|maintainers?|"
    r"mathematicians?|scholars?|academics?|professors?|supervisors?|"
    r"authorities?|judges?|jurors?|faculty)"
)

GATE_NOUN = (
    r"(?:release|submission|readiness|completion|validation|publication|"
    r"circulation|archiving)"
)
GATE_VERB = r"(?:release|submit|publish|circulate|complete|validate|archive)"

APPROVAL_NOUN = r"(?:approval|validation|review|evaluation|endorsement|sign[\s-]*off)"
APPROVAL_VERB = (
    r"(?:approves?|validates?|reviews?|evaluates?|endorses?|signs?[\s-]+off)"
)
APPROVAL_PARTICIPLE = (
    r"(?:approved|validated|reviewed|evaluated|endorsed|signed[\s-]+off)"
)

PERSON_GATE_TERM = _pattern(
    r"\b(?:",
    PERSON_ROLE,
    "|",
    "Dr",
    r"s?\.?|",
    "Prof",
    r"s?\.?)\b",
)

EVALUATION_TERM = _pattern(
    r"\b(?:",
    APPROVAL_NOUN,
    "|",
    APPROVAL_VERB,
    "|",
    APPROVAL_PARTICIPLE,
    r"|assess(?:ment|ed|es|ing)?|certif(?:y|ies|ied|ication)|",
    r"inspect(?:ion|ed|s|ing)?|check(?:ed|s|ing)?|",
    r"verif(?:y|ied|ies|ying|ication)|",
    r"vet(?:ted|s|ting)?|audit(?:ed|s|ing)?|scrutini[sz](?:e|ed|es|ing)|",
    r"examin(?:e|ed|es|ing|ation)|accept(?:ed|s|ing|ance)|",
    r"consent(?:ed|s|ing)?|authori[sz](?:e|ed|es|ing|ation)|",
    r"confirm(?:ed|s|ing|ation)|recommend(?:ed|s|ing|ation)|",
    r"adjudicat(?:e|ed|es|ing|ion)|clearance|",
    r"attest(?:ed|s|ing|ation))\b",
)

PUBLICATION_GATE_TERM = _pattern(
    r"\b(?:releas(?:e|ed|es|ing)|submissions?|readiness|completions?|",
    r"publications?|circulation|archiving|submit(?:ted|s|ting)?|",
    r"publish(?:ed|es|ing)?|",
    r"circulat(?:e|ed|es|ing)|archiv(?:e|ed|es|ing)|preprints?|",
    r"repositor(?:y|ies)|post(?:ed|s|ing)?|upload(?:ed|s|ing)?|",
    r"deposit(?:ed|s|ing)?|disseminat(?:e|ed|es|ing|ion))\b",
)

PERSONAL_PERMISSION_TERM = _pattern(
    r"(?:\b",
    PERSON_ROLE,
    r"\s+(?:permission|authorization)\b|",
    r"\b(?:permission|authorization)\s+(?:from|by)\s+(?:an?\s+)?",
    PERSON_ROLE,
    r"\b)",
)


# These patterns are assembled from fragments so the checker and its mutation
# test remain members of the corpus that they scan.
PUBLIC_PROCESS_RULES = (
    (
        "publica" "tion-process-status",
        _pattern(r"\b", "peer", r"[\s-]*", "review", r"(?:ed|ing)?\b"),
    ),

    (
        "vague-method-status",
        _pattern(r"\b", "A", "I", r"[\s-]*assisted[\s-]*", "review", r"\b"),
    ),

    (
        "human-validation-status",
        _pattern(r"\b", "needs", r"\s+", "human", r"\s+", "validation", r"\b"),
    ),

    (
        "self-undermining-status",
        _pattern(r"\b", "claimed", r"\s+", "complete", r"\s+", "solution", r"\b"),
    ),

    (
        "approval-protocol",
        _pattern(r"\b", "sign", r"[\s-]*", "off", r"\b"),
    ),

    (
        "role-protocol",
        _pattern(
            r"\b(?:",
            "role",
            r"\s+",
            "matrix",
            "|",
            "reviewer",
            r"\s+",
            "roster",
            "|",
            "reader",
            r"\s+",
            "test",
            r")\b",
        ),
    ),

    (
        "pending-evaluation-status",
        _pattern(r"\b", "pending", r"\s+", "evaluation", r"\b"),
    ),

    (
        "assignment-protocol",
        _pattern(
            r"\b(?:",
            "reviewer",
            "|",
            "reader",
            "|",
            "expert",
            r")\s+",
            "assignment",
            r"\b",
        ),
    ),

    (
        "per" "son-dependent-gate",
        _pattern(
            r"\b",
            GATE_NOUN,
            r"\s+",
            r"(?:requires?|depends\s+on|awaits?)\s+(?:an?\s+)?",
            PERSON_ROLE,
            r"\b",
        ),
    ),

    (
        "awaiting-personal-approval",
        _pattern(
            r"\b(?:awaiting|pending)\s+",
            r"(?:(?:human|expert|reviewer|reader|editor|committee)\s+)?",
            r"(?:approval|validation|",
            "review",
            r")\b",
        ),
    ),

    (
        "passive-per" "son-gate",
        _pattern(
            r"\b",
            GATE_NOUN,
            r"\s+(?:is|remains|will\s+be)\s+",
            r"(?:blocked|delayed|withheld|prohibited|forbidden|not\s+permitted)\s+",
            r"(?:(?:until|unless)\s+(?:(?:an?\s+)?",
            PERSON_ROLE,
            r"\s+",
            APPROVAL_VERB,
            "|",
            APPROVAL_PARTICIPLE,
            r"\s+by\s+(?:an?\s+)?",
            PERSON_ROLE,
            r")|pending\s+(?:an?\s+)?",
            PERSON_ROLE,
            r"\s+",
            APPROVAL_NOUN,
            r")",
            r"\b",
        ),
    ),

    (
        "contingent-per" "son-gate",
        _pattern(
            r"\b",
            GATE_NOUN,
            r"\s+(?:is|remains|becomes)\s+(?:contingent|conditioned|subject)\s+",
            r"(?:on|upon|to)\s+(?:an?\s+)?",
            PERSON_ROLE,
            r"\s+",
            APPROVAL_NOUN,
            r"\b",
        ),
    ),

    (
        "per" "son-approval-precondition",
        _pattern(
            r"(?:\b(?:do\s+not|must\s+not|cannot|may\s+not)\s+",
            GATE_VERB,
            r"\b[^.\n]{0,60}\b(?:before|until|unless)\s+(?:an?\s+)?",
            PERSON_ROLE,
            r"\s+(?:",
            APPROVAL_NOUN,
            "|",
            APPROVAL_VERB,
            r")\b|",
            r"\b(?:the\s+)?(?:manuscript|paper|work|release|submission)\b",
            r"[^.\n]{0,60}\b(?:only\s+after|not\s+until)\s+(?:an?\s+)?",
            PERSON_ROLE,
            r"\s+(?:",
            APPROVAL_NOUN,
            "|",
            APPROVAL_VERB,
            r")\b)",
        ),
    ),

    (
        "per" "son-approval-prerequisite",
        _pattern(
            r"\b(?:an?\s+)?",
            PERSON_ROLE,
            r"\s+",
            APPROVAL_NOUN,
            r"\s+(?:(?:is|remains)\s+(?:required|mandatory|a\s+prerequisite)|",
            r"must\s+be\s+(?:obtained|secured|given))\s+",
            r"(?:before|for|prior\s+to)\s+(?:the\s+)?",
            GATE_NOUN,
            r"\b",
        ),
    ),

    (
        "without-per" "son-approval-gate",
        _pattern(
            r"\b",
            GATE_NOUN,
            r"\s+(?:cannot|may\s+not|must\s+not)\s+",
            r"(?:proceed|continue|occur|happen)\s+without\s+(?:an?\s+)?",
            PERSON_ROLE,
            r"\s+",
            APPROVAL_NOUN,
            r"\b",
        ),
    ),

    (
        "mandated-per" "son-approval",
        _pattern(
            r"\b(?:an?\s+)?",
            PERSON_ROLE,
            r"\s+(?:must|shall|needs?\s+to|is\s+required\s+to)\s+",
            APPROVAL_VERB,
            r"\b[^.\n]{0,60}\b",
            GATE_NOUN,
            r"\b",
        ),
    ),

    (
        "assignment-evaluation-protocol",
        _pattern(
            r"\b(?:assign|designate|appoint)\s+",
            r"(?:(?:an?\s+)?",
            PERSON_ROLE,
            r"|(?:Dr|Prof)\.?\s+[A-Z][A-Za-z.-]*)",
            r"[^.\n]{0,50}\bto\s+",
            APPROVAL_VERB,
            r"\b",
        ),
    ),
)

INDEX_DECORATION = re.compile(
    r"(?:\\(?:left|right|middle|bigl?|bigr?|Bigl?|Bigr?|biggl?|biggr?|Biggl?|Biggr?)\b"
    r"|\\(?:[,;:!]|quad\b|qquad\b)|~|\\hspace\s*\{[^}\n]*\})"
)
INDEX_COLON = re.compile(
    r"\\colon\b|\\(?:mathbin|mathrel|mathpunct)\s*"
    r"\{\s*(?::|\\colon\b)\s*\}"
)
INDEX_LEFT_BRACKET = re.compile(r"\\lbrack\b")
INDEX_RIGHT_BRACKET = re.compile(r"\\rbrack\b")

SQUARE_DELIMITED_EXPRESSION = re.compile(
    r"(?<!\\)\[(?P<body>(?:\\.|[^\\\]]){1,480})(?<!\\)\]"
)
GROUP_EXPRESSION_SIGNAL = re.compile(
    r"(?:(?<![A-Za-z])[A-Z](?![A-Za-z])|"
    r"\b(?:Aut|Inn|Out|Soc|Phi|Fit|GL|SL|PSL|PGL)\b|\\[A-Za-z]+\b)"
)

DISCLOSURE_HEADING = _pattern(
    r"\\section\*\{",
    "Generative",
    r"[\s-]*",
    "AI",
    r"\s+",
    "disclosure",
    r"\}",
)

RENDERED_DISCLOSURE_HEADING = _pattern(
    r"(?m)^[ \t]*",
    "Generative",
    r"[\s-]*",
    "AI",
    r"\s+",
    "disclosure",
    r"[ \t]*$",
)

DISCLOSURE_TOOL_NAMES = (
    _pattern("Anthropic", r"\s+", "Claude"),
    _pattern("OpenAI", r"\s+", "Codex"),
)

DISCLOSURE_MARKERS = (
    DISCLOSURE_HEADING,
    RENDERED_DISCLOSURE_HEADING,
    *DISCLOSURE_TOOL_NAMES,
)

AI_OR_TOOL_TERM = _pattern(
    r"\b(?:",
    "AI",
    r"(?:[\s-]+(?:assistant|system|tool|model)s?)?",
    "|",
    "LLMs?",
    "|",
    r"(?:(?:large|generative|foundation)[\s-]+)?language[\s-]+models?",
    "|",
    r"(?:generative|foundation)[\s-]+models?",
    "|",
    r"chatbots?",
    "|",
    r"Gen[\s-]*AI",
    "|",
    r"artificial[\s-]+intelligence",
    "|",
    "Chat",
    "GPT",
    r"|GPT(?:-[0-9][A-Za-z0-9.-]*)?|",
    "Claude",
    "|",
    "Gemini",
    "|",
    "Copilot",
    "|",
    "Codex",
    "|",
    "OpenAI",
    "|",
    "Anthropic",
    "|",
    "Perplexity",
    "|",
    "Grok",
    "|",
    "Llama",
    "|",
    "Mistral",
    r")\b",
)

AI_CONTRIBUTION_TERM = _pattern(
    r"\b(?:use(?:d|s|ing)?|utiliz(?:e|ed|es|ing|ation)|",
    r"leverag(?:e|ed|es|ing)|employ(?:ed|s|ing)?|consult(?:ed|s|ing|ation)|",
    r"involv(?:e|ed|es|ing|ement)|participat(?:e|ed|es|ing|ion)|",
    r"assist(?:ed|s|ing|ance)?|support(?:ed|s|ing)?|",
    r"help(?:ed|s|ing)?|aid(?:ed|s|ing)?|contribut(?:e|ed|es|ing|ion)|",
    r"draft(?:ed|s|ing)?|writ(?:e|es|ing|ten)|revis(?:e|ed|es|ing|ion)|",
    r"edit(?:ed|s|ing|orial)|generat(?:e|ed|es|ing|ion)|",
    r"prepar(?:e|ed|es|ing|ation)|explor(?:e|ed|es|ing|ation)|",
    r"develop(?:ed|s|ing|ment)|polish(?:ed|es|ing)?|proofread(?:s|ing)?|",
    r"improv(?:e|ed|es|ing|ement)|suggest(?:ed|s|ing|ion)s?|",
    r"summari[sz](?:e|ed|es|ing|ation)|translat(?:e|ed|es|ing|ion)|",
    r"formulat(?:e|ed|es|ing|ion)|organi[sz](?:e|ed|es|ing|ation)|",
    r"structur(?:e|ed|es|ing)|analy[sz](?:e|ed|es|ing|is)|",
    r"research(?:ed|es|ing)?|search(?:ed|es|ing)?|brainstorm(?:ed|s|ing)?|",
    r"debug(?:ged|s|ging)?|cod(?:e|ed|es|ing)|comput(?:e|ed|es|ing|ation)|",
    r"creat(?:e|ed|es|ing|ion)|produc(?:e|ed|es|ing|tion)|",
    r"provid(?:e|ed|es|ing)|suppl(?:y|ied|ies|ying)|offer(?:ed|s|ing)?|",
    r"responsib(?:le|ility)|check(?:ed|s|ing)?|verif(?:y|ied|ies|ying)|",
    r"facilitat(?:e|ed|es|ing|ion)|enabl(?:e|ed|es|ing)|",
    r"augment(?:ed|s|ing|ation)?|refin(?:e|ed|es|ing|ement)|",
    r"review(?:ed|s|ing)?|evaluat(?:e|ed|es|ing|ion)|",
    r"validat(?:e|ed|es|ing|ion)|inspect(?:ed|s|ing|ion)|",
    r"deriv(?:e|ed|es|ing|ation)|solv(?:e|ed|es|ing)|",
    r"compos(?:e|ed|es|ing|ition)|author(?:ed|s|ing|ship)?|",
    r"rewrit(?:e|es|ing|ten)|rewrote|redraft(?:ed|s|ing)?|",
    r"appl(?:y|ied|ies|ying)|ask(?:ed|s|ing)?|prompt(?:ed|s|ing)?|",
    r"giv(?:e|es|ing)|gave|benefit(?:ed|s|ing)?|",
    r"shap(?:e|ed|es|ing)|inform(?:ed|s|ing)?|advis(?:e|ed|es|ing|ory)|",
    r"feedback|input|guidance|comment(?:ed|s|ing)?|",
    r"collaborat(?:e|ed|es|ing|ion)|work(?:ed|s|ing)?|",
    r"redesign(?:ed|s|ing)?|correct(?:ed|s|ing|ion)|",
    r"simplif(?:y|ied|ies|ying|ication)|clarif(?:y|ied|ies|ying|ication)|",
    r"reli(?:ed|es|ance|ant|ying)|depend(?:ed|s|ing|ence)|",
    r"owe(?:d|s|ing)?|credit(?:ed|s|ing)?|attribut(?:e|ed|es|ing|ion))\b",
)

PRINCIPAL_MANUSCRIPT_SOURCE = "paper/main.tex"
PRINCIPAL_MANUSCRIPT_RENDER = "paper/main.pdf"
SEMANTIC_PERSON_GATE_RULE = "per" "son-evaluation-publication-gate"

SECTION_BOUNDARY = re.compile(
    r"\\(?:section\*?\s*\{|begin\s*\{thebibliography\})",
    re.IGNORECASE,
)

RENDERED_SECTION_BOUNDARY = re.compile(
    r"(?m)^[ \t]*(?:References|Acknowledgments|Code and data availability)[ \t]*$",
    re.IGNORECASE,
)


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _excerpt(text: str, offset: int) -> str:
    start = text.rfind("\n", 0, offset) + 1
    end = text.find("\n", offset)
    if end == -1:
        end = len(text)
    return text[start:end].strip()[:180]


def _paragraph_spans(text: str) -> Iterable[tuple[int, str]]:
    """Yield nonempty blank-line-delimited windows with source offsets."""
    start = 0
    for boundary in re.finditer(r"\n[ \t]*\n+", text):
        if text[start : boundary.start()].strip():
            yield start, text[start : boundary.start()]
        start = boundary.end()
    if text[start:].strip():
        yield start, text[start:]


def _disclosure_patterns(path: str) -> tuple[re.Pattern[str], re.Pattern[str]]:
    if path == PRINCIPAL_MANUSCRIPT_SOURCE:
        return DISCLOSURE_HEADING, SECTION_BOUNDARY
    if path == PRINCIPAL_MANUSCRIPT_RENDER:
        return RENDERED_DISCLOSURE_HEADING, RENDERED_SECTION_BOUNDARY
    raise ValueError(f"not a principal manuscript path: {path}")


def _principal_disclosure_region(
    path: str, text: str
) -> tuple[int, int, int] | None:
    """Return heading start, body start, and section end for one disclosure."""
    heading_pattern, boundary_pattern = _disclosure_patterns(path)
    headings = list(heading_pattern.finditer(text))
    if len(headings) != 1:
        return None
    heading = headings[0]
    boundary = boundary_pattern.search(text, heading.end())
    end = boundary.start() if boundary else len(text)
    return heading.start(), heading.end(), end


def _inside_region(offset: int, region: tuple[int, int, int] | None) -> bool:
    return bool(region and region[0] <= offset < region[2])


def _principal_disclosure_findings(path: str, text: str) -> list[Finding]:
    """Validate the unique disclosure section and its single prose paragraph."""
    findings: list[Finding] = []
    heading_pattern, _ = _disclosure_patterns(path)
    headings = list(heading_pattern.finditer(text))
    if len(headings) != 1:
        findings.append(
            Finding(
                path,
                "disclosure-count",
                1,
                f"expected exactly one heading, found {len(headings)}",
            )
        )
        return findings

    region = _principal_disclosure_region(path, text)
    if region is None:
        findings.append(
            Finding(
                path,
                "disclosure-section-boundary",
                _line_number(text, headings[0].start()),
                "could not isolate the disclosure section",
            )
        )
        return findings

    _, body_start, section_end = region
    body = text[body_start:section_end]
    paragraphs = [paragraph.strip() for _, paragraph in _paragraph_spans(body)]
    paragraphs = [paragraph for paragraph in paragraphs if paragraph]
    if len(paragraphs) != 1:
        findings.append(
            Finding(
                path,
                "disclosure-body-count",
                _line_number(text, body_start),
                f"expected one disclosure paragraph, found {len(paragraphs)}",
            )
        )
        return findings

    paragraph = paragraphs[0]
    sentence_endings = re.findall(r"[.!?](?=\s|$)", paragraph)
    if len(sentence_endings) != 1 or not paragraph.rstrip().endswith(
        (".", "!", "?")
    ):
        findings.append(
            Finding(
                path,
                "disclosure-sentence-count",
                _line_number(text, body_start),
                "expected exactly one complete disclosure sentence",
            )
        )
    if len(re.findall(r"\b[\w'-]+\b", paragraph)) > 80:
        findings.append(
            Finding(
                path,
                "disclosure-not-concise",
                _line_number(text, body_start),
                "disclosure exceeds 80 words",
            )
        )
    if not AI_OR_TOOL_TERM.search(paragraph) or not AI_CONTRIBUTION_TERM.search(
        paragraph
    ):
        findings.append(
            Finding(
                path,
                "disclosure-body-content",
                _line_number(text, body_start),
                "disclosure paragraph must identify a model or tool "
                "and its contribution",
            )
        )
    return findings


def _normalized_index_text(text: str) -> str:
    """Mask TeX delimiter and spacing decoration without changing offsets."""
    normalized = INDEX_DECORATION.sub(lambda match: " " * len(match.group(0)), text)
    normalized = INDEX_COLON.sub(
        lambda match: ":" + " " * (len(match.group(0)) - 1), normalized
    )
    normalized = INDEX_LEFT_BRACKET.sub(
        lambda match: "[" + " " * (len(match.group(0)) - 1), normalized
    )
    return INDEX_RIGHT_BRACKET.sub(
        lambda match: "]" + " " * (len(match.group(0)) - 1), normalized
    )


def _square_index_offsets(text: str) -> Iterable[int]:
    """Yield square-delimited colon expressions with group-like sides."""

    def group_like(side: str) -> bool:
        if GROUP_EXPRESSION_SIGNAL.search(side):
            return True
        if re.search(
            r"(?:\{\}\s*)?\^\s*(?:\{[^}\n]+\}|[a-z]+)\s*[A-Z]", side
        ):
            return True
        undecorated = re.sub(r"[\s{}()$]", "", side)
        return undecorated == "1"

    normalized = _normalized_index_text(text)
    for match in SQUARE_DELIMITED_EXPRESSION.finditer(normalized):
        body = match.group("body")
        for colon in re.finditer(":", body):
            left = body[: colon.start()]
            right = body[colon.end() :]
            if group_like(left) and group_like(right):
                yield match.start()
                break


def scan_text(path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[tuple[str, int, str]] = set()

    def add(rule: str, offset: int) -> None:
        line = _line_number(text, offset)
        excerpt = _excerpt(text, offset)
        key = (rule, line, excerpt)
        if key not in seen:
            findings.append(Finding(path, rule, line, excerpt))
            seen.add(key)

    if path in {PRINCIPAL_MANUSCRIPT_SOURCE, PRINCIPAL_MANUSCRIPT_RENDER}:
        for finding in _principal_disclosure_findings(path, text):
            key = (finding.rule, finding.line, finding.excerpt)
            if key not in seen:
                findings.append(finding)
                seen.add(key)

    for rule, pattern in PUBLIC_PROCESS_RULES:
        for match in pattern.finditer(text):
            add(rule, match.start())

    for paragraph_start, paragraph in _paragraph_spans(text):
        actor = PERSON_GATE_TERM.search(paragraph)
        evaluation = (
            EVALUATION_TERM.search(paragraph)
            or PERSONAL_PERMISSION_TERM.search(paragraph)
        )
        publication = PUBLICATION_GATE_TERM.search(paragraph)
        if actor and evaluation and publication:
            add(
                SEMANTIC_PERSON_GATE_RULE,
                paragraph_start
                + min(actor.start(), evaluation.start(), publication.start()),
            )

    for offset in _square_index_offsets(text):
        add("nonstandard-subgroup-index", offset)

    disclosure_region = (
        _principal_disclosure_region(path, text)
        if path in {PRINCIPAL_MANUSCRIPT_SOURCE, PRINCIPAL_MANUSCRIPT_RENDER}
        else None
    )
    for pattern in DISCLOSURE_MARKERS:
        for match in pattern.finditer(text):
            if disclosure_region and _inside_region(match.start(), disclosure_region):
                continue
            add("duplicate-disclosure", match.start())
    disclosure_scan_segments = [(0, text)]
    if disclosure_region:
        heading_start, _, section_end = disclosure_region
        disclosure_scan_segments = [
            (0, text[:heading_start]),
            (section_end, text[section_end:]),
        ]
    for segment_start, segment in disclosure_scan_segments:
        for paragraph_start, paragraph in _paragraph_spans(segment):
            tool = AI_OR_TOOL_TERM.search(paragraph)
            contribution = AI_CONTRIBUTION_TERM.search(paragraph)
            if tool and contribution:
                add(
                    "duplicate-disclosure",
                    segment_start
                    + paragraph_start
                    + min(tool.start(), contribution.start()),
                )
    return findings


def public_candidate_paths(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [root / item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def tracked_text(
    root: Path,
) -> tuple[list[tuple[Path, str]], list[Path], list[Finding]]:
    texts: list[tuple[Path, str]] = []
    pdfs: list[Path] = []
    findings: list[Finding] = []
    for path in public_candidate_paths(root):
        if not path.exists():
            # A tracked path deleted in the working tree is not part of the
            # current public corpus; a replacement path is reported by
            # ``git ls-files --others``.
            continue
        rel = path.relative_to(root).as_posix()
        if path.suffix.lower() in BINARY_SUFFIXES:
            pdfs.append(path)
            continue
        if path.name not in TEXT_BASENAMES and path.suffix.lower() not in TEXT_SUFFIXES:
            findings.append(
                Finding(
                    rel,
                    "unclassified-tracked-file",
                    1,
                    "add an explicit text or binary classification",
                )
            )
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            findings.append(Finding(rel, "unreadable-tracked-text", 1, str(exc)))
            continue
        texts.append((path, text))
    return texts, pdfs, findings


def extract_pdf_text(path: Path, root: Path) -> tuple[str, list[Finding]]:
    """Extract text and verify basic accessibility metadata, failing closed."""
    rel = path.relative_to(root).as_posix()
    extractor = shutil.which("pdftotext")
    if extractor is None:
        return "", [
            Finding(
                rel,
                "pdf-text-extractor-missing",
                1,
                "install pdftotext from Poppler",
            )
        ]
    try:
        result = subprocess.run(
            [extractor, "-enc", "UTF-8", str(path), "-"],
            cwd=root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        return "", [Finding(rel, "unreadable-pdf", 1, str(exc))]
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()[:180]
        return "", [Finding(rel, "unreadable-pdf", 1, detail)]
    try:
        text = result.stdout.decode("utf-8")
    except UnicodeDecodeError as exc:
        return "", [Finding(rel, "unreadable-pdf-text", 1, str(exc))]
    if not text.strip():
        return "", [Finding(rel, "empty-pdf-text", 1, "no searchable text extracted")]

    metadata_tool = shutil.which("pdfinfo")
    if metadata_tool is None:
        return text, [
            Finding(
                rel,
                "pdf-metadata-inspector-missing",
                1,
                "install pdfinfo from Poppler",
            )
        ]
    try:
        metadata_result = subprocess.run(
            [metadata_tool, str(path)],
            cwd=root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        return text, [Finding(rel, "unreadable-pdf-metadata", 1, str(exc))]
    if metadata_result.returncode != 0:
        detail = metadata_result.stderr.decode("utf-8", errors="replace").strip()[:180]
        return text, [Finding(rel, "unreadable-pdf-metadata", 1, detail)]
    metadata_text = metadata_result.stdout.decode("utf-8", errors="replace")
    metadata = {
        key.strip(): value.strip()
        for row in metadata_text.splitlines()
        if ":" in row
        for key, value in [row.split(":", 1)]
    }
    findings: list[Finding] = []
    for field in ("Title", "Author", "Subject", "Keywords"):
        if not metadata.get(field):
            findings.append(
                Finding(rel, "missing-pdf-metadata", 1, f"missing {field.lower()}")
            )
    if metadata.get("Tagged", "").casefold() != "yes":
        findings.append(
            Finding(rel, "untagged-pdf", 1, "PDF structure tagging is required")
        )
    return text, findings


def check_repository(root: Path) -> tuple[list[Finding], int]:
    texts, pdfs, findings = tracked_text(root)
    for path, content in texts:
        rel = path.relative_to(root).as_posix()
        findings.extend(scan_text(rel, content))
    for path in pdfs:
        content, pdf_findings = extract_pdf_text(path, root)
        findings.extend(pdf_findings)
        if content:
            findings.extend(scan_text(path.relative_to(root).as_posix(), content))

    principal = root / "paper" / "main.tex"
    principal_rows = [content for path, content in texts if path == principal]
    if len(principal_rows) != 1:
        findings.append(
            Finding(
                "paper/main.tex",
                "principal-manuscript-missing",
                1,
                "expected one tracked principal manuscript",
            )
        )

    return findings, len(texts) + len(pdfs)


def format_findings(findings: Iterable[Finding]) -> str:
    return "\n".join(
        f"{row.path}:{row.line}: {row.rule}: {row.excerpt}" for row in findings
    )


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    findings, count = check_repository(root)
    if findings:
        print(format_findings(findings), file=sys.stderr)
        return 1
    print(f"public corpus check passed ({count} tracked or candidate public artifacts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
