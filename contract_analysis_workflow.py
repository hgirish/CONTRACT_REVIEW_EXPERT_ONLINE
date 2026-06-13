import asyncio
from typing import Optional
from llama_index.core.workflow import (
    Workflow,
    StartEvent,
    StopEvent,
    Event,
    step,
    Context
)
from analysis import perform_risk_analysis, perform_compliance_check


class RiskAnalyzed(Event):
    text: str


class ComplianceChecked(Event):
    text: str


class ContractAnalysisWorkflow(Workflow):
    """
    Minimal workflow:
      - Takes `contract_path` and `policies_index` via StartEvent
      - Runs risk and compliance analyses in parallel
      - Merges results and returns {"risk": str, "compliance": str}
    """
    @step
    async def risk(self, ev: StartEvent) -> RiskAnalyzed:
        contract_path = ev.get("contract_path")
        policies_index = ev.get("policies_index")

        # Run the blocking work in a thread to keep the step async-friendly
        risk_text = await asyncio.to_thread(
            perform_risk_analysis, contract_path, policies_index
        )
        return RiskAnalyzed(text=risk_text)

    @step
    async def compliance(self, ev: StartEvent) -> ComplianceChecked:
        contract_path = ev.get("contract_path")
        policies_index = ev.get("policies_index")
        comp_text = await asyncio.to_thread(
            perform_compliance_check, contract_path, policies_index
        )
        return ComplianceChecked(text=comp_text)

    @step(pass_context=True)
    async def merge(
        self, ctx: Context, ev: RiskAnalyzed | ComplianceChecked
    ) -> StopEvent | None:
        # Wait for both results to arrive (fan-in)
        data: Optional[tuple[RiskAnalyzed, ComplianceChecked]] = ctx.collect_events(
            ev, [RiskAnalyzed, ComplianceChecked])
        if not data:
            return None
        risk_ev, comp_ev = data
        print("analysis completed on merge")
        return StopEvent(result={"risk": risk_ev.text, "compliance": comp_ev.text})
