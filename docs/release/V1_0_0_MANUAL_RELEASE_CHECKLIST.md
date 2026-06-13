# v1.0.0 Manual Release Checklist

**Release posture before maintainer action:** v1.0.0 prepared_not_released

1. Verify main is clean.
2. Verify CI is green.
3. Verify pyproject.toml version is 1.0.0.
4. Run python -m odin.cli validate-all.
5. Run pytest.
6. Optionally create git tag v1.0.0.
   - manual_only: true
   - claimed_by_pr56: false
7. Optionally create GitHub Release v1.0.0.
   - manual_only: true
   - claimed_by_pr56: false
8. Optionally upload release assets.
   - manual_only: true
   - claimed_by_pr56: false
9. Optionally publish to PyPI.
   - manual_only: true
   - claimed_by_pr56: false
10. Verify external release state after publication.
    - manual_only: true
    - claimed_by_pr56: false
11. Record external release receipts separately.
    - manual_only: true
    - claimed_by_pr56: false
