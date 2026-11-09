export type TraderInput = {
  name: string;
  inflow: number;
  outflow: number;
  sales: number;
  pastLoans: number;
  repaidOnTime: number;
};

export type Decision = "approve" | "decline" | "refer for review";

export type Scored = {
  score: number;
  decision: Decision;
  rationale: string;
};

export function scoreTrader(input: TraderInput): Scored {
  const net = input.inflow - input.outflow;
  const parts: string[] = [];
  let score = 0;

  // Liquidity: net mobile-money flow (0–40 points).
  if (net > 0) {
    const liquidity = Math.min(40, Math.round((net / 200000) * 40));
    score += Math.max(5, liquidity);
    parts.push(
      `a net monthly mobile-money flow of ${net.toLocaleString()} RWF shows money moving in and staying`,
    );
  } else {
    parts.push(`a net monthly mobile-money flow of ${net.toLocaleString()} RWF shows more leaving than arriving`);
  }

  // Trade: average monthly market sales (0–40 points).
  if (input.sales > 0) {
    const trade = Math.min(40, Math.round((input.sales / 500000) * 40));
    score += Math.max(5, trade);
    parts.push(`average monthly market sales of ${input.sales.toLocaleString()} RWF show a real, recurring trade`);
  } else {
    parts.push("no average monthly market sales were entered, so the trade itself is unproven here");
  }

  // Repayment history (0–20 points).
  if (input.pastLoans > 0) {
    const rate = input.repaidOnTime / input.pastLoans;
    const history = Math.round(rate * 20);
    score += history;
    if (rate >= 0.9) {
      parts.push(`a repayment history of ${input.repaidOnTime} of ${input.pastLoans} loans on time is strong evidence`);
    } else if (rate >= 0.6) {
      parts.push(`a repayment history of ${input.repaidOnTime} of ${input.pastLoans} loans on time is workable but uneven`);
    } else {
      parts.push(`a repayment history of ${input.repaidOnTime} of ${input.pastLoans} loans on time is weak`);
    }
  } else {
    parts.push("no past loans were entered, so there is no repayment history to weigh");
  }

  const decision: Decision = score >= 65 ? "approve" : score >= 40 ? "refer for review" : "decline";
  const lead =
    decision === "approve"
      ? "The figures support a yes."
      : decision === "refer for review"
        ? "The figures are mixed; the circle should look closer before deciding."
        : "The figures do not support a yes on this data alone.";
  const rationale = `${lead} ${input.name || "The trader"} shows ${parts.join(", ")}.`;

  return { score, decision, rationale };
}
