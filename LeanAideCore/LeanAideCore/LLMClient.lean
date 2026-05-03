import Lean
import LeanAideCore.Aides
import LeanAideCore.Template
import LeanAideCore.MathDoc
import LeanAideCore.Resources

open Lean Meta System LeanAide

#logIO leanaide.llm.info

variable [LeanAideBaseDir]

deriving instance Repr for Lean.Json

def optJson {α} [ToJson α] (k : String) (v : Option α) : Option (String × Json) :=
  v.bind fun val =>
    let j := toJson val
    if j == Json.mkObj [] || j == Json.null then none
    else some (k, j)

def reqJson {α} [ToJson α] (k : String) (v : α) : Option (String × Json) :=
  some (k, toJson v)

def dropNulls (fields : List (Option (String × Json))) : Json :=
  Json.mkObj (fields.filterMap id)

namespace OpenAI

structure Client where
  apiKey : String := ""
  organization : Option String := none
  project : Option String := none
  baseUrl : String := "https://api.openai.com/v1"
  deriving Repr

instance : Inhabited Client where
  default := {
    apiKey := "",
    organization := none,
    project := none,
    baseUrl := "https://api.openai.com/v1"
  }

inductive Role where
  | developer | system | user | assistant | tool | function
  deriving Inhabited, Repr, ToJson, FromJson

inductive ReasoningEffort where
  | none | minimal | low | medium | high | xhigh
  deriving Inhabited, Repr, Hashable, ToJson, FromJson, DecidableEq

structure Reasoning where
  effort : Option ReasoningEffort := none
  summary : Option String := none -- "auto" or "detailed" or "concise"
  deriving Inhabited, Repr

instance : ToJson Reasoning where
  toJson s := dropNulls [
    optJson "effort" s.effort,
    optJson "summary" s.summary
  ]

structure ImageUrl where
  url : String
  detail : Option String := none -- "auto" or "low" or "high"
  deriving FromJson, Repr, Inhabited

instance : ToJson ImageUrl where
  toJson s := dropNulls [
    reqJson "url" s.url,
    optJson "detail" s.detail
  ]

structure FileInput where
  file_id : Option String := none
  file_data : Option String := none -- base64 encoded
  filename : Option String := none
  deriving FromJson, Repr, Inhabited

instance : ToJson FileInput where
  toJson s := dropNulls [
    optJson "file_id" s.file_id,
    optJson "file_data" s.file_data,
    optJson "filename" s.filename
  ]

inductive ContentPart where
  | text (text : String)
  | imageUrl (image_url : ImageUrl)
  | file (file : FileInput)
  | inputAudio (data : String) (format : String) -- base64 encoded `dat`, "wav" or "mp3" `format`
  deriving Inhabited, Repr, FromJson

instance : ToJson ContentPart where
  toJson
    | .text t => Json.mkObj [("type", "text"), ("text", t)]
    | .imageUrl img => Json.mkObj [("type", "image_url"), ("image_url", toJson img)]
    | .file f => Json.mkObj [("type", "file"), ("file", toJson f)]
    | .inputAudio d f => Json.mkObj [("type", "input_audio"), ("input_audio", Json.mkObj [("data", d), ("format", f)])]

inductive Content where
  | str (s : String)
  | parts (p : Array ContentPart)
  deriving Inhabited, Repr, FromJson

def mkFileContent (fileID : String) : Content :=
  .parts #[.file { file_id := fileID }]

instance : ToJson Content where
  toJson
    | .str s => toJson s
    | .parts p => toJson p

structure JSONSchema where
  name : String
  schema : Json
  description : Option String := none
  strict : Option Bool := none
  deriving FromJson, Inhabited, Repr

instance : ToJson JSONSchema where
  toJson s := dropNulls [
    reqJson "name" s.name,
    reqJson "schema" s.schema,
    optJson "description" s.description,
    optJson "strict" s.strict
  ]

inductive ResponseFormat where
  | text
  | jsonObject
  | jsonSchema (schema : JSONSchema)
  deriving Repr, FromJson

instance : ToJson ResponseFormat where
  toJson
    | .text => Json.mkObj [("type", "text")]
    | .jsonObject => Json.mkObj [("type", "json_object")]
    | .jsonSchema s => Json.mkObj [("type", "json_schema"), ("json_schema", toJson s)]

structure JSONSchemaConfig where
  type : String := "json_schema"
  name : String
  schema : Json
  description : Option String := none
  strict : Option Bool := none
  deriving FromJson, Inhabited, Repr

