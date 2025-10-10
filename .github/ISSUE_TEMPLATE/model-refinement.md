---
name: Model Refinement
about: Refine generated models to eliminate more repetition and improve type accuracy
title: 'Refine generated models: additional mixins and optional field review'
labels: enhancement, models, code-generation
assignees: ''
---

## Overview

While we've made significant improvements to the generated models (enums, mixins, snake_case, required fields), there are opportunities for further refinement.

## Current State

✅ **Completed:**
- 22 enum types with 210 values
- 18 field mixins (629 fields eliminated, 52.9% reduction)
- 29 method mixins (~141 helper methods)
- 894 required fields (64%)
- 100% snake_case with aliases
- Comprehensive validation

## Areas for Further Refinement

### 1. Additional Field Mixins

Some repeated fields could potentially be moved to mixins:

**Candidate fields for new mixins:**
- `time` field (appears in 8 models) - could be `TimeFields` mixin
- `id` field (appears in 5 models) - could be `IdFields` mixin
- `metadata` field (appears in 55 wrapper models) - could be `MetadataFields` mixin
- `data` field (appears in 130 wrapper models) - could be `DataFields` mixin
- `bid` + `offer` fields - could be part of `BidOfferFields` mixin (currently only methods)
- `margin` field (appears in 7 models) - could be `MarginFields` mixin
- `surplus` field (appears in 6 models) - could be `SurplusFields` mixin

**Potential impact:**
- Could eliminate another ~100-150 field definitions
- Would increase mixin coverage from 50% to 60%+

### 2. Optional Field Review

Some fields marked as `Optional` might actually be required based on API behavior:

**Fields to investigate:**
```python
# Example from BidOfferDatasetResponse:
bid: Optional[float] = Field(...)  # Has example - might be required?
offer: Optional[float] = Field(...)  # Has example - might be required?

# Example from various models:
time: Optional[datetime] = Field(...)  # Appears in 8 models with examples
```

**Approach:**
1. Make actual API calls to test endpoints
2. Analyze which fields are consistently present (>90% of responses)
3. Update `inferred_required_fields` in `tools/generate_models.py`
4. Regenerate models

**Tool available:**
- `tools/infer_required_fields.py` - Tests actual API responses

### 3. Wrapper Model Optimization

Many `*_DatasetResponse` and `*_ResponseWithMetadata` models are very similar:

```python
class SomeModel_DatasetResponse(BaseModel):
    data: Optional[List[SomeModel]] = None

class AnotherModel_DatasetResponse(BaseModel):
    data: Optional[List[AnotherModel]] = None
```

**Potential solutions:**
- Generic wrapper with TypeVar
- Shared base class for all wrapper models
- Factory function for creating wrappers

### 4. Additional Validations

Some fields could benefit from validation:

**Candidates:**
- `frequency` - Already has FrequencyMixin, ensure all frequency fields use it
- `temperature` - Already has TemperatureMixin, ensure all temperature fields use it
- `percentage` fields - Validate 0-100 range
- `capacity` fields - Validate positive values
- `volume` fields - Could validate reasonable ranges

### 5. More Comprehensive Enums

Some string fields might have limited value sets that could be enums:

**Fields to investigate:**
- `status` field (appears in multiple models)
- `priceDirection` field
- `cause` field (might have common values)
- `service` field
- `dataType` field

## Implementation Plan

### Phase 1: Data Collection (Low effort)
- [ ] Run `tools/infer_required_fields.py` with API key
- [ ] Analyze actual API responses for field presence
- [ ] Document findings in `tools/field_analysis.md`

### Phase 2: Additional Field Mixins (Medium effort)
- [ ] Create `TimeFields`, `IdFields`, `MarginFields`, `SurplusFields` mixins
- [ ] Update `tools/generate_models.py` to detect these patterns
- [ ] Regenerate models
- [ ] Test with `test_all_improvements.py`

### Phase 3: Optional Field Refinement (Medium effort)
- [ ] Review fields with examples that are marked Optional
- [ ] Update `inferred_required_fields` based on API testing
- [ ] Regenerate models
- [ ] Update tests to handle new required fields

### Phase 4: Wrapper Model Optimization (Low-Medium effort)
- [ ] Design generic wrapper approach
- [ ] Implement in `tools/generate_models.py`
- [ ] Test with existing code

### Phase 5: Additional Validations (Low effort)
- [ ] Add percentage validation
- [ ] Add positive value validation for capacity/volume
- [ ] Ensure all frequency/temperature fields use appropriate mixins

## Success Criteria

- [ ] Field mixin coverage >60% (currently 50%)
- [ ] Required field percentage >70% (currently 64%)
- [ ] Additional 100-150 field definitions eliminated
- [ ] All tests passing
- [ ] Documentation updated

## Notes

- Maintain backward compatibility where possible
- Use `populate_by_name=True` to support both snake_case and camelCase
- Keep API compatibility via aliases
- Ensure all changes are tested

## Related Files

- `elexon_bmrs/generated_models.py` - Generated models
- `elexon_bmrs/field_mixins.py` - Field mixin definitions
- `elexon_bmrs/validators.py` - Method mixin definitions
- `elexon_bmrs/enums.py` - Enum definitions
- `tools/generate_models.py` - Model generator
- `tools/generate_enums.py` - Enum generator
- `tools/infer_required_fields.py` - API testing tool

