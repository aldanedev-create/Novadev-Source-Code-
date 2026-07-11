# Python Modules

NovaDev 1.1 supports Python modules wrapped in Nova source.

```nova
module ConstructionEstimator python {
    export estimate

    python """
def estimate(**payload):
    square_feet = float(payload.get("squareFeet", 1000))
    return round(square_feet * 118, 2)
"""
}
```

Use it in a workflow:

```nova
workflow EstimateRequest {
    input Lead
    uses ConstructionEstimator.estimate
    creates Estimate
}
```

Generated backend output:

```txt
backend/modules/construction_estimator.py
backend/workflows/estimate_request.py
POST /api/workflows/estimate-request
```

Validation checks that Python code compiles and that workflow references point
to existing modules and exports.