instance : ToJson JSONSchemaConfig where
  toJson s := dropNulls [
    reqJson "type" s.type,
    reqJson "name" s.name,
    reqJson "schema" s.schema,
    optJson "description" s.description,
    optJson "strict" s.strict
  ]

inductive ResponseFormatTextConfig where
  | text
  | jsonObject
  | jsonSchema (schemaConfig : JSONSchemaConfig)
  deriving Repr

instance : ToJson ResponseFormatTextConfig where
  toJson
    | .text => Json.mkObj [("type", "text")]
    | .jsonObject => Json.mkObj [("type", "json_object")]
    | .jsonSchema s => toJson s

structure ResponseTextConfig where
  format : Option ResponseFormatTextConfig := none
  verbosity : Option String := none -- "low" or "medium" or "high"
  deriving Inhabited, Repr

instance : ToJson ResponseTextConfig where
  toJson s := dropNulls [
    optJson "format" s.format,
    optJson "verbosity" s.verbosity
  ]

/- Chat Completions API -/

structure ChatMessage where
  role : Role
  content : Content
  name : Option String := none
  deriving FromJson, Inhabited, Repr

instance : ToJson ChatMessage where
  toJson s := dropNulls [
    reqJson "role" s.role,
    reqJson "content" s.content,
    optJson "name" s.name
  ]

def mkCMsg (role : Role) (msg : String) : ChatMessage :=
  { role := role, content := .str msg }

def attachFileID (role : Role) (fileID : String) : ChatMessage :=
  {
    role := role
    content := mkFileContent fileID
  }

structure ChatCompletionRequest where
  model : String := "gpt-5.4"
  messages : Json
  n : Option Nat := none -- number of chat completion choices
  reasoning_effort : Option ReasoningEffort := none
  response_format : Option ResponseFormat := none
  temperature : Option JsonNumber := none
  max_completion_tokens : Option Nat := none
  deriving FromJson, Inhabited, Repr

instance : ToJson ChatCompletionRequest where
  toJson s := dropNulls [
    reqJson "model" s.model,
    reqJson "messages" s.messages,
    optJson "n" s.n,
    optJson "reasoning_effort" s.reasoning_effort,
    optJson "response_format" s.response_format,
    optJson "temperature" s.temperature,
    optJson "max_completion_tokens" s.max_completion_tokens
  ]

structure ChatCompletionMessage where
  content : String
  role : Role
  deriving FromJson, ToJson, Inhabited, Repr

structure Choice where
  message : ChatCompletionMessage
  index : Nat
  deriving FromJson, ToJson, Inhabited, Repr

structure ChatCompletionResponse where
  id : String
  object : String
  created : Nat
  model : String
  choices : Array Choice
  usage : Option Json
  deriving FromJson, ToJson, Inhabited, Repr

namespace ChatCompletionResponse

def getChoiceIndex? (resp : ChatCompletionResponse) (i : Nat) : Option Choice :=
  resp.choices.find? (fun c => c.index == i)

def getContentIndex? (resp : ChatCompletionResponse) (i : Nat) : Option String :=
  match resp.getChoiceIndex? i with
  | none => none
  | some choice => choice.message.content

def getContents (resp : ChatCompletionResponse) : Array String :=
  resp.choices.map fun choice => choice.message.content

end ChatCompletionResponse

/- Responses API -/

structure ResponseInputFile where
  type      : String        := "input_file"
  detail    : Option String := none -- `low` or `high`
  file_id   : Option String := none
  file_data : Option String := none -- base64 encoded
  filename  : Option String := none
  file_url  : Option String := none
  deriving FromJson, Repr, Inhabited

instance : ToJson ResponseInputFile where
  toJson s := dropNulls [
    reqJson "type" s.type,
    optJson "detail" s.detail,
    optJson "file_id" s.file_id,
    optJson "file_data" s.file_data,
    optJson "filename" s.filename,
    optJson "file_url" s.file_url
  ]

inductive ResponseInputContent where
  | text (text : String)
  | file (file : FileInput)
  deriving Inhabited, Repr, FromJson

instance : ToJson ResponseInputContent where
  toJson
    | .text t => Json.mkObj [("type", "input_text"), ("text", t)]
    | .file f => Json.mkObj [("type", "input_file"), ("file", toJson f)]

inductive ResponseContent where
  | str (s : String)
  | parts (p : Array ContentPart)
  deriving Inhabited, Repr, FromJson

structure ResponseInputMessage where
  role : Role
  content : ResponseContent
  phase : Option String := none
  type : String := "message"
  deriving Inhabited, Repr

