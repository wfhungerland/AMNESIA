# Displacement Before Escalation, the Manuscript's LaTeX Build and Development Repositioning

*This chat turned a completed catch-up manuscript into a clean LaTeX build and then repositioned it from a trade-policy timing study into a development-economics contribution for World Development, without touching any empirical content.*

## Yield
1. The manuscript's empirical core is a pure sequencing result: across all four late-industrialising cases (Germany 1840-1914, Japan 1950-1990, Korea 1960-1997, China 1978-2024) and every coding variant, incumbent external constraint is dated after measurable sectoral displacement, never during absorption, with lags running from 0 to 37 years and no negative lag from any primary milestone (in the manuscript).
2. The identical empirical paper reads as either a trade-policy study or a development contribution through framing alone; the repositioning changed lexicon, literature anchor and case framing while leaving every datum, test and claim untouched (derived in this chat).
3. The three-tier claim hierarchy (sequencing, then TFP deceleration, then basic-research interpretation) is nested so that a referee who rejects the descriptive and interpretive layers still retains the falsifiable core, which is what lets one manuscript survive hostile review (in the manuscript).

## Findings
The substantive object throughout was a single argument: in four historical catch-up episodes, organised incumbent response (rhetorical escalation, binding policy instruments, technology controls) follows measurable displacement rather than preceding it during the technology-absorption phase. All four lag variables (rhetoric onset, rhetoric peak, first binding instrument, highest-salience instrument) are positive across all cases, incumbents and coding variants; the shortest lag is the 1981 Japanese automobile export restraint at one year after JP-1, the longest Britain's 1907 Patents Act at 37 years after the German dye displacement (in the manuscript). The one apparent negative-lag case (Germany measured from the 1893 steel crossover) resolves once the earlier c.1870 dye displacement is used as the primary milestone, which the 1885 Royal Commission independently corroborates (in the manuscript).

The reframing was the genuine intellectual work of this chat. The same manuscript was moved from trade-policy framing to development framing by three coordinated moves, none of which altered data, tests or claims (derived in this chat): a lexical swap (external constraint, policy escalation and incumbent intervention replacing trade retaliation, trade war and antidumping focus); a change of literature anchor (the developmental-state canon of Gerschenkron, Amsden, Wade, Evans and Chang made primary, with the trade-protection models of Grossman-Helpman and Bown-Crowley demoted to adjacent); and a change of case framing (China presented as the largest late-industrialising economy under tightening external constraint rather than as a geopolitical rival, with upstream semiconductor controls read as potentially compressing the absorption-to-origination sequence). The abstract was rebuilt on a fixed six-sentence developmental arc and held under 180 words.

The claim hierarchy is what makes the paper robust: Claim 1 (sequencing) is primary and falsifiable, its falsification condition being systematic negative lags across cases and variants; Claim 2 (TFP deceleration onset in the 0.60-0.73 range, US = 1.00, in the two non-German completed cases) is descriptive; Claim 3 (a basic-research transition constraint) is explicitly interpretive, weakened further because the pre-specified 1.0 percent government-plus-higher-education threshold was crossed by no economy in the set, so the original lag test is untestable as formulated and compositional documentation is substituted (in the manuscript).

On production, the sandbox forced several LaTeX substitutions worth keeping for any later recompile (established in this chat): newtxtext/newtxmath are unavailable, so mathptmx supplies the Times body; addmargin requires scrextend; the table glyphs checkmark, triangle and times require pifont; and agsm.bst is not installed, so the bibliography compiles under plainnat with natbib author-year. Compile order is pdflatex, then bibtex, then pdflatex twice. The delivered refs.bib holds all 38 references in full BibTeX form; two stray semicolon-separated \citep keys and three techreport entries missing an institution field were the only fixes needed for a clean bibtex run.

## Open and uncertain
The bibliography entries were carried in from prior sessions and formatted here, not verified against primary sources in this chat; none was fetched or checked, so their factual accuracy rests on earlier work, not on anything established here. The FRED Japan TFP value (0.640, 2023) and the various TFP, GERD and basic-research figures appear in the manuscript with full specificity but were not re-confirmed in this chat. The prompt's instruction to leave empirical scope untouched was followed, so no claim was tested or strengthened here; whether the development repositioning actually improves fit with World Development's audience is an editorial judgement, not a result. For any hard check of the numbers or sources, the manuscript should go through /verify.

## Literature
The load-bearing anchors of the repositioned argument are listed below with honest flags; the complete 38-source bibliography lives in the delivered refs.bib in full BibTeX form, so nothing is lost if this chat is deleted. All entries are flagged as mentioned rather than documented because this chat formatted them without independently verifying any against a primary source.

◐ Acemoglu, D., Aghion, P. and Zilibotti, F. (2006) 'Distance to frontier, selection, and economic growth', *Journal of the European Economic Association*, 4(1), pp. 37-74.
◐ Amsden, A. (1989) *Asia's Next Giant: South Korea and Late Industrialization*. New York: Oxford University Press.
◐ Bown, C.P. and Crowley, M.A. (2013) 'Import protection, business cycles, and exchange rates: Evidence from the Great Recession', *Journal of International Economics*, 90(1), pp. 50-64.
◐ Chang, H.-J. (2002) *Kicking Away the Ladder: Development Strategy in Historical Perspective*. London: Anthem Press.
◐ Eichengreen, B., Park, D. and Shin, K. (2012) 'When fast-growing economies slow down: International evidence and implications for China', *Asian Economic Papers*, 11(1), pp. 42-87.
◐ Evans, P. (1995) *Embedded Autonomy: States and Industrial Transformation*. Princeton: Princeton University Press.
◐ Gerschenkron, A. (1962) *Economic Backwardness in Historical Perspective*. Cambridge, MA: Belknap Press.
◐ Grossman, G.M. and Helpman, E. (1994) 'Protection for sale', *American Economic Review*, 84(4), pp. 833-850.
◐ Lind, J. and Mastanduno, M. (2025) 'Economic statecraft and technology competition: From CoCom to chip controls', *International Security*, 49(3), pp. 1-45.
◐ Mastanduno, M. (1992) *Economic Containment: CoCom and the Politics of East-West Trade*. Ithaca: Cornell University Press.
◐ Wade, R. (1990) *Governing the Market: Economic Theory and the Role of Government in East Asian Industrialization*. Princeton: Princeton University Press.
◐ World Bank (2024) *World Development Report 2024: The Middle Income Trap*. Washington, DC: World Bank Publications.

The remaining 26 sources (Bolt and van Zanden, Feenstra-Inklaar-Timmer, GGDC/PWT 11.0, FRED, OECD MSTI, IMF, Bank of Japan, NBS, Rodrik, Hsieh-Klenow, Rogowski, Irwin, Johnson, Khan, Moser, Moser and Voena, Brander and Spencer, Branstetter, Hayashi and Prescott, Agenor and Canuto ×2, Felipe et al., Eichengreen et al. 2014, OECD 1990) are held in refs.bib, all flagged ◐ mentioned on the same basis.

*Yield of a work chat from 26.08.2026, lightly checked, not /verify-audited. Flags: ● documented, ◐ mentioned, ○ unverified.*
