# LogBreak Backend
This repo contains Cloud Functions that are used by LogBreak app for more intensive computations (not suitable for frontend).

## /releases/{owner}/{repository}
Queries project releases using Github GraphQL API. Then finds all releases that might contain breaking changes (using semantic versioning conventions and keyword matching).
