import Lean.Meta
import LeanCodePrompts
import LeanAide.TheoremElab
import LeanAide.Config
open Lean

set_option maxHeartbeats 10000000
set_option maxRecDepth 1000
set_option compiler.extract_closed false


def main (args: List String) : IO Unit := do
  initSearchPath (← Lean.findSysroot)
  let env ←
    importModules (loadExts := true) #[{module := `Mathlib},
    {module:= `LeanAide.TheoremElab},
    {module := `Mathlib}] {}
  let coreCtx : Core.Context :=
    {fileName := "", fileMap := {source:= "", positions := #[]}, maxHeartbeats := 1000000000, maxRecDepth := 10000}
  let core := promptsThmSplitCore
  let (succ, fail) ←  core.run' coreCtx {env := env} |>.runToIO'
  IO.println "Success"
  IO.println s!"parsed : {succ.size}"
  IO.println s!"failed to parse: {fail.size}"
  let succFile := System.mkFilePath ["data/parsed_thms.txt"]
  IO.FS.writeFile succFile <|
    succ.foldl (fun acc x => acc ++ s!"{x}\n") ""
  let failFile := System.mkFilePath ["data/unparsed_thms.txt"]
  IO.FS.writeFile failFile <|
    fail.foldl (fun acc x => acc ++ s!"{x}\n") ""
