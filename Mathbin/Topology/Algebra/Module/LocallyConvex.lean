/-
Copyright (c) 2022 Anatole Dedecker. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Anatole Dedecker
-/
import Mathbin.Analysis.Convex.Topology

/-!
# Locally convex topological modules

A `locally_convex_space` is a topological semimodule over an ordered semiring in which any point
admits a neighborhood basis made of convex sets, or equivalently, in which convex neighborhoods of
a point form a neighborhood basis at that point.

In a module, this is equivalent to `0` satisfying such properties.

## Main results

- `locally_convex_space_iff_zero` : in a module, local convexity at zero gives
  local convexity everywhere
- `seminorm.locally_convex_space` : a topology generated by a family of seminorms is locally convex
- `normed_space.locally_convex_space` : a normed space is locally convex

## TODO

- define a structure `locally_convex_filter_basis`, extending `module_filter_basis`, for filter
  bases generating a locally convex topology
- show that any locally convex topology is generated by a family of seminorms

-/


open TopologicalSpace Filter Set

open TopologicalSpace

section Semimodule

/-- A `locally_convex_space` is a topological semimodule over an ordered semiring in which convex
neighborhoods of a point form a neighborhood basis at that point. -/
class LocallyConvexSpace (𝕜 E : Type _) [OrderedSemiring 𝕜] [AddCommMonoidₓ E] [Module 𝕜 E] [TopologicalSpace E] :
  Prop where
  convex_basis : ∀ x : E, (𝓝 x).HasBasis (fun s : Set E => s ∈ 𝓝 x ∧ Convex 𝕜 s) id

variable (𝕜 E : Type _) [OrderedSemiring 𝕜] [AddCommMonoidₓ E] [Module 𝕜 E] [TopologicalSpace E]

theorem locally_convex_space_iff :
    LocallyConvexSpace 𝕜 E ↔ ∀ x : E, (𝓝 x).HasBasis (fun s : Set E => s ∈ 𝓝 x ∧ Convex 𝕜 s) id :=
  ⟨@LocallyConvexSpace.convex_basis _ _ _ _ _ _, LocallyConvexSpace.mk⟩

theorem LocallyConvexSpace.of_bases {ι : Type _} (b : E → ι → Set E) (p : E → ι → Prop)
    (hbasis : ∀ x : E, (𝓝 x).HasBasis (p x) (b x)) (hconvex : ∀ x i, p x i → Convex 𝕜 (b x i)) :
    LocallyConvexSpace 𝕜 E :=
  ⟨fun x =>
    (hbasis x).to_has_basis (fun i hi => ⟨b x i, ⟨⟨(hbasis x).mem_of_mem hi, hconvex x i hi⟩, le_reflₓ (b x i)⟩⟩)
      fun s hs => ⟨(hbasis x).index s hs.1, ⟨(hbasis x).property_index hs.1, (hbasis x).set_index_subset hs.1⟩⟩⟩

theorem LocallyConvexSpace.convex_basis_zero [LocallyConvexSpace 𝕜 E] :
    (𝓝 0 : Filter E).HasBasis (fun s => s ∈ (𝓝 0 : Filter E) ∧ Convex 𝕜 s) id :=
  LocallyConvexSpace.convex_basis 0

theorem locally_convex_space_iff_exists_convex_subset :
    LocallyConvexSpace 𝕜 E ↔ ∀ x : E, ∀, ∀ U ∈ 𝓝 x, ∀, ∃ S ∈ 𝓝 x, Convex 𝕜 S ∧ S ⊆ U :=
  (locally_convex_space_iff 𝕜 E).trans (forall_congrₓ fun x => has_basis_self)

end Semimodule

section Module

variable (𝕜 E : Type _) [OrderedSemiring 𝕜] [AddCommGroupₓ E] [Module 𝕜 E] [TopologicalSpace E] [TopologicalAddGroup E]

theorem LocallyConvexSpace.of_basis_zero {ι : Type _} (b : ι → Set E) (p : ι → Prop) (hbasis : (𝓝 0).HasBasis p b)
    (hconvex : ∀ i, p i → Convex 𝕜 (b i)) : LocallyConvexSpace 𝕜 E := by
  refine'
    LocallyConvexSpace.of_bases 𝕜 E (fun (x : E) (i : ι) => (· + ·) x '' b i) (fun _ => p) (fun x => _) fun x i hi =>
      (hconvex i hi).translate x
  rw [← map_add_left_nhds_zero]
  exact hbasis.map _

