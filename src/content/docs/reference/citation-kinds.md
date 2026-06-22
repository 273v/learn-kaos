---
title: Citation kinds
description: The domains of legal, financial, accounting, and identifier citations kaos-citations recognizes.
---

`kaos-citations` recognizes ~60 typed citation kinds across four domains, returned as
typed objects with a `kind`, `raw`, `normalized`, and `span` (you used `extract_citations`
in [extract legal citations](/how-to/extract-citations)). Each kind is its own Pydantic
type, so you get structured fields specific to that citation family.

## Domains

**Legal** — case law and primary/secondary legal sources:
`CaseCitation`, `CFRCitation`, `FederalRegisterCitation`, `FederalRuleCitation`,
`ConstitutionCitation`, `ExecutiveActionCitation`, `CourtDocumentCitation`,
`AgencyAdjudicationCitation`, `AgencyManualCitation`, `BarEthicsOpinionCitation`,
`HereinafterCitation`, `IdCitation`, and more (statutes, regulations, court documents).

**Financial / regulatory** — securities and banking regulators:
`FINRARuleCitation`, `FINRARegulatoryNoticeCitation`, `FINRADisciplinaryCitation`,
`ExchangeRuleCitation`, `CFTCDocumentCitation`, `CFPBDocumentCitation`,
`FDICDocumentCitation`, `FedReserveRegulationCitation`, `FedReserveLetterCitation`,
`FFIECCallReportCitation`, `BaselFrameworkCitation`, `InternationalFinancialCitation`.

**Accounting / auditing** — standards bodies:
`AICPACitation`, `ASCCitation` (Accounting Standards Codification), `ASUCitation`,
`FASABCitation`, `GASBCitation`, `IFRSCitation`, `IAASBCitation`, `IESBACodeCitation`,
`GovernmentAuditCitation`, `IRSGuidanceCitation`.

**Identifier / academic** — stable identifiers and scholarship:
`DOICitation`, `ArXivCitation` (opt-in), `JournalCitation`, `ArchiveCitation`,
`InternetCitation`, `ElectronicMediaCitation`.

## Enumerate them live

The authoritative list is exposed as an MCP resource and in code:

```python
import kaos_citations as kc
print(kc.CITATION_KINDS_URI)   # the kaos-citations://kinds resource
```

Restrict extraction to specific kinds with `extract_citations(text, kinds=[...])`.

:::note
`span` is the absolute `(start, end)` offset in the source text; `normalized` is the
canonical form (e.g. `347 U.S. 483 (1954)`). They serve different purposes — `span` for
verification and linking, `normalized` for display and dedup.
:::
