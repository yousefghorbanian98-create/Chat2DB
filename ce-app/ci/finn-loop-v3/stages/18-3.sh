#!/usr/bin/env bash
set -euo pipefail
# 18.3 Bump to 1.5.0 -> CI release -> verify differential update path
node -e "const p=require('./ce-app/frontend/package.json');p.version='1.5.0';require('fs').writeFileSync('ce-app/frontend/package.json',JSON.stringify(p,null,2)+'\n')"
echo "push this branch; ce-workflow.yml builds + publishes v1.5.0 automatically"
