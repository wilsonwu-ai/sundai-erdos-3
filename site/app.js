"use strict";
(() => {
  const $ = (id) => document.getElementById(id);
  const controls = { kind: $("set-kind"), limit: $("limit"), length: $("length"), custom: $("custom-numbers") };
  let patterns = [], currentPattern = 0, currentSet = [], currentLimit = 72;
  const observations = {
    all: "For all positive integers, the reciprocal sum is the harmonic series, which diverges. Every positive length has an immediate progression.",
    odds: "Odd numbers have a divergent reciprocal sum and an explicit progression of every length: 1, 3, 5, … .",
    primes: "The primes have a divergent reciprocal sum. Arbitrarily long progressions in the primes are known, but a finite search alone does not prove that fact.",
    multiples: "The reciprocal sum of positive multiples of 3 is one third of the harmonic series. Their progression formula is shown below.",
    powers: "The infinite set {1, 2, 4, 8, …} has reciprocal sum 2. It has no nonconstant three-term arithmetic progression. It does not satisfy the conjecture’s premise.",
    custom: "A finite set has a finite reciprocal sum. Any infinite continuation would need its own definition and proof."
  };
  const { isPrime, findProgressions } = window.ErdosExplorer;
  function readSet() {
    const kind=controls.kind.value, limit=Number(controls.limit.value);
    $("custom-control").hidden=kind!=="custom";
    $("custom-error").textContent=""; controls.custom.removeAttribute("aria-invalid");
    if (kind==="custom") {
      const tokens=controls.custom.value.trim().split(/[\s,;]+/).filter(Boolean);
      const invalid=tokens.some(token=>!/^\d+$/.test(token)||Number(token)<1||Number(token)>300);
      if (invalid) {
        $("custom-error").textContent="Please enter only whole numbers from 1 to 300, separated by commas or spaces.";
        controls.custom.setAttribute("aria-invalid","true"); return [];
      }
      return [...new Set(tokens.map(Number))].filter(n=>n<=limit).sort((a,b)=>a-b);
    }
    return Array.from({length:limit},(_,i)=>i+1).filter(n=>kind==="all" || (kind==="primes"&&isPrime(n)) || (kind==="odds"&&n%2===1) || (kind==="multiples"&&n%3===0) || (kind==="powers"&&Number.isInteger(Math.log2(n))));
  }
  function renderPattern() {
    const pattern=patterns[currentPattern], k=Number(controls.length.value);
    const equation=$("pattern-equation"); equation.replaceChildren();
    if (pattern) {
      pattern.terms.forEach((n,index)=>{ if(index) {const arrow=document.createElement("span");arrow.textContent="→";arrow.setAttribute("aria-hidden","true");equation.append(arrow);} equation.append(document.createTextNode(String(n))); });
      equation.setAttribute("aria-label",pattern.terms.join(", "));
      $("pattern-label").textContent=`${k}-TERM ARITHMETIC PROGRESSION`;
      $("pattern-gap").textContent=`STEP +${pattern.d}`;
      $("pattern-count").textContent=`${currentPattern+1} OF ${patterns.length.toLocaleString()} PATTERNS`;
    } else {
      equation.textContent="No pattern in this window."; equation.removeAttribute("aria-label");
      $("pattern-label").textContent=currentSet.length ? `${k}-TERM SEARCH COMPLETE` : "NO NUMBERS TO SEARCH";
      $("pattern-gap").textContent="FINITE SEARCH ONLY"; $("pattern-count").textContent="0 PATTERNS";
    }
    $("next-pattern").disabled=patterns.length<2;
    const members=new Set(currentSet), highlights=new Set(pattern?.terms||[]), fragment=document.createDocumentFragment();
    for (let n=1;n<=currentLimit;n++) {
      const cell=document.createElement("span");cell.className="number-cell"+(members.has(n)?" is-member":"")+(highlights.has(n)?" is-pattern":""); cell.textContent=String(n); cell.setAttribute("aria-hidden","true");fragment.append(cell);
    }
    $("number-strip").replaceChildren(fragment);
    $("number-strip").setAttribute("aria-label",`${controls.kind.options[controls.kind.selectedIndex].text}, from 1 to ${currentLimit}. ${currentSet.length} numbers in the set. ${pattern?`Highlighted progression: ${pattern.terms.join(", ")}, with common difference ${pattern.d}.`:`No ${k}-term arithmetic progression exists in this finite window.`}`);
  }
  function update() {
    currentLimit=Number(controls.limit.value);$("limit-value").textContent=String(currentLimit);
    currentSet=readSet();patterns=findProgressions(currentSet,Number(controls.length.value));currentPattern=0;
    $("set-count").textContent=`${currentSet.length} MEMBERS`;
    $("reciprocal-sum").textContent=currentSet.reduce((sum,n)=>sum+1/n,0).toFixed(5);
    $("set-observation").textContent=observations[controls.kind.value];renderPattern();
  }
  function updateConstruction() {
    const k=Number($("construction-length").value);$("construction-value").textContent=String(k);
    $("construction-sequence").textContent=Array.from({length:k},(_,i)=>3*(i+1)).join(", ");
  }
  for (const control of Object.values(controls)) control.addEventListener("input",update);
  $("next-pattern").addEventListener("click",()=>{ if(patterns.length){currentPattern=(currentPattern+1)%patterns.length;renderPattern();} });
  $("construction-length").addEventListener("input",updateConstruction);
  const evidence=window.PROJECT_EVIDENCE;
  if(evidence) {
    document.querySelectorAll("[data-repository-link]").forEach(link=>link.href=evidence.repository);
    $("result-summary").textContent=evidence.summary;$("result-description").textContent=evidence.description;$("evidence-note").textContent=evidence.note;
    for(const result of evidence.results) {
      const row=document.createElement("div");row.className="evidence-row";row.setAttribute("role","row");
      const claim=document.createElement("span");claim.setAttribute("role","cell");claim.textContent=result.claim;
      const status=document.createElement("span");status.setAttribute("role","cell");status.className=result.verified?"claim-verified":"claim-pending";status.textContent=result.status;
      row.append(claim,status);$("evidence-rows").append(row);
    }
  }
  update();updateConstruction();
})();