instance : ToJson ResponseInputMessage where
  toJson s := dropNulls [
    reqJson "role" s.role,
    reqJson "content" s.content,
    optJson "phase" s.phase,
    reqJson "type" s.type
  ]

structure ResponseRequest where
  model : Option String := "gpt-5.4"
  input : Array ResponseInputMessage
  background : Option Bool := none
  reasoning : Option Reasoning := none
  text : Option ResponseTextConfig := none -- contains response format
  tools : Option Json := none -- have to expand this
  deriving Inhabited, Repr

instance : ToJson ResponseRequest where
  toJson s := dropNulls [
    reqJson "model" s.model,
    reqJson "input" s.input,
    optJson "background" s.background,
    optJson "reasoning" s.reasoning,
    optJson "text" s.text,
    optJson "tools" s.tools
  ]

structure APIResponse where
  id : String
  object : String
  created_at : Nat
  output : Array Json
  usage : Option Json
  deriving FromJson, ToJson, Inhabited, Repr

/- API Call Method -/

def runCurl (client : Client) (method : String) (endpoint : String) (body : Option Json := none) (extraArgs : Array String := #[]) : MetaM <| Except String String := do
  let mut args := #["-s", "-X", method, client.baseUrl ++ endpoint,
    "-H", s!"Authorization: Bearer {client.apiKey}"]

  if let some org := client.organization then
    args := args.push "-H" |>.push s!"OpenAI-Organization: {org}"
  if let some proj := client.project then
    args := args.push "-H" |>.push s!"OpenAI-Project: {proj}"

  if ! extraArgs.isEmpty then
    args := args ++ extraArgs

  if let some payload := body then
    args := args ++ #["-H", "Content-Type: application/json"]
    args := args.push "-d" |>.push (payload.compress)

  traceAide `leanaide.llm.info s!"OpenAI API Call Payload: {body.getD Json.null}"

  let out ← IO.Process.output { cmd := "curl", args := args }
  if out.exitCode != 0 then
    traceAide `leanaide.llm.info s!"Curl failed with code {out.exitCode}: {out.stderr}"
    -- throw <| IO.userError s!"Curl failed with code {out.exitCode}: {out.stderr}"
    return .error out.stderr
  return .ok out.stdout

def parseJson {α} [FromJson α] [Inhabited α] (result : Except String String) : MetaM α := do
  match result with
  | .error _ => return default
  | .ok raw =>
    match Json.parse raw with
    | .error e =>
      traceAide `leanaide.llm.info s!"Error parsing JSON: {e}; source: {raw}"
      return default
    | .ok js => match fromJson? js with
              | .error e =>
                traceAide `leanaide.llm.info s!"Failed to parse JSON into struct: {e}; source: {js}"
                return default
              | .ok val => return val

def checkClient (client : Client) : IO Client := do
  match client.apiKey with
  | "" => return {client with apiKey := ← openAIKey}
  | _ => return client

/- Chat Completions Endpoints -/

namespace Chat

def create (req : ChatCompletionRequest) (client : Client := default) : MetaM ChatCompletionResponse := do
  let client ← checkClient client
  let reqJs := toJson req
  let result ← runCurl client "POST" "/chat/completions" reqJs
  parseJson result

def list (client : Client := default) : MetaM Json := do
  let client ← checkClient client
  let result ← runCurl client "GET" "/chat/completions"
  parseJson result

def get (id : String) (client : Client := default) : MetaM Json := do
  let client ← checkClient client
  let result ← runCurl client "GET" s!"/chat/completions/{id}"
  parseJson result

def update (id : String) (metadata : Json) (client : Client := default) : MetaM Json := do
  let client ← checkClient client
  let payload := Json.mkObj [("metadata", metadata)]
  let result ← runCurl client "POST" s!"/chat/completions/{id}" payload
  parseJson result

def delete (id : String) (client : Client := default) : MetaM Json := do
  let client ← checkClient client
  let result ← runCurl client "DELETE" s!"/chat/completions/{id}"
  parseJson result

end Chat

/- Responses Endpoints -/

-- Responses is still under construction
-- DO NOT USE Responses

namespace Responses

def create (req : ResponseRequest) (client : Client := default) : MetaM APIResponse := do
  let client ← checkClient client
  let reqJs := toJson req
  let result ← runCurl client "POST" "/responses" reqJs
  parseJson result

def get (id : String) (client : Client := default) : MetaM APIResponse := do
  let client ← checkClient client
  let result ← runCurl client "GET" s!"/responses/{id}"
  parseJson result

