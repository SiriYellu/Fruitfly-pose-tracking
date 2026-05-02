## Push `main` to GitHub from this workstation

HTTPS may fail until credentials are configured (`could not read Username`).

### A. SSH (with GitHub key added)

```bash
cd /path/to/Fruitfly-pose-tracking-rebuild
git remote set-url origin git@github.com:SiriYellu/Fruitfly-pose-tracking.git
ssh -T git@github.com
git push origin main
```

### B. PAT over HTTPS

```bash
git push https://YOUR_USERNAME:YOUR_TOKEN@github.com/SiriYellu/Fruitfly-pose-tracking.git main
```

### C. GitHub CLI

```bash
gh auth login
git push origin main
```
