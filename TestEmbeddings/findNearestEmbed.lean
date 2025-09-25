import LeanCodePrompts.Translate
import LeanAideCore.Translator
import LeanAide.PromptBuilder
import LeanAideCore.PromptExampleBuilder


#check LeanAide.Translator.translateViewVerboseM

#check LeanAide.Translator.defaultDefM

#check LeanAide.PromptExampleBuilder.embedBuilder

#check LeanAide.PromptExampleBuilder.getPromptPairs

-- #eval LeanAide.PromptExampleBuilder.getPromptPairsOrderedAux (LeanAide.PromptExampleBuilder.embedBuilder 10 0 0) ("infinite odd numbers")

-- #eval LeanAide.Translator.translateViewVerboseM ("infinite odd numbers") (← LeanAide.Translator.defaultDefM)
