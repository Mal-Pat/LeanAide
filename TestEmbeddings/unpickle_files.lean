import Lean
import Batteries.Util.Pickle
import LeanAideCore.Aides

def writeAllEmbedData (filename : String) (content : EmbedData) : IO Unit := do
  let handle ← IO.FS.Handle.mk filename IO.FS.Mode.append
  content.forM (fun data : (String × String × Bool × String) × FloatArray =>
    match data with
    | ((a,b,c,d),_) => do
      handle.putStrLn a
      handle.putStrLn b
      handle.putStrLn (toString c)
      handle.putStrLn d)
  handle.flush
  IO.println s!"Content successfully written to {filename}"

def writeFirstEmbedData (filename : String) (content : EmbedData) : IO Unit := do
  let handle ← IO.FS.Handle.mk filename IO.FS.Mode.append
  content.forM (fun data : (String × String × Bool × String) × FloatArray =>
    match data with
    | ((a,_,_,_),_) => do
      handle.putStrLn a
      handle.putStrLn "\n"
      handle.putStrLn "==="
      handle.putStrLn "\n")
  handle.flush
  IO.println s!"Content successfully written to {filename}"

unsafe def readAndWrite (args : List String) : IO Unit := do
  let x ← unpickle (EmbedData) (args.getD 0
    ".lake/build/lib/mathlib4-concise-description-embeddings-v4.22.0.olean")
  writeFirstEmbedData (args.getD 1 "FAISS/unpickled1.txt") (x.1)



--#eval readAndWrite [".lake/build/lib/mathlib4-concise-description-embeddings-v4.22.0.olean", "FAISS/concise_desc_emb.txt"]

--#eval readAndWrite [".lake/build/lib/mathlib4-description-embeddings-v4.22.0.olean", "FAISS/desc_emb.txt"]

--#eval readAndWrite [".lake/build/lib/mathlib4-prompts-embeddings-v4.22.0.olean", "FAISS/prompt_emb.txt"]
