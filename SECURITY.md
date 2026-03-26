# Security Advisory

## LiteLLM Supply Chain Compromise (March 2026)

### Summary

LiteLLM versions **1.82.7** and **1.82.8** were compromised in a supply chain attack on March 24, 2026. The malicious packages have been removed from PyPI.

This project pins LiteLLM to the last known safe version: **1.82.6**.

### What happened

The threat actor (TeamPCP) compromised a LiteLLM maintainer's PyPI credentials and published two malicious versions containing:

- Credential stealers targeting AWS keys, GCP credentials, GitHub tokens, SSH keys, `.env` files, and cryptocurrency wallets
- Data exfiltration to an attacker-controlled domain (`models.litellm.cloud`)
- Kubernetes lateral movement tools
- A persistent systemd backdoor (C2)
- A `.pth` file (`litellm_init.pth`) that executes automatically on every Python process startup

### What to do

- **DO NOT** install `litellm>=1.82.7` until the LiteLLM team confirms new releases are safe
- This repo pins `litellm==1.82.6` in `backend/pyproject.toml`
- If you previously installed 1.82.7 or 1.82.8, **rotate all credentials** in that environment immediately

### Pinned version

| Package  | Pinned Version | Reason                                      |
|----------|---------------|----------------------------------------------|
| litellm  | ==1.82.6      | Versions 1.82.7-1.82.8 contained malware    |

### References

- [LiteLLM Official Security Update](https://docs.litellm.ai/blog/security-update-march-2026)
- [GitHub Issue #24518](https://github.com/BerriAI/litellm/issues/24518)
- [The Hacker News Coverage](https://thehackernews.com/2026/03/teampcp-backdoors-litellm-versions.html)
- [Sonatype Analysis](https://www.sonatype.com/blog/compromised-litellm-pypi-package-delivers-multi-stage-credential-stealer)

### Updating this pin

Once the LiteLLM team completes their supply chain review and publishes verified safe releases, update the pin in:

1. `backend/pyproject.toml` — change `litellm==1.82.6` to the new safe version
2. `.env.example` — update the install instruction
3. This file — note the resolution
