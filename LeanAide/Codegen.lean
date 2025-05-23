import Lean
import Qq
import LeanAide.Aides
import LeanAide.TranslateM
import LeanCodePrompts.Translate
import LeanAide.RunTactics
import LeanAide.AutoTactic

open Lean Meta Qq Elab

initialize registerTraceClass `LeanAide.Codegen

namespace LeanAide

namespace Codegen

/--
Attribute for generating Lean code, more precisely Syntax of a given category, from JSON data. More precisely, we generate `TranslateM <| Option <| TSyntax Q` from a JSON object, with the matching key as part of the attribute. In some cases, no syntax is generated as the goal is purely to have a side-effect to modify the context.

As the same statement can generate different syntax categories (e.g. `def` and `let`) this is not specified in the attribute. Instead the target category is part of the signature of the function.
-/
syntax (name := codegen) "codegen" str,* : attr

/-- Environment extension storing code generation lemmas -/
initialize codegenExt :
    SimpleScopedEnvExtension (Name × String) (Std.HashMap String Name) ←
  registerSimpleScopedEnvExtension {
    addEntry := fun m (n, key) => m.insert key n
    initial := {}
  }

def codegenKeyM (stx : Syntax) : CoreM (Array String) := do
  match stx with
  | `(attr|codegen $x) => do
    return #[x.getString]
  | `(attr|codegen $xs,*) => do
    let keys := xs.getElems
    return keys.map (·.getString)
  | _ => throwUnsupportedSyntax


initialize registerBuiltinAttribute {
  name := `codegen
  descr := "Lean code generator"
  add := fun decl stx kind => MetaM.run' do
    let declTy := (← getConstInfo decl).type
    let expectedType : Q(Type) :=
    q(Translator → Option MVarId  → (kind : SyntaxNodeKinds) → Json → TranslateM (Option (TSyntax kind)))
    unless ← isDefEq declTy expectedType do
      logWarning -- replace with error
        s!"codegen: {decl} has type {declTy}, but expected {expectedType}"
    let keys ← codegenKeyM stx
    logInfo m!"codegen: {decl}; keys: {keys}"
    for key in keys do
      codegenExt.add (decl, key) kind
}

def codegenMatch (key: String) : CoreM Name := do
  let some f :=
    (codegenExt.getState (← getEnv)).get? key | throwError
      s!"codegen: no function found for key {key}"
  return f

def codeFromFunc (goal? : Option MVarId) (translator: Translator) (f: Name) (kind : SyntaxNodeKinds) (source: Json) :
    TranslateM (Option (TSyntax kind)) := do
  let expectedType : Q(Type) :=
    q(Translator → Option MVarId  →  (kind : SyntaxNodeKinds) → Json → TranslateM (Option (TSyntax kind)))
  let f := mkConst f
  let code ←
    unsafe evalExpr
      (Translator → Option MVarId  → (kind : SyntaxNodeKinds) → Json → TranslateM (Option (TSyntax kind))) expectedType f
  code translator goal? kind source

/--
Given a JSON object, return the corresponding syntax by matching with `.getKVorType?` and then calling the function in the environment using `codeFromFunc`. The function is expected to return a `TranslateM (Option (TSyntax kind))`, where `kind` is the syntax category of the object.
-/
def getCode  (translator: Translator) (goal? : Option MVarId) (kind: SyntaxNodeKinds)
  (source: Json) :
    TranslateM (Option (TSyntax kind)) := do
  match source.getKVorType? with
  | some (key, source) => do
    let f ←  codegenMatch key
    let code ← codeFromFunc goal? translator f kind source
    return code
  | none => do
    throwError
      s!"codegen: no key or type found in JSON object {source}"

open Lean.Parser.Tactic
def emptyTacs : CoreM (TSyntax ``tacticSeq) := do
  let xs: Array (TSyntax `tactic) := #[]
  `(tacticSeq| $xs*)

def getCodeTacticsAux (translator: Translator) (goal :  MVarId)
  (sources: List Json) (accum: TSyntax ``tacticSeq) :
    TranslateM ((TSyntax ``tacticSeq) × Option MVarId) :=
  goal.withContext do
  match sources with
  | [] => do
    return (accum, goal)
  | source::sources => do
    let code? ← getCode translator (some goal) ``tacticSeq source
    match code? with
    | none => do -- error with obtaining tactics
      getCodeTacticsAux translator goal sources accum
    | some code => do
      let goal? ← runForSingleGoal goal code
      match goal? with
      | none => do -- tactics closed the goal
        return (accum, none)
      | some newGoal => do
        let newAccum ← appendTactics accum code
        getCodeTacticsAux translator newGoal sources newAccum

/--
Main helper for generating tactics from a list of JSON objects.
-/
def getCodeTactics (translator: Translator) (goal :  MVarId)
  (sources: List Json) :
    TranslateM (TSyntax ``tacticSeq) := do
  let accum ← emptyTacs
  let (tacs, goal?) ←
     getCodeTacticsAux translator goal sources accum
  match goal? with
  | none => do
    return tacs
  | some goal => do
    let autoTacs ←
      runTacticsAndGetTryThisI (← goal.getType) #[← `(tactic| auto?)]
    appendTactics tacs (← `(tacticSeq| $autoTacs*))

end Codegen

end LeanAide