theorem locally_convex_space_iff_zero :
    LocallyConvexSpace 𝕜 E ↔ (𝓝 0 : Filter E).HasBasis (fun s : Set E => s ∈ (𝓝 0 : Filter E) ∧ Convex 𝕜 s) id :=
  ⟨fun h => @LocallyConvexSpace.convex_basis _ _ _ _ _ _ h 0, fun h =>
    LocallyConvexSpace.of_basis_zero 𝕜 E _ _ h fun s => And.right⟩

theorem locally_convex_space_iff_exists_convex_subset_zero :
    LocallyConvexSpace 𝕜 E ↔ ∀, ∀ U ∈ (𝓝 0 : Filter E), ∀, ∃ S ∈ (𝓝 0 : Filter E), Convex 𝕜 S ∧ S ⊆ U :=
  (locally_convex_space_iff_zero 𝕜 E).trans has_basis_self

end Module

section LatticeOps

variable {ι : Sort _} {𝕜 E F : Type _} [OrderedSemiring 𝕜] [AddCommMonoidₓ E] [Module 𝕜 E] [AddCommMonoidₓ F]
  [Module 𝕜 F]

theorem locally_convex_space_Inf {ts : Set (TopologicalSpace E)} (h : ∀, ∀ t ∈ ts, ∀, @LocallyConvexSpace 𝕜 E _ _ _ t) :
    @LocallyConvexSpace 𝕜 E _ _ _ (inf ts) := by
  let this : TopologicalSpace E := Inf ts
  refine'
    LocallyConvexSpace.of_bases 𝕜 E (fun x => fun If : Set ts × (ts → Set E) => ⋂ i ∈ If.1, If.2 i)
      (fun x => fun If : Set ts × (ts → Set E) =>
        If.1.Finite ∧ ∀, ∀ i ∈ If.1, ∀, If.2 i ∈ @nhds _ (↑i) x ∧ Convex 𝕜 (If.2 i))
      (fun x => _) fun x If hif => convex_Inter fun i => convex_Inter fun hi => (hif.2 i hi).2
  rw [nhds_Inf, ← infi_subtype'']
  exact has_basis_infi fun i : ts => (@locally_convex_space_iff 𝕜 E _ _ _ ↑i).mp (h (↑i) i.2) x

theorem locally_convex_space_infi {ts' : ι → TopologicalSpace E} (h' : ∀ i, @LocallyConvexSpace 𝕜 E _ _ _ (ts' i)) :
    @LocallyConvexSpace 𝕜 E _ _ _ (⨅ i, ts' i) := by
  refine' locally_convex_space_Inf _
  rwa [forall_range_iff]

theorem locally_convex_space_inf {t₁ t₂ : TopologicalSpace E} (h₁ : @LocallyConvexSpace 𝕜 E _ _ _ t₁)
    (h₂ : @LocallyConvexSpace 𝕜 E _ _ _ t₂) : @LocallyConvexSpace 𝕜 E _ _ _ (t₁⊓t₂) := by
  rw [inf_eq_infi]
  refine' locally_convex_space_infi fun b => _
  cases b <;> assumption

theorem locally_convex_space_induced {t : TopologicalSpace F} [LocallyConvexSpace 𝕜 F] (f : E →ₗ[𝕜] F) :
    @LocallyConvexSpace 𝕜 E _ _ _ (t.induced f) := by
  let this : TopologicalSpace E := t.induced f
  refine'
    LocallyConvexSpace.of_bases 𝕜 E (fun x => preimage f) (fun x => fun s : Set F => s ∈ 𝓝 (f x) ∧ Convex 𝕜 s)
      (fun x => _) fun x s ⟨_, hs⟩ => hs.linear_preimage f
  rw [nhds_induced]
  exact (LocallyConvexSpace.convex_basis <| f x).comap f

instance {ι : Type _} {X : ι → Type _} [∀ i, AddCommMonoidₓ (X i)] [∀ i, TopologicalSpace (X i)] [∀ i, Module 𝕜 (X i)]
    [∀ i, LocallyConvexSpace 𝕜 (X i)] : LocallyConvexSpace 𝕜 (∀ i, X i) :=
  locally_convex_space_infi fun i => locally_convex_space_induced (LinearMap.proj i)

instance [TopologicalSpace E] [TopologicalSpace F] [LocallyConvexSpace 𝕜 E] [LocallyConvexSpace 𝕜 F] :
    LocallyConvexSpace 𝕜 (E × F) :=
  locally_convex_space_inf (locally_convex_space_induced (LinearMap.fst _ _ _))
    (locally_convex_space_induced (LinearMap.snd _ _ _))

end LatticeOps