def cancel (id : String) (client : Client := default) : MetaM Json := do
  let client ← checkClient client
  let result ← runCurl client "POST" s!"/responses/{id}/cancel" (Json.mkObj [])
  parseJson result

def delete (id : String) (client : Client := default) : MetaM Json := do
  let client ← checkClient client
  let result ← runCurl client "DELETE" s!"/responses/{id}"
  parseJson result

def compact (id : String) (client : Client := default) : MetaM Json := do
  let client ← checkClient client
  let payload := Json.mkObj [("response_id", toJson id)]
  let result ← runCurl client "POST" "/responses/compact" payload
  parseJson result

end Responses

structure FileState where
  client : Client := default
  trackedFiles : Array <| String × String := #[]
  deriving Inhabited, Repr

abbrev FileM := StateT FileState MetaM

def runOpenAIM {α} (x : FileM α) (initialState : FileState) : MetaM (α × FileState) :=
  StateT.run x initialState

inductive FilePurpose where
  | assistants
  | batch
  | fine_tune
  | vision
  | user_data
  | evals
  deriving Inhabited, Repr, BEq, ToJson

instance : ToJson FilePurpose where
  toJson order := match order with
    | .assistants => .str "assistants"
    | .batch      => .str "batch"
    | .fine_tune  => .str "fine-tune"
    | .vision     => .str "vision"
    | .user_data  => .str "user_data"
    | .evals      => .str "evals"

inductive Order where
  | asc
  | desc
  deriving Inhabited, Repr, BEq

instance : ToJson Order where
  toJson order := match order with
    | .asc  => .str "asc"
    | .desc => .str "desc"

structure FileObject where
  id : String
  bytes : Nat
  created_at : Nat
  filename : String
  object : String := "file"
  purpose : String
  expires_at : Option Nat := none
  deriving Inhabited, Repr, FromJson, ToJson

structure FileDeleted where
  id : String
  deleted : Bool
  object : String := "file"
  deriving Inhabited, Repr, FromJson, ToJson

structure FileList where
  data : Array FileObject
  first_id : String
  has_more : Bool
  last_id : String
  object : String := "list"
  deriving Inhabited, Repr, FromJson, ToJson

structure ListFilesRequest where
  after : Option String := none
  limit : Option Nat := none
  order : Option Order := none
  purpose : Option FilePurpose := none
  deriving Inhabited, Repr

namespace Files

def list (req : ListFilesRequest := {}) (client : Client := default) : FileM FileList := do
  let client ← checkClient client
  let mut args := #[]

  if let some after := req.after then
    args := args ++ #["-d", s!"after=\"{after}\""]
  if let some limit := req.limit then
    args := args ++ #["-d", s!"limit={limit}"]
  if let some order := req.order then
    args := args ++ #["-d", s!"order=\"{toJson order}\""]
  if let some purpose := req.purpose then
    args := args ++ #["-d", s!"purpose=\"{toJson purpose}\""]

  if ! args.isEmpty then
    args := #["-G"] ++ args

  let raw ← runCurl client "GET" "/files" none args
  parseJson raw

def upload (filePath : String) (purpose : FilePurpose := .user_data) (expiry : Nat := 86400) (client : Client := default) : FileM FileObject := do
  let client ← checkClient client
  let purposeStr := match toJson purpose with
    | .str s => s
    | _      => "user_data"
  let args := #[
    "-F", s!"purpose={purposeStr}",
    "-F", s!"file=@{filePath}",
    "-F", s!"expires_after[anchor]=\"created_at\"",
    "-F", s!"expires_after[seconds]={expiry}"
  ]
  let raw ← runCurl client "POST" "/files" none args
  let fileObj ← parseJson raw

  modify fun s => { s with trackedFiles := s.trackedFiles.push (filePath, fileObj.id) }

  return fileObj

def delete (fileId : String) (client : Client := default) : FileM FileDeleted := do
  let client ← checkClient client
  let raw ← runCurl client "DELETE" s!"/files/{fileId}"
  let fileDel : FileDeleted ← parseJson raw

  if fileDel.deleted then
    modify fun s => { s with trackedFiles := s.trackedFiles.filter (fun (_, id) => id != fileId) }

  return fileDel

def retrieve (fileId : String) (client : Client := default) : FileM FileObject := do
  let client ← checkClient client
  let raw ← runCurl client "GET" s!"/files/{fileId}"
  parseJson raw

def retrieveContent (fileId : String) (client : Client := default) : FileM <| Except String String := do
  let client ← checkClient client
  runCurl client "GET" s!"/files/{fileId}/content"

end Files

end OpenAI
